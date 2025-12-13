import pdfplumber

pdf = pdfplumber.open('price_pdfs_2025_01/price_report_20251212_e.pdf')
page = pdf.pages[0]
text = page.extract_text()

print("=== FULL TEXT (First 5000 chars) ===\n")
print(text[:5000])

print("\n\n=== DATE EXTRACTION ===")
import re
# Look for date patterns
date_patterns = [
    r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})',
    r'(\d{1,2})\s+[A-Za-z]+\s+(\d{4})',
    r'(\d{2}/\d{2}/\d{4})'
]

for pattern in date_patterns:
    matches = re.findall(pattern, text)
    if matches:
        print(f"Pattern {pattern}: {matches[:3]}")

pdf.close()
