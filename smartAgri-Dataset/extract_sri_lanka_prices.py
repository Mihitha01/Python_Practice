import pdfplumber
import pandas as pd
import re
import os
import glob

# ==========================================
# CONFIGURATION
# ==========================================
PDF_FOLDER = 'price_pdfs_2025_01'
OUTPUT_FILE = 'vegetable_prices_dataset.csv'

def extract_date_from_text(text):
    """
    Extracts the date from the PDF text.
    Looks for patterns like "12 December 2025"
    """
    # Pattern: Day Month Year (e.g., 12 December 2025)
    match = re.search(r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', text, re.IGNORECASE)
    if match:
        return match.group(0)
    return "Unknown Date"

def extract_products_from_text(text, filename):
    """
    Extracts product price data from the PDF text using pattern matching.
    Looks for product names (Beans, Carrot, Cabbage, Lime, Salaya, Fish, etc.)
    followed by their market location and prices.
    """
    products = []
    
    if not text:
        return products
    
    # Extract date from text
    report_date = extract_date_from_text(text)
    
    # Known product keywords to look for
    product_keywords = ['beans', 'carrot', 'cabbage', 'lime', 'onion', 'potato', 'salaya', 
                        'fish', 'garlic', 'ginger', 'radish', 'beetroot', 'brinjal']
    
    # Market locations
    markets = ['pettah', 'dambulla', 'peliyagoda', 'negombo', 'narahenpita', 'colombo']
    
    # Split text into lines
    lines = text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        line_lower = line.lower()
        
        # Skip empty lines, headers, and categories
        if not line or len(line) < 3:
            i += 1
            continue
        
        # Check if line contains a product name
        found_product = None
        for product in product_keywords:
            if product in line_lower and line_lower not in ['vegetables', 'fruits', 'fish', 'other', 'rice', 'meat']:
                found_product = product.capitalize()
                break
        
        if found_product:
            # This line starts a product section
            # Now collect the price data from subsequent lines
            market_prices = {}
            
            # Look ahead for market locations and prices
            for j in range(i+1, min(i+20, len(lines))):
                next_line = lines[j].strip()
                next_line_lower = next_line.lower()
                
                # Stop if we hit another product or category
                if any(prod in next_line_lower for prod in product_keywords) and next_line_lower not in line_lower:
                    if any(kw in next_line_lower for kw in ['vegetables', 'fruits', 'fish', 'meat', 'dairy']):
                        break
                
                # Stop if we hit a spaced-out header
                if 'voN' in next_line or 'ceD' in next_line:
                    continue
                
                # Look for market:price pattern like "Dambulla : 980.00 905.00"
                market_price_pattern = r'([A-Za-z]+)\s*:\s*(\d+\.\d{2})\s+(\d+\.\d{2})'
                matches = re.findall(market_price_pattern, next_line)
                
                if matches:
                    for market, price_yesterday, price_today in matches:
                        market_clean = market.strip()
                        market_prices[market_clean] = {
                            'Price Yesterday': float(price_yesterday),
                            'Price Today': float(price_today)
                        }
                
                # Also look for standalone prices
                if not matches:
                    prices = re.findall(r'(\d+\.\d{2})', next_line)
                    if len(prices) >= 2:
                        # Check if previous line has market name
                        if i > 0:
                            prev_line = lines[i-1].strip().lower()
                            for market in markets:
                                if market in prev_line:
                                    market_prices[market.capitalize()] = {
                                        'Price Yesterday': float(prices[0]),
                                        'Price Today': float(prices[1])
                                    }
                                    break
            
            # Create product entries for each market
            if market_prices:
                for market, prices in market_prices.items():
                    product_data = {
                        "Date": report_date,
                        "Product Name": found_product,
                        "Market": market,
                        "Unit": "kg",
                        "Price Today": prices['Price Today'],
                        "Source File": filename
                    }
                    products.append(product_data)
                
                i = j
            else:
                i += 1
        else:
            i += 1
    
    return products

def process_pdfs():
    all_data = []
    pdf_files = sorted(glob.glob(os.path.join(PDF_FOLDER, "*.pdf")))
    
    print(f"Found {len(pdf_files)} PDF files.")

    for filepath in pdf_files:
        filename = os.path.basename(filepath)
        print(f"Processing {filename}...")
        
        try:
            with pdfplumber.open(filepath) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract all text from page
                    text = page.extract_text()
                    
                    if text:
                        # Extract products from text
                        products = extract_products_from_text(text, filename)
                        all_data.extend(products)

        except Exception as e:
            print(f"Error reading {filename}: {e}")


    # ==========================================
    # SAVE
    # ==========================================
    if all_data:
        df = pd.DataFrame(all_data)
        
        # Create output CSV with columns exactly like the table screenshot
        output_columns = ["Date", "Product Name", "Market", "Unit", "Price Today", "Source File"]
        # Keep only columns that exist in dataframe
        output_cols = [col for col in output_columns if col in df.columns]
        output_df = df[output_cols]
        
        # Sort by date and product name
        output_df = output_df.sort_values(['Date', 'Product Name']).reset_index(drop=True)
        
        output_df.to_csv(OUTPUT_FILE, index=False)
        print(f"\nSuccess! Extracted {len(output_df)} product entries.")
        print(f"Saved to {OUTPUT_FILE}")
        print("\nFirst 20 entries:")
        print(output_df.head(20).to_string())
    else:
        print("No data extracted. Check if the PDF structure is as expected.")

if __name__ == "__main__":
    process_pdfs()