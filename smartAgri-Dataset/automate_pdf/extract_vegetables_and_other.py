"""
Automated PDF Price Extraction Script
Extracts vegetable and other food prices from PDF reports
Uses text parsing to get product names and table extraction for prices
"""

import pdfplumber
import pandas as pd
import re
import os
import glob

# ==========================================
# CONFIGURATION
# ==========================================
PDF_FOLDER = '../price_pdfs_2025_01'
OUTPUT_FILE = 'extracted_prices.csv'

# TODAY price columns (cols contain "yesterday today" format)
# Col 2: Pettah WS, Col 4: Dambulla WS, Col 6: Pettah Retail, Col 8: Dambulla Retail, Col 10: Narahenpita Retail

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


def parse_today_price(price_str):
    """
    Extract TODAY price from "yesterday today" format like "800.00 800.00"
    Returns only the TODAY price (second price)
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
            price = float(part.replace(',', ''))
            prices.append(price)
        except ValueError:
            continue
    
    # Return the last (TODAY) price
    if prices:
        return prices[-1]
    return None


def extract_product_names_from_text(page_text, section_name):
    """
    Extract product names from page text for a specific section
    Returns list of product names in order
    """
    products = []
    
    # Find the section
    if section_name == 'Vegetables':
        section_marker = 'V E G E T A B L E S'
        next_section_marker = 'O T H E R'
    else:  # Other
        section_marker = 'O T H E R'
        next_section_marker = 'F R U I T S'
    
    # Find section start and end in text
    try:
        start_idx = page_text.find(section_marker)
        if start_idx == -1:
            return products
        
        # Find next section
        end_idx = page_text.find(next_section_marker, start_idx)
        if end_idx == -1:
            end_idx = len(page_text)
        
        section_text = page_text[start_idx:end_idx]
        
        # Split by lines and extract product names
        lines = section_text.split('\n')
        for line in lines:
            # Product lines have pattern: "ProductName Rs./kg price price price ..."
            # Skip header and section marker lines
            if 'Rs./kg' in line and section_marker not in line and next_section_marker not in line:
                # Extract product name (everything before "Rs./kg")
                product = line.split('Rs./kg')[0].strip()
                if product and len(product) > 1:
                    products.append(product)
    except:
        pass
    
    return products


def process_pdf(filepath):
    """Process a single PDF file and extract prices"""
    all_data = []
    filename = os.path.basename(filepath)
    
    try:
        with pdfplumber.open(filepath) as pdf:
            # Extract date from PDF
            report_date = extract_date_from_pdf(pdf)
            
            # Get page 2 text and table
            if len(pdf.pages) < 2:
                return all_data
            
            page = pdf.pages[1]
            page_text = page.extract_text()
            tables = page.extract_tables()
            
            if not tables:
                return all_data
            
            table = tables[0]
            
            # Extract product names for each section
            vegetables = extract_product_names_from_text(page_text, 'Vegetables')
            others = extract_product_names_from_text(page_text, 'Other')
            
            # Find section rows in table
            section_rows = {}
            for i, row in enumerate(table):
                if row and row[0]:
                    cell_text = str(row[0]).upper().replace(' ', '')
                    if 'VEGETABLES' in cell_text:
                        section_rows['vegetables'] = i
                    elif 'OTHER' in cell_text:
                        section_rows['other'] = i
                    elif 'FRUITS' in cell_text:
                        section_rows['fruits'] = i
            
            # Extract VEGETABLES section
            if 'vegetables' in section_rows and 'other' in section_rows:
                veg_start = section_rows['vegetables'] + 1
                veg_end = section_rows['other']
                all_data.extend(
                    extract_section_data(table, veg_start, veg_end, vegetables,
                                       'Vegetables', report_date, filename)
                )
            
            # Extract OTHER section
            if 'other' in section_rows:
                other_start = section_rows['other'] + 1
                other_end = section_rows.get('fruits', len(table))
                all_data.extend(
                    extract_section_data(table, other_start, other_end, others,
                                       'Other', report_date, filename)
                )
    
    except Exception as e:
        print(f"  Error processing {filename}: {e}")
    
    return all_data


def extract_section_data(table, start_idx, end_idx, product_names, section_name, report_date, filename):
    """Extract price data for a section"""
    section_data = []
    product_idx = 0
    
    for row_idx in range(start_idx, end_idx):
        row = table[row_idx]
        
        # Skip if row is too short
        if not row or len(row) < 11:
            continue
        
        # Check if this row has any price data
        has_price = False
        for col_idx in [2, 4, 6, 8, 10]:
            if col_idx < len(row) and row[col_idx]:
                has_price = True
                break
        
        if not has_price:
            continue
        
        # Only process the first 5 columns (actual markets), not multiline cells
        # Get product name - only advance if this is a single-line data row
        if product_idx < len(product_names):
            product_name = product_names[product_idx]
            
            # Check if this row has multiline prices (prices on multiple rows for same product)
            has_multiline = False
            for col_idx in [2, 4, 6, 8, 10]:
                if col_idx < len(row) and row[col_idx] and '\n' in str(row[col_idx]):
                    has_multiline = True
                    break
            
            # Only increment product_idx if we don't have multiline (single product row)
            if not has_multiline:
                product_idx += 1
        else:
            # Skip rows beyond the number of products
            continue
        
        # Extract TODAY prices from each market
        for market_name, col_idx in MARKET_COLUMNS.items():
            if col_idx < len(row) and row[col_idx]:
                today_price = parse_today_price(str(row[col_idx]))
                if today_price is not None:
                    section_data.append({
                        'Date': report_date,
                        'Product': product_name,
                        'Market': market_name,
                        'Unit': 'Rs./kg',
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
        print(f"OK {len(data)} records")
    
    # Save to CSV
    if all_data:
        df = pd.DataFrame(all_data)
        
        # Sort by date and product
        df = df.sort_values(['Date', 'Product']).reset_index(drop=True)
        
        df.to_csv(OUTPUT_FILE, index=False)
        
        print("\n" + "=" * 60)
        print(f"SUCCESS - Extraction Complete!")
        print("=" * 60)
        print(f"Total records extracted: {len(df)}")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"Markets: {', '.join(df['Market'].unique())}")
        print(f"Output file: {OUTPUT_FILE}")
        
        print(f"\nFirst 30 records:")
        print(df.head(30).to_string(index=False))
        
    else:
        print("\n" + "=" * 60)
        print("No data extracted. Check PDF structure.")
        print("=" * 60)


if __name__ == "__main__":
    main()
