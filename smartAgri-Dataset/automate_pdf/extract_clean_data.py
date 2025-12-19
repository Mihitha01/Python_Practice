"""
Clean Data Extraction Script
Handles all PDF formats (2016-2025) and creates a clean CSV for model training
"""

import pdfplumber
import pandas as pd
import re
import os
import glob
from tqdm import tqdm
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
PDF_FOLDER = '../new_price_pdf'
OUTPUT_FILE = 'vegetable_prices_clean.csv'

# Vegetables to extract
VEGETABLES = ['Beans', 'Carrot', 'Cabbage', 'Tomato', 'Tomatoes', 'Brinjal', 'Pumpkin', 'Snake gourd', 'Green Chilli', 'Lime']
OTHER_ITEMS = ['Red Onion', 'Big Onion', 'Potato', 'Dried Chilli', 'Coconut']


def extract_date_from_pdf(pdf):
    """Extract date from PDF text"""
    try:
        text = pdf.pages[0].extract_text() or ''
        match = re.search(
            r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})',
            text, re.IGNORECASE
        )
        if match:
            day = int(match.group(1))
            month_name = match.group(2)
            year = int(match.group(3))
            month_map = {
                'january': 1, 'february': 2, 'march': 3, 'april': 4,
                'may': 5, 'june': 6, 'july': 7, 'august': 8,
                'september': 9, 'october': 10, 'november': 11, 'december': 12
            }
            month = month_map[month_name.lower()]
            return datetime(year, month, day).strftime('%Y-%m-%d')
    except:
        pass
    return None


def parse_price(price_str):
    """Parse price string to float"""
    if not price_str or 'n.a.' in str(price_str).lower():
        return None
    try:
        cleaned = re.sub(r'(\d)\s+([,\d])', r'\1\2', str(price_str).strip())
        cleaned = cleaned.replace(',', '')
        match = re.search(r'[\d.]+', cleaned)
        if match:
            val = float(match.group())
            if val > 0:
                return val
    except:
        pass
    return None


def extract_prices_from_line(line, product_name):
    """
    Extract prices from a line, handling various formats
    Returns dict with prices or None
    """
    # Clean the line - fix spacing in numbers
    cleaned = re.sub(r'(\d)\s+(\d+\.\d+)', r'\1\2', line)
    cleaned = re.sub(r'(\d)\s+,', r'\1,', cleaned)
    cleaned = re.sub(r',\s+(\d)', r',\1', cleaned)
    
    # Remove n.a. and extract all numbers
    # Split by n.a. to understand structure
    parts = re.split(r'n\.a\.', cleaned)
    
    # Extract all decimal numbers
    all_numbers = re.findall(r'[\d,]+\.\d+', cleaned)
    
    if len(all_numbers) >= 10:
        # Full new format: 10 prices (Yesterday/Today for 5 markets)
        # Indices 1,3,5,7,9 are TODAY prices
        return {
            'Pettah_Wholesale': parse_price(all_numbers[1]),
            'Dambulla_Wholesale': parse_price(all_numbers[3]),
            'Pettah_Retail': parse_price(all_numbers[5]),
            'Dambulla_Retail': parse_price(all_numbers[7]),
            'Narahenpita_Retail': parse_price(all_numbers[9])
        }
    elif len(all_numbers) >= 8:
        # Old format or partial new: 8 prices
        return {
            'Pettah_Wholesale': parse_price(all_numbers[1]),
            'Dambulla_Wholesale': parse_price(all_numbers[3]),
            'Pettah_Retail': parse_price(all_numbers[5]),
            'Dambulla_Retail': parse_price(all_numbers[7]),
            'Narahenpita_Retail': None
        }
    elif len(all_numbers) >= 4:
        # Minimal format
        return {
            'Pettah_Wholesale': parse_price(all_numbers[1]) if len(all_numbers) > 1 else None,
            'Dambulla_Wholesale': parse_price(all_numbers[3]) if len(all_numbers) > 3 else None,
            'Pettah_Retail': None,
            'Dambulla_Retail': None,
            'Narahenpita_Retail': None
        }
    
    return None


def process_pdf(pdf_path):
    """Process a single PDF and return extracted data"""
    data = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Get date
            report_date = extract_date_from_pdf(pdf)
            if not report_date:
                filename = os.path.basename(pdf_path)
                match = re.search(r'(\d{8})', filename)
                if match:
                    date_str = match.group(1)
                    report_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            
            if not report_date:
                return []
            
            # Try to extract from all pages
            for page_idx in range(min(len(pdf.pages), 3)):
                page = pdf.pages[page_idx]
                text = page.extract_text() or ''
                
                # Skip pages without vegetable data
                if 'Beans' not in text and 'Carrot' not in text:
                    continue
                
                # Process each line
                lines = text.split('\n')
                
                all_products = VEGETABLES + OTHER_ITEMS
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    for product in all_products:
                        if line.startswith(product):
                            prices = extract_prices_from_line(line, product)
                            if prices:
                                product_name = product if product != 'Tomatoes' else 'Tomato'
                                data.append({
                                    'Date': report_date,
                                    'Product': product_name,
                                    **prices
                                })
                            break
                
                if data:
                    break
                    
    except Exception as e:
        pass
    
    return data


def main():
    print("="*70)
    print("Clean Data Extraction for Model Training")
    print("="*70)
    
    # Get all PDF files
    pdf_pattern = os.path.join(PDF_FOLDER, '*.pdf')
    pdf_files = sorted(glob.glob(pdf_pattern))
    
    print(f"\nFound {len(pdf_files)} PDF files")
    
    all_data = []
    success_count = 0
    
    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        data = process_pdf(pdf_file)
        if data:
            all_data.extend(data)
            success_count += 1
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    if len(df) > 0:
        # Convert date and sort
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(['Date', 'Product'])
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['Date', 'Product'], keep='first')
        
        # Save to CSV
        df.to_csv(OUTPUT_FILE, index=False)
        
        print("\n" + "="*70)
        print("EXTRACTION COMPLETE")
        print("="*70)
        print(f"\nPDFs processed successfully: {success_count}/{len(pdf_files)}")
        print(f"Total records: {len(df)}")
        print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
        print(f"Products: {sorted(df['Product'].unique())}")
        
        # Records per year
        df['Year'] = df['Date'].dt.year
        print(f"\nRecords per year:")
        print(df.groupby('Year').size().to_string())
        
        # Missing data summary
        print(f"\nMissing values per column:")
        for col in ['Pettah_Wholesale', 'Dambulla_Wholesale', 'Pettah_Retail', 'Dambulla_Retail', 'Narahenpita_Retail']:
            missing = df[col].isna().sum()
            pct = 100 * missing / len(df)
            print(f"  {col}: {missing} ({pct:.1f}%)")
        
        # Drop Year column before final save
        df = df.drop('Year', axis=1)
        df.to_csv(OUTPUT_FILE, index=False)
        
        print(f"\nOutput saved to: {OUTPUT_FILE}")
        
        # Sample data
        print("\nSample data (first 5 rows):")
        print(df.head().to_string())
    else:
        print("\nNo data extracted!")
    
    return df


if __name__ == "__main__":
    main()
