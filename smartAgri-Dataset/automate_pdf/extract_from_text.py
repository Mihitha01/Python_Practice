"""
Extract prices from PDF text (not table) for accurate Dambulla data
"""

import pdfplumber
import pandas as pd
import re
import os
import glob

def extract_prices_from_text(pdf_path):
    """Extract prices directly from page text"""
    data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        # Get date from page 1
        text_p1 = pdf.pages[0].extract_text()
        date_match = re.search(
            r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})',
            text_p1,
            re.IGNORECASE
        )
        report_date = date_match.group(0) if date_match else "Unknown"
        
        # Get prices from page 2
        text_p2 = pdf.pages[1].extract_text()
        
        # Extract VEGETABLES section
        veg_start = text_p2.find('V E G E T A B L E S')
        other_start = text_p2.find('O T H E R')
        veg_text = text_p2[veg_start:other_start]
        
        # Extract OTHER section
        fruits_start = text_p2.find('F R U I T S')
        if fruits_start == -1:
            fruits_start = len(text_p2)
        other_text = text_p2[other_start:fruits_start]
        
        # Process each section
        for section_text in [veg_text, other_text]:
            lines = section_text.split('\n')[1:]  # Skip section header
            
            for line in lines:
                line = line.strip()
                if not line or 'E G E T A B L E S' in line or 'O T H E R' in line or 'F R U I T S' in line:
                    continue
                
                # Parse: "ProductName Rs./kg n.a. price1 n.a. price2 ..."
                match = re.match(r'^([A-Za-z\s\(\)]+?)\s+Rs\.\/kg\s+(.*)', line)
                if not match:
                    continue
                    
                product = match.group(1).strip()
                prices_str = match.group(2)
                
                # Extract all prices: look for "n.a. " followed by numbers with optional spaces/commas
                prices = []
                for price_match in re.finditer(r'n\.a\.\s+([\d\s,\.]+?)(?=\s+n\.a\.|$)', prices_str):
                    price_str = price_match.group(1).strip().replace(' ', '').replace(',', '')
                    try:
                        price = float(price_str)
                        prices.append(price)
                    except:
                        pass
                
                # Map to markets: [Pettah WS, Dambulla WS, Pettah Retail, Dambulla Retail, Narahenpita Retail]
                if len(prices) >= 5:
                    data.append({
                        'Date': report_date,
                        'Product': product,
                        'Unit': 'Rs./kg',
                        'Pettah (Wholesale)': prices[0],
                        'Dambulla (Wholesale)': prices[1],
                        'Pettah (Retail)': prices[2],
                        'Dambulla (Retail)': prices[3],
                        'Narahenpita (Retail)': prices[4]
                    })
    
    return data

# Process all PDFs
print("="*60)
print("Extracting prices from PDF text...")
print("="*60)

all_data = []
pdf_files = sorted(glob.glob('price_pdfs_2025_01/*.pdf'))
print(f"Found {len(pdf_files)} PDFs\n")

for idx, pdf_file in enumerate(pdf_files, 1):
    filename = os.path.basename(pdf_file)
    data = extract_prices_from_text(pdf_file)
    all_data.extend(data)
    print(f"[{idx}/{len(pdf_files)}] {filename:40} OK {len(data):3} records")

# Create DataFrame
df_new = pd.DataFrame(all_data)

print("\n" + "="*60)
print(f"Total records extracted: {len(df_new)}")
print(f"Unique dates: {len(df_new['Date'].unique())}")
print(f"Unique products: {len(df_new['Product'].unique())}")

# Save
df_new.to_csv('extracted_prices.csv', index=False)
print(f"\nSaved to: extracted_prices.csv")

print("\n" + "="*60)
print("Sample data verification:")
print("="*60)
print("\nBeans (01 Dec):")
print(df_new[(df_new['Product'] == 'Beans') & (df_new['Date'] == '01 December 2025')])

print("\nCarrot (01 Dec):")
print(df_new[(df_new['Product'] == 'Carrot') & (df_new['Date'] == '01 December 2025')])
