"""
Automated PDF Price Extraction Script
Extracts vegetable and other food prices from PDF reports
Focuses on: Vegetable section and Other section  
Columns: Today prices only (ignoring Yesterday)
"""

import pdfplumber
import pandas as pd
import re
import os
import glob
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
PDF_FOLDER = '../price_pdfs_2025_01'
OUTPUT_FILE = '../extracted_prices.csv'

# Market columns for TODAY prices
# Due to merged header cells, prices are at indices 2, 4, 6, 8, 10
# Each contains "YYYY YYYY" format (Yesterday Today)
MARKET_INFO = [
    ('Pettah (Wholesale)', 2),
    ('Dambulla (Wholesale)', 4),
    ('Pettah (Retail)', 6),
    ('Dambulla (Retail)', 8),
    ('Narahenpita (Retail)', 10)
]


def extract_date_from_pdf(pdf):
    """Extract date from PDF text (usually on first page)"""
    try:
        text = pdf.pages[0].extract_text()
        # Pattern: Day Month Year (e.g., 12 December 2025)
        match = re.search(
            r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})',
            text,
            re.IGNORECASE
        )
        if match:
            return match.group(0)
    except:
        pass
    return None


def parse_price_pair(price_str):
    """
    Parse a price pair string like "800.00 800.00" or "8 00.00 8 00.00"
    Returns the TODAY price (second/last price)
    """
    if not price_str or price_str.strip() == '' or price_str.strip() == 'n.a.':
        return None
    
    # Remove extra spaces within numbers (e.g., "8 00.00" -> "800.00")
    normalized = re.sub(r'(\d)\s+(\d)', r'\1\2', price_str.strip())
    
    # Split by spaces to get price components
    parts = normalized.split()
    
    # Extract prices
    prices = []
    for part in parts:
        try:
            # Handle patterns like "1,400.00" or "400.00"
            price = float(part.replace(',', ''))
            prices.append(price)
        except ValueError:
            continue
    
    # Return the last (today) price
    if prices:
        return prices[-1]
    return None


def extract_multiline_prices(price_str):
    """
    Parse multiline price data like:
    '950.00 875.00\\n145.00 240.00\\n125.00 175.00'
    Returns list of today prices only (second price in each pair)
    """
    if not price_str or price_str.strip() == '' or price_str.strip() == 'n.a.':
        return []
    
    results = []
    lines = price_str.strip().split('\n')
    
    for line in lines:
        today_price = parse_price_pair(line)
        if today_price is not None:
            results.append(today_price)
    
    return results


def process_pdf(filepath):
    """Process a single PDF file and extract prices"""
    all_data = []
    filename = os.path.basename(filepath)
    
    try:
        with pdfplumber.open(filepath) as pdf:
            # Extract date from PDF
            report_date = extract_date_from_pdf(pdf)
            
            # Tables are on page 2 (index 1)
            if len(pdf.pages) < 2:
                return all_data
            
            page = pdf.pages[1]
            tables = page.extract_tables()
            
            if not tables:
                return all_data
            
            table = tables[0]
            
            # Find section boundaries
            vegetables_start = None
            vegetables_end = None
            other_start = None
            other_end = None
            
            for i, row in enumerate(table):
                if row[0]:
                    cell_text = str(row[0]).upper()
                    if 'VEGETABLE' in cell_text and vegetables_start is None:
                        vegetables_start = i
                    elif 'OTHER' in cell_text and other_start is None:
                        other_start = i
                        if vegetables_start is not None:
                            vegetables_end = i
                    elif any(kw in cell_text for kw in ['FRUIT', 'RICE', 'FISH', 'MEAT']):
                        if other_start is not None and other_end is None:
                            other_end = i
            
            # Set default end if not found
            if vegetables_end is None and vegetables_start is not None:
                vegetables_end = other_start if other_start else len(table)
            if other_end is None and other_start is not None:
                other_end = len(table)
            
            # Extract vegetable section
            if vegetables_start is not None and vegetables_end is not None:
                all_data.extend(
                    extract_section(table, vegetables_start + 1, vegetables_end, 
                                  'Vegetables', report_date, filename)
                )
            
            # Extract OTHER section
            if other_start is not None and other_end is not None:
                all_data.extend(
                    extract_section(table, other_start + 1, other_end, 
                                  'Other', report_date, filename)
                )
    
    except Exception as e:
        print(f"  Error processing {filename}: {e}")
    
    return all_data


def extract_section(table, start_idx, end_idx, section_name, report_date, filename):
    """Extract price data from a specific section of the table"""
    section_data = []
    current_item = None
    
    for row_idx in range(start_idx, end_idx):
        row = table[row_idx]
        
        # Skip rows where the first column indicates another section
        if row[0] and any(kw in str(row[0]).upper() for kw in ['FRUIT', 'RICE', 'FISH', 'MEAT', 'VEGETABLE', 'OTHER']):
            break
        
        # If first column has text, it's an item name
        if row[0] and str(row[0]).strip():
            current_item = str(row[0]).strip()
        
        # Extract prices from market columns
        for market_name, col_idx in MARKET_INFO:
            if col_idx < len(row) and row[col_idx]:
                price_str = str(row[col_idx]).strip()
                
                # Handle multiline prices
                if '\n' in price_str:
                    prices = extract_multiline_prices(price_str)
                    for idx, today_price in enumerate(prices):
                        if today_price is not None:
                            product_name = current_item if idx == 0 else f"{current_item} ({idx})"
                            section_data.append({
                                'Date': report_date,
                                'Section': section_name,
                                'Product': product_name,
                                'Market': market_name,
                                'Price Today': today_price,
                                'Source File': filename
                            })
                else:
                    today_price = parse_price_pair(price_str)
                    if today_price is not None and current_item:
                        section_data.append({
                            'Date': report_date,
                            'Section': section_name,
                            'Product': current_item,
                            'Market': market_name,
                            'Price Today': today_price,
                            'Source File': filename
                        })
    
    return section_data


def main():
    """Main entry point"""
    print("=" * 60)
    print("PDF Price Extraction - Vegetables & Other Sections")
    print("=" * 60)
    
    # Find all PDF files
    pdf_files = sorted(glob.glob(os.path.join(PDF_FOLDER, "*.pdf")))
    
    print(f"\nFound {len(pdf_files)} PDF files in {PDF_FOLDER}")
    
    if not pdf_files:
        print("No PDF files found. Exiting.")
        return
    
    all_data = []
    
    for idx, filepath in enumerate(pdf_files, 1):
        filename = os.path.basename(filepath)
        print(f"[{idx}/{len(pdf_files)}] Processing {filename}...", end=' ')
        
        data = process_pdf(filepath)
        all_data.extend(data)
        print(f"✓ {len(data)} records")
    
    # Save to CSV
    if all_data:
        df = pd.DataFrame(all_data)
        
        # Sort by date, section, and product
        df = df.sort_values(['Date', 'Section', 'Product']).reset_index(drop=True)
        
        df.to_csv(OUTPUT_FILE, index=False)
        
        print("\n" + "=" * 60)
        print(f"✓ SUCCESS - Extraction Complete!")
        print("=" * 60)
        print(f"Total records extracted: {len(df)}")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"Sections: {', '.join(df['Section'].unique())}")
        print(f"Markets: {', '.join(df['Market'].unique())}")
        print(f"Output file: {OUTPUT_FILE}")
        
        print(f"\nRecords by Section:")
        print(df.groupby('Section').size())
        
        print(f"\nFirst 20 records:")
        print(df.head(20).to_string(index=False))
        
    else:
        print("\n" + "=" * 60)
        print("✗ No data extracted. Check PDF structure.")
        print("=" * 60)


if __name__ == "__main__":
    main()
