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
OUTPUT_FILE = './extracted_prices.csv'

# TODAY price columns (Yesterday/Today pairs in single cell)
# Col 0=Item, Col 1=Unit
# Col 2: Pettah WS (format: "yesterday today"), Col 4: Dambulla WS, 
# Col 6: Pettah Retail, Col 8: Dambulla Retail, Col 10: Narahenpita Retail

MARKET_COLUMNS = {
    'Pettah (Wholesale)': 2,
    'Dambulla (Wholesale)': 4,
    'Pettah (Retail)': 6,
    'Dambulla (Retail)': 8,
    'Narahenpita (Retail)': 10
}


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


def parse_price(price_str):
    """
    Parse a price string in format "yesterday today" like "800.00 800.00" or "8 00.00 8 00.00"
    Returns only the TODAY price (second/last price)
    """
    if not price_str or price_str.strip() == '' or price_str.strip() == 'n.a.':
        return None
    
    # Remove extra spaces within numbers (e.g., "8 00.00" -> "800.00")
    normalized = re.sub(r'(\d)\s+(\d)', r'\1\2', price_str.strip())
    
    # Split by spaces to extract prices
    parts = normalized.split()
    
    prices = []
    for part in parts:
        try:
            # Handle patterns like "1,400.00" or "400.00"
            price = float(part.replace(',', ''))
            prices.append(price)
        except ValueError:
            continue
    
    # Return the last (TODAY) price
    if prices:
        return prices[-1]
    return None


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
            section_positions = {}
            
            for i, row in enumerate(table):
                if row and row[0]:
                    cell_text = str(row[0]).upper().replace(' ', '')
                    if 'VEGETABLES' in cell_text and 'vegetables' not in section_positions:
                        section_positions['vegetables'] = i
                    elif 'OTHER' in cell_text and 'other' not in section_positions:
                        section_positions['other'] = i
                    elif 'FRUITS' in cell_text and 'fruits' not in section_positions:
                        section_positions['fruits'] = i
                    elif 'RICE' in cell_text and 'rice' not in section_positions:
                        section_positions['rice'] = i
            
            # Extract VEGETABLES section
            if 'vegetables' in section_positions and 'other' in section_positions:
                veg_start = section_positions['vegetables']
                veg_end = section_positions['other']
                all_data.extend(
                    extract_section(table, veg_start + 1, veg_end, 
                                  'Vegetables', report_date, filename)
                )
            
            # Extract OTHER section
            if 'other' in section_positions:
                other_start = section_positions['other']
                # Find the end of OTHER section (next section or end of table)
                other_end = section_positions.get('fruits', len(table))
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
    
    for row_idx in range(start_idx, end_idx):
        row = table[row_idx]
        
        # Skip if row is too short
        if not row or len(row) < 12:
            continue
        
        # Check if this row has a food name in Col 0
        food_name = row[0]
        if not food_name or not str(food_name).strip():
            continue
        
        food_name = str(food_name).strip()
        
        # Skip section headers
        if any(kw in food_name.upper().replace(' ', '') for kw in ['VEGETABLES', 'OTHER', 'FRUITS', 'RICE', 'FISH', 'MEAT']):
            break
        
        # Extract TODAY prices from each market column
        for market_name, col_idx in MARKET_COLUMNS.items():
            if col_idx < len(row) and row[col_idx]:
                price = parse_price(str(row[col_idx]))
                if price is not None:
                    section_data.append({
                        'Date': report_date,
                        'Section': section_name,
                        'Product': food_name,
                        'Market': market_name,
                        'Unit': 'Rs./kg',
                        'Price Today': price,
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
