"""Debug script to test price extraction"""
import pdfplumber
import re
import os

def parse_price(val_str):
    """Parse price string to float"""
    if not val_str:
        return None
    try:
        cleaned = val_str.replace(',', '').strip()
        val = float(cleaned)
        if 0 < val < 50000:
            return val
    except:
        pass
    return None


# Test with old format
old_pdf = 'd:/Python/smartAgri-Dataset/new_price_pdf/price_report_20170215e.pdf'
print("=== TESTING OLD FORMAT ===")

if os.path.exists(old_pdf):
    with pdfplumber.open(old_pdf) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        lines = text.split('\n')
        
        for line in lines:
            if 'Beans' in line and 'Rs./Kg' in line:
                print(f"\nOriginal line:\n{line}")
                
                # Clean the line
                cleaned = re.sub(r'(\d)\s+(\d+\.\d+)', r'\1\2', line)
                cleaned = re.sub(r'(\d)\s+,', r'\1,', cleaned)
                cleaned = re.sub(r',\s+(\d)', r',\1', cleaned)
                print(f"\nCleaned line:\n{cleaned}")
                
                # Extract numbers
                all_numbers = re.findall(r'[\d,]+\.\d+', cleaned)
                print(f"\nExtracted numbers ({len(all_numbers)}):")
                for i, num in enumerate(all_numbers):
                    print(f"  [{i}]: {num}")
                
                # Parse interpretation  
                print(f"\nInterpretation:")
                print(f"  Pettah_Wholesale (idx 1 = Today): {all_numbers[1] if len(all_numbers) > 1 else 'N/A'}")
                print(f"  Dambulla_Wholesale (idx 3 = Today): {all_numbers[3] if len(all_numbers) > 3 else 'N/A'}")
                break

# Test with new format
print("\n" + "="*50)
print("=== TESTING NEW FORMAT ===")

# Find a new format PDF
new_pdf_dir = 'd:/Python/smartAgri-Dataset/new_price_pdf/'
for fname in sorted(os.listdir(new_pdf_dir)):
    if '2024' in fname and fname.endswith('.pdf'):
        new_pdf = os.path.join(new_pdf_dir, fname)
        break

print(f"Using: {new_pdf}")

if os.path.exists(new_pdf):
    with pdfplumber.open(new_pdf) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if 'Beans' in text:
                lines = text.split('\n')
                for line in lines:
                    if 'Beans' in line and ('Rs.' in line or re.search(r'\d+\.\d+', line)):
                        print(f"\nOriginal line:\n{line}")
                        
                        # Clean the line
                        cleaned = re.sub(r'(\d)\s+(\d+\.\d+)', r'\1\2', line)
                        cleaned = re.sub(r'(\d)\s+,', r'\1,', cleaned)
                        cleaned = re.sub(r',\s+(\d)', r',\1', cleaned)
                        print(f"\nCleaned line:\n{cleaned}")
                        
                        # Extract numbers
                        all_numbers = re.findall(r'[\d,]+\.\d+', cleaned)
                        print(f"\nExtracted numbers ({len(all_numbers)}):")
                        for i, num in enumerate(all_numbers):
                            print(f"  [{i}]: {num}")
                        
                        if len(all_numbers) >= 10:
                            print(f"\nInterpretation (10 numbers - Yesterday/Today for 5 markets):")
                            print(f"  Pettah_Wholesale (idx 1): {all_numbers[1]}")
                            print(f"  Dambulla_Wholesale (idx 3): {all_numbers[3]}")
                            print(f"  Pettah_Retail (idx 5): {all_numbers[5]}")
                            print(f"  Dambulla_Retail (idx 7): {all_numbers[7]}")
                            print(f"  Narahenpita_Retail (idx 9): {all_numbers[9]}")
                        break
                break

# Now let's check the actual CSV output
print("\n" + "="*50)
print("=== CHECKING CSV OUTPUT ===")

csv_path = 'd:/Python/smartAgri-Dataset/automate_pdf/vegetable_prices_clean.csv'
if os.path.exists(csv_path):
    import pandas as pd
    df = pd.read_csv(csv_path)
    
    # Check for suspicious values (prices with many digits)
    print(f"\nLooking for suspicious price values (> 1000 for wholesale)...")
    suspicious = df[df['Pettah_Wholesale'] > 1000]
    if len(suspicious) > 0:
        print(f"Found {len(suspicious)} records with Pettah_Wholesale > 1000:")
        print(suspicious[['Date', 'Product', 'Pettah_Wholesale', 'Dambulla_Wholesale']].head(20))
    
    # Check sample from different years
    print(f"\nSample from 2017:")
    sample_2017 = df[df['Date'].str.startswith('2017')].head(5)
    print(sample_2017[['Date', 'Product', 'Pettah_Wholesale', 'Dambulla_Wholesale']])
    
    print(f"\nSample from 2024:")
    sample_2024 = df[df['Date'].str.startswith('2024')].head(5)
    print(sample_2024[['Date', 'Product', 'Pettah_Wholesale', 'Dambulla_Wholesale', 'Pettah_Retail']])
