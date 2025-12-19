"""
Clean Data Extraction Script v2 (FIXED)
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
PDF_FOLDER = 'd:/Python/smartAgri-Dataset/new_price_pdf'
OUTPUT_FILE = 'd:/Python/smartAgri-Dataset/automate_pdf/vegetable_prices_clean_v2.csv'

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
        cleaned = str(price_str).replace(',', '').strip()
        val = float(cleaned)
        # Sanity check: prices should be reasonable (0 to 10000 Rs.)
        if 0 < val < 10000:
            return round(val, 2)
    except:
        pass
    return None


def extract_prices_from_line(line, is_old_format=False):
    """
    Extract prices from a line, handling various formats
    
    OLD FORMAT (2016-2019): Numbers are space-separated
    e.g., "Beans Rs./Kg 173.00 155.00 199.00 190.00 156.00 190.00 191.00 215.00"
    Pattern: Product Unit Prev1 Today1 Prev2 Today2 Prev3 Today3 Prev4 Today4
    
    NEW FORMAT (2020+): Numbers may have n.a. and different structure
    e.g., "Beans 7 00.00 730.00 690.00 725.00 n.a. n.a. n.a. n.a. n.a. n.a."
    Sometimes numbers have spaces: "7 00.00" should be "700.00"
    
    Returns dict with prices or None
    """
    
    # Replace n.a. with a placeholder to preserve structure
    cleaned = line.replace('n.a.', 'NA')
    
    if is_old_format:
        # OLD FORMAT: Numbers are cleanly separated by spaces
        # Extract all decimal numbers directly
        all_numbers = re.findall(r'\d+\.\d+', cleaned)
        
        # Old format has 8 numbers: Prev/Today pairs for 4 markets
        # We want indices 1, 3, 5, 7 (Today values)
        if len(all_numbers) >= 8:
            return {
                'Pettah_Wholesale': parse_price(all_numbers[1]),
                'Dambulla_Wholesale': parse_price(all_numbers[3]),
                'Pettah_Retail': parse_price(all_numbers[5]),
                'Dambulla_Retail': parse_price(all_numbers[7]),
                'Narahenpita_Retail': None
            }
        elif len(all_numbers) >= 4:
            # Some old PDFs only have wholesale
            return {
                'Pettah_Wholesale': parse_price(all_numbers[1]) if len(all_numbers) > 1 else None,
                'Dambulla_Wholesale': parse_price(all_numbers[3]) if len(all_numbers) > 3 else None,
                'Pettah_Retail': None,
                'Dambulla_Retail': None,
                'Narahenpita_Retail': None
            }
    else:
        # NEW FORMAT: May have spaces within numbers like "7 00.00"
        # Fix spacing issues: "7 00.00" -> "700.00"
        # But be careful not to merge separate numbers
        
        # Pattern: digit(s) space digit(s).digit(s) -> merge them
        # This handles "7 00.00" -> "700.00" but not "700.00 730.00"
        fixed = re.sub(r'(\d)\s+(\d+\.\d{2})\b', r'\1\2', cleaned)
        
        # Also fix cases like "1 ,100.00" -> "1,100.00"
        fixed = re.sub(r'(\d)\s*,\s*(\d)', r'\1,\2', fixed)
        
        # Extract all decimal numbers
        all_numbers = re.findall(r'[\d,]+\.\d+', fixed)
        
        # New format has 10 numbers: Yesterday/Today for 5 markets
        # We want indices 1, 3, 5, 7, 9 (Today values)
        if len(all_numbers) >= 10:
            return {
                'Pettah_Wholesale': parse_price(all_numbers[1]),
                'Dambulla_Wholesale': parse_price(all_numbers[3]),
                'Pettah_Retail': parse_price(all_numbers[5]),
                'Dambulla_Retail': parse_price(all_numbers[7]),
                'Narahenpita_Retail': parse_price(all_numbers[9])
            }
        elif len(all_numbers) >= 8:
            # Partial format (no Narahenpita)
            return {
                'Pettah_Wholesale': parse_price(all_numbers[1]),
                'Dambulla_Wholesale': parse_price(all_numbers[3]),
                'Pettah_Retail': parse_price(all_numbers[5]),
                'Dambulla_Retail': parse_price(all_numbers[7]),
                'Narahenpita_Retail': None
            }
        elif len(all_numbers) >= 4:
            return {
                'Pettah_Wholesale': parse_price(all_numbers[1]) if len(all_numbers) > 1 else None,
                'Dambulla_Wholesale': parse_price(all_numbers[3]) if len(all_numbers) > 3 else None,
                'Pettah_Retail': None,
                'Dambulla_Retail': None,
                'Narahenpita_Retail': None
            }
    
    return None


def detect_pdf_format(pdf):
    """Detect if PDF is old format (2016-2019) or new format (2020+)"""
    try:
        text = pdf.pages[0].extract_text() or ''
        
        # Old format indicators:
        # - Has "Rs./Kg" in the vegetable rows
        # - Has 4-5 pages
        # - Header mentions specific markets differently
        
        if 'Rs./Kg' in text and 'Rs./Nut' in text:
            return 'old'
        
        # Check filename date
        # New format has different structure
        if 'Previous' in text and 'Yesterday' in text:
            return 'new'
        
        # Check number of pages
        if len(pdf.pages) >= 4:
            return 'old'
        
        return 'new'
    except:
        return 'new'


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
            
            # Detect format
            is_old_format = detect_pdf_format(pdf) == 'old'
            
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
                            prices = extract_prices_from_line(line, is_old_format)
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
    print("Clean Data Extraction for Model Training (v2 - Fixed)")
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
        print(f"Total records: {len(df):,}")
        print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
        print(f"Products: {len(df['Product'].unique())} ({', '.join(sorted(df['Product'].unique()))})")
        
        # Records per year
        df['Year'] = df['Date'].dt.year
        print(f"\nRecords per year:")
        for year, count in df.groupby('Year').size().items():
            print(f"  {year}: {count:,}")
        
        # Missing data summary
        print(f"\nMissing values per column:")
        for col in ['Pettah_Wholesale', 'Dambulla_Wholesale', 'Pettah_Retail', 'Dambulla_Retail', 'Narahenpita_Retail']:
            missing = df[col].isna().sum()
            pct = 100 * missing / len(df)
            print(f"  {col}: {missing:,} ({pct:.1f}%)")
        
        # Drop Year column before final save
        df = df.drop('Year', axis=1)
        df.to_csv(OUTPUT_FILE, index=False)
        
        print(f"\nOutput saved to: {OUTPUT_FILE}")
        
        # Sample data
        print("\nSample data from 2017 (old format):")
        sample_old = df[df['Date'].dt.year == 2017].head(5)
        print(sample_old[['Date', 'Product', 'Pettah_Wholesale', 'Dambulla_Wholesale']].to_string())
        
        print("\nSample data from 2024 (new format):")
        sample_new = df[df['Date'].dt.year == 2024].head(5)
        print(sample_new[['Date', 'Product', 'Pettah_Wholesale', 'Dambulla_Wholesale', 'Pettah_Retail']].to_string())
        
        # Data quality check
        print("\n" + "="*70)
        print("DATA QUALITY CHECK")
        print("="*70)
        suspicious = df[(df['Pettah_Wholesale'] > 5000) | (df['Dambulla_Wholesale'] > 5000)]
        if len(suspicious) > 0:
            print(f"\nWARNING: {len(suspicious)} records have prices > 5000 (may be parsing errors)")
            print(suspicious[['Date', 'Product', 'Pettah_Wholesale', 'Dambulla_Wholesale']].head(10).to_string())
        else:
            print("\n✓ All prices are within reasonable range (< 5000)")
        
    else:
        print("\nNo data extracted!")
    
    return df


if __name__ == "__main__":
    main()
