import pdfplumber
import pandas as pd
import re
import os
import glob

PDF_FOLDER = 'price_pdfs_2025_01'

def extract_date_from_text(text):
    """Extracts the date from the PDF text."""
    match = re.search(r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', text, re.IGNORECASE)
    if match:
        return match.group(0)
    return "Unknown Date"

def extract_products_from_text(text, filename):
    """Extracts product price data from the PDF text."""
    products = []
    
    if not text:
        return products
    
    report_date = extract_date_from_text(text)
    
    product_keywords = ['beans', 'carrot', 'cabbage', 'lime', 'onion', 'potato', 'salaya', 
                        'fish', 'garlic', 'ginger', 'radish', 'beetroot', 'brinjal']
    
    markets = ['pettah', 'dambulla', 'peliyagoda', 'negombo', 'narahenpita', 'colombo']
    
    lines = text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        line_lower = line.lower()
        
        if not line or len(line) < 3:
            i += 1
            continue
        
        found_product = None
        for product in product_keywords:
            if product in line_lower and line_lower not in ['vegetables', 'fruits', 'fish', 'other', 'rice', 'meat']:
                found_product = product.capitalize()
                break
        
        if found_product:
            market_prices = {}
            
            for j in range(i+1, min(i+20, len(lines))):
                next_line = lines[j].strip()
                next_line_lower = next_line.lower()
                
                if any(prod in next_line_lower for prod in product_keywords) and next_line_lower not in line_lower:
                    if any(kw in next_line_lower for kw in ['vegetables', 'fruits', 'fish', 'meat', 'dairy']):
                        break
                
                if 'voN' in next_line or 'ceD' in next_line:
                    continue
                
                market_price_pattern = r'([A-Za-z]+)\s*:\s*(\d+\.\d{2})\s+(\d+\.\d{2})'
                matches = re.findall(market_price_pattern, next_line)
                
                if matches:
                    for market, price_yesterday, price_today in matches:
                        market_clean = market.strip()
                        market_prices[market_clean] = {
                            'Price Yesterday': float(price_yesterday),
                            'Price Today': float(price_today)
                        }
                
                if not matches:
                    prices = re.findall(r'(\d+\.\d{2})', next_line)
                    if len(prices) >= 2:
                        if i > 0:
                            prev_line = lines[i-1].strip().lower()
                            for market in markets:
                                if market in prev_line:
                                    market_prices[market.capitalize()] = {
                                        'Price Yesterday': float(prices[0]),
                                        'Price Today': float(prices[1])
                                    }
                                    break
            
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

# Test with one file
filepath = 'price_pdfs_2025_01/price_report_20251212_e.pdf'
with pdfplumber.open(filepath) as pdf:
    text = pdf.pages[0].extract_text()
    products = extract_products_from_text(text, os.path.basename(filepath))
    
print(f"Found {len(products)} products")
for p in products:
    print(p)
