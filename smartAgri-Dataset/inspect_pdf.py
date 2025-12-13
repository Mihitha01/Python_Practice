import pdfplumber

pdf = pdfplumber.open('price_pdfs_2025_01/price_report_20251212_e.pdf')
tables = pdf.pages[0].extract_tables()

for i, table in enumerate(tables):
    print(f"\n===Table {i} ({len(table)} rows)===")
    for j, row in enumerate(table):
        print(f"Row {j}: {row}")

pdf.close()
