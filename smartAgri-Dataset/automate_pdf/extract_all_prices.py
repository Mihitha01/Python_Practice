"""
Unified PDF Price Extraction Script
Handles both OLD format (2016-2019) and NEW format (2020-2025)
Extracts vegetable prices from CBSL daily price reports

Author: Auto-generated
Date: December 2025
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
OUTPUT_FILE = 'extracted_prices_all.csv'

# Products to extract (common across both formats)
VEGETABLES = ['Beans', 'Carrot', 'Cabbage', 'Tomato', 'Tomatoes', 'Brinjal', 'Pumpkin', 'Snake gourd']
OTHER_ITEMS = ['Red Onion', 'Big Onion', 'Potato', 'Dried Chilli', 'Coconut', 'Green Chilli', 'Lime']


def detect_format(pdf):
    """
    Detect PDF format based on structure
    Returns: 'old' (2016-2019) or 'new' (2020-2025)
    """
    num_pages = len(pdf.pages)
    
    # New format typically has 2 pages, old format has 4-5 pages
    if num_pages == 2:
        return 'new'
    
    # Check page 2 content for format indicators
    if num_pages > 1:
        text = pdf.pages[1].extract_text() or ''
        # New format has "Yesterday Today" columns
        if 'Yesterday' in text and 'Today' in text:
            # Check if it has Narahenpita (new format indicator)
            if 'Narahenpita' in text:
                return 'new'
            # Check for V E G E T A B L E S spacing (new format)
            if 'V E G E T A B L E S' in text:
                return 'new'
        # Old format has "Previous Week Today" or "Previous 5 Days Average"
        if 'Previous Week' in text or 'Previous' in text and '5 Days' in text:
            return 'old'
    
    # Default to old if 4+ pages
    if num_pages >= 4:
        return 'old'
    
    return 'new'


def extract_date_from_pdf(pdf):
    """Extract date from PDF text"""
    try:
        # Try page 1 first
        text = pdf.pages[0].extract_text() or ''
        
        # Pattern: "18 December 2025" or "1 August 2016"
        match = re.search(
            r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})',
            text,
            re.IGNORECASE
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
    """
    Parse price string to float
    Handles: "800.00", "8 00.00", "1 ,200.00", "n.a."
    """
    if not price_str or price_str.strip() == '' or 'n.a.' in str(price_str).lower():
        return None
    
    try:
        # Remove spaces within numbers: "8 00.00" -> "800.00"
        cleaned = re.sub(r'(\d)\s+([,\d])', r'\1\2', str(price_str).strip())
        # Remove commas
        cleaned = cleaned.replace(',', '')
        # Extract the number
        match = re.search(r'[\d.]+', cleaned)
        if match:
            return float(match.group())
    except:
        pass
    return None


def extract_old_format(pdf, report_date):
    """
    Extract prices from OLD format PDFs (2016-2019)
    Structure: Table with columns:
    Pettah WS (Prev, Today), Dambulla WS (Prev, Today), Pettah Retail (Prev, Today), Dambulla Retail (Prev, Today)
    Indices for TODAY: 1, 3, 5, 7
    """
    data = []
    
    try:
        # Get page 1 or 2 (vegetables are usually on page 1 or 2)
        for page_idx in [0, 1]:
            if page_idx >= len(pdf.pages):
                continue
                
            page = pdf.pages[page_idx]
            text = page.extract_text() or ''
            
            # Skip if no vegetable data
            if 'Beans' not in text and 'Carrot' not in text:
                continue
            
            # Parse line by line
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Try to match vegetable lines
                # Format: "Beans 300.00 340.00 248.00 325.00 351.00 400.00 268.00 345.00"
                for veg in VEGETABLES:
                    if line.startswith(veg):
                        # Extract all numbers from the line
                        numbers = re.findall(r'\d+\.\d+', line)
                        
                        if len(numbers) >= 8:
                            # OLD format column order:
                            # [0] Pettah WS Prev, [1] Pettah WS Today, 
                            # [2] Dambulla WS Prev, [3] Dambulla WS Today,
                            # [4] Pettah Retail Prev, [5] Pettah Retail Today,
                            # [6] Dambulla Retail Prev, [7] Dambulla Retail Today
                            product = veg if veg != 'Tomatoes' else 'Tomato'
                            
                            data.append({
                                'Date': report_date,
                                'Product': product,
                                'Pettah_Wholesale': parse_price(numbers[1]),
                                'Dambulla_Wholesale': parse_price(numbers[3]),
                                'Pettah_Retail': parse_price(numbers[5]),
                                'Dambulla_Retail': parse_price(numbers[7]),
                                'Narahenpita_Retail': None  # Not available in old format
                            })
                        elif len(numbers) >= 4:
                            # Some old formats have fewer columns (only Pettah)
                            product = veg if veg != 'Tomatoes' else 'Tomato'
                            
                            data.append({
                                'Date': report_date,
                                'Product': product,
                                'Pettah_Wholesale': parse_price(numbers[1]) if len(numbers) > 1 else None,
                                'Dambulla_Wholesale': parse_price(numbers[3]) if len(numbers) > 3 else None,
                                'Pettah_Retail': None,
                                'Dambulla_Retail': None,
                                'Narahenpita_Retail': None
                            })
                        break
            
            if data:  # Found data on this page
                break
                
    except Exception as e:
        pass
    
    return data


def extract_new_format(pdf, report_date):
    """
    Extract prices from NEW format PDFs (2020-2025)
    Structure: Page 2 has table with Yesterday/Today for 5 markets
    Uses the existing proven extraction logic
    """
    data = []
    
    try:
        # Data is on page 2 (index 1)
        if len(pdf.pages) < 2:
            return data
        
        text = pdf.pages[1].extract_text() or ''
        
        # Find VEGETABLES section
        veg_start = text.find('V E G E T A B L E S')
        if veg_start == -1:
            veg_start = text.find('Vegetables')
        
        other_start = text.find('O T H E R')
        if other_start == -1:
            other_start = text.find('Other')
        
        if veg_start == -1:
            return data
        
        # Extract vegetables section
        if other_start > veg_start:
            veg_text = text[veg_start:other_start]
        else:
            veg_text = text[veg_start:veg_start+2000]
        
        # Parse each vegetable line
        lines = veg_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Match vegetable names
            for veg in VEGETABLES:
                if line.startswith(veg):
                    # Fix spacing issues: "7 00.00" -> "700.00", "1 ,200.00" -> "1,200.00"
                    # First, fix the space before decimal numbers pattern
                    cleaned_line = line
                    
                    # Pattern: digit + space + digits + .00 (e.g., "7 00.00" -> "700.00")
                    cleaned_line = re.sub(r'(\d)\s+(\d+\.\d+)', r'\1\2', cleaned_line)
                    # Pattern: digit + space + comma (e.g., "1 ,200" -> "1,200")  
                    cleaned_line = re.sub(r'(\d)\s+,', r'\1,', cleaned_line)
                    # Pattern: comma + space + digit (e.g., ", 200" -> ",200")
                    cleaned_line = re.sub(r',\s+(\d)', r',\1', cleaned_line)
                    
                    # Now extract all price numbers
                    numbers = re.findall(r'[\d,]+\.\d+', cleaned_line)
                    
                    if len(numbers) >= 10:
                        # We want TODAY prices: indices 1, 3, 5, 7, 9
                        # [Pettah WS Yesterday, Pettah WS Today, Dambulla WS Yesterday, Dambulla WS Today,
                        #  Pettah Retail Yesterday, Pettah Retail Today, Dambulla Retail Yesterday, Dambulla Retail Today,
                        #  Narahenpita Retail Yesterday, Narahenpita Retail Today]
                        product = veg if veg != 'Tomatoes' else 'Tomato'
                        
                        data.append({
                            'Date': report_date,
                            'Product': product,
                            'Pettah_Wholesale': parse_price(numbers[1]),
                            'Dambulla_Wholesale': parse_price(numbers[3]),
                            'Pettah_Retail': parse_price(numbers[5]),
                            'Dambulla_Retail': parse_price(numbers[7]),
                            'Narahenpita_Retail': parse_price(numbers[9])
                        })
                    elif len(numbers) >= 8:
                        # Sometimes Narahenpita is missing
                        product = veg if veg != 'Tomatoes' else 'Tomato'
                        
                        data.append({
                            'Date': report_date,
                            'Product': product,
                            'Pettah_Wholesale': parse_price(numbers[1]),
                            'Dambulla_Wholesale': parse_price(numbers[3]),
                            'Pettah_Retail': parse_price(numbers[5]),
                            'Dambulla_Retail': parse_price(numbers[7]),
                            'Narahenpita_Retail': None
                        })
                    break
        
        # Also extract OTHER section items
        if other_start > 0:
            fruits_start = text.find('F R U I T S')
            if fruits_start == -1:
                fruits_start = text.find('Fruits')
            if fruits_start == -1:
                fruits_start = len(text)
            
            other_text = text[other_start:fruits_start]
            lines = other_text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                for item in OTHER_ITEMS:
                    if item in line:
                        # Fix spacing issues
                        cleaned_line = re.sub(r'(\d)\s+(\d+\.\d+)', r'\1\2', line)
                        cleaned_line = re.sub(r'(\d)\s+,', r'\1,', cleaned_line)
                        cleaned_line = re.sub(r',\s+(\d)', r',\1', cleaned_line)
                        
                        numbers = re.findall(r'[\d,]+\.\d+', cleaned_line)
                        
                        if len(numbers) >= 10:
                            data.append({
                                'Date': report_date,
                                'Product': item,
                                'Pettah_Wholesale': parse_price(numbers[1]),
                                'Dambulla_Wholesale': parse_price(numbers[3]),
                                'Pettah_Retail': parse_price(numbers[5]),
                                'Dambulla_Retail': parse_price(numbers[7]),
                                'Narahenpita_Retail': parse_price(numbers[9])
                            })
                        elif len(numbers) >= 8:
                            data.append({
                                'Date': report_date,
                                'Product': item,
                                'Pettah_Wholesale': parse_price(numbers[1]),
                                'Dambulla_Wholesale': parse_price(numbers[3]),
                                'Pettah_Retail': parse_price(numbers[5]),
                                'Dambulla_Retail': parse_price(numbers[7]),
                                'Narahenpita_Retail': None
                            })
                        break
                        
    except Exception as e:
        pass
    
    return data


def process_pdf(pdf_path):
    """Process a single PDF and return extracted data"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Get date
            report_date = extract_date_from_pdf(pdf)
            if not report_date:
                # Try to extract from filename
                filename = os.path.basename(pdf_path)
                match = re.search(r'(\d{8})', filename)
                if match:
                    date_str = match.group(1)
                    report_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            
            if not report_date:
                return [], 'no_date'
            
            # Detect format
            fmt = detect_format(pdf)
            
            # Extract based on format
            if fmt == 'old':
                data = extract_old_format(pdf, report_date)
            else:
                data = extract_new_format(pdf, report_date)
            
            return data, fmt
            
    except Exception as e:
        return [], f'error: {str(e)}'


def main():
    print("="*70)
    print("Unified PDF Price Extraction")
    print("Processing all PDFs from 2016-2025")
    print("="*70)
    
    # Get all PDF files
    pdf_pattern = os.path.join(PDF_FOLDER, '*.pdf')
    pdf_files = sorted(glob.glob(pdf_pattern))
    
    print(f"\nFound {len(pdf_files)} PDF files")
    
    all_data = []
    stats = {'old': 0, 'new': 0, 'error': 0, 'no_data': 0}
    
    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        data, fmt = process_pdf(pdf_file)
        
        if data:
            all_data.extend(data)
            if fmt in ['old', 'new']:
                stats[fmt] += 1
        else:
            if 'error' in str(fmt):
                stats['error'] += 1
            else:
                stats['no_data'] += 1
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    if len(df) > 0:
        # Sort by date and product
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(['Date', 'Product'])
        
        # Save to CSV
        df.to_csv(OUTPUT_FILE, index=False)
        
        print("\n" + "="*70)
        print("EXTRACTION COMPLETE")
        print("="*70)
        print(f"\nStatistics:")
        print(f"  Old format PDFs processed: {stats['old']}")
        print(f"  New format PDFs processed: {stats['new']}")
        print(f"  Errors: {stats['error']}")
        print(f"  No data extracted: {stats['no_data']}")
        print(f"\nTotal records extracted: {len(df)}")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"Products: {df['Product'].nunique()}")
        print(f"\nOutput saved to: {OUTPUT_FILE}")
        
        # Show sample
        print("\nSample data (first 10 rows):")
        print(df.head(10).to_string())
    else:
        print("\nNo data extracted!")
    
    return df


if __name__ == "__main__":
    main()
