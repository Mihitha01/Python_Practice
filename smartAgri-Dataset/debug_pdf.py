import pdfplumber

pdf = pdfplumber.open('price_pdfs_2025_01/price_report_20251212_e.pdf')
page = pdf.pages[0]
text = page.extract_text()

# Print first 3000 characters to see structure
print("=== FULL TEXT FROM PAGE 1 ===\n")
print(text[:3000])
print("\n\n=== LOOKING FOR DATE ===")
import re
date_match = re.search(r'\d{1,2}\s+\w+\s+\d{4}', text)
if date_match:
    print(f"Found date: {date_match.group()}")

print("\n=== LOOKING FOR PRODUCT NAMES ===")
# Look for patterns like "Beans" or "Carrot" followed by prices
lines = text.split('\n')
for i, line in enumerate(lines[:100]):
    if line.strip() and len(line.strip()) > 3 and len(line.strip()) < 50:
        print(f"Line {i}: {repr(line.strip()[:80])}")

pdf.close()
