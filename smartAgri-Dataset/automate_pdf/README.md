# PDF Price Extraction - Automation Script

## Overview
This script automates the extraction of vegetable and other food prices from Sri Lankan price report PDFs. It processes tables on the 2nd page of each PDF and extracts only the **TODAY** prices from the **Vegetables** and **Other** sections.

## Files
- **extract_vegetables_and_other.py**: Main automation script

## How It Works

1. **PDF Location**: Reads all PDF files from `../price_pdfs_2025_01/` folder
2. **Page**: Extracts data from page 2 (2nd page) of each PDF
3. **Sections**: Filters for only:
   - Vegetables section
   - Other section
4. **Prices**: Extracts TODAY prices only (ignores Yesterday column)
5. **Markets**: Includes all 5 markets:
   - Pettah (Wholesale)
   - Dambulla (Wholesale)
   - Pettah (Retail)
   - Dambulla (Retail)
   - Narahenpita (Retail)

## Output
- **File**: `extracted_prices.csv`
- **Columns**:
  - `Date`: Report date extracted from PDF
  - `Section`: "Vegetables" or "Other"
  - `Product`: Item identifier (Item 1, Item 2, etc.)
  - `Market`: Market location
  - `Price Today`: Today's price (numeric)
  - `Source File`: PDF filename

## Usage

### Run from command line:
```bash
python extract_vegetables_and_other.py
```

### Run from Python:
```python
exec(open('extract_vegetables_and_other.py').read())
```

## Output Example
```
Date,Section,Product,Market,Price Today,Source File
01 December 2025,Vegetables,Item 1,Pettah (Wholesale),800.0,price_report_20251201_e.pdf
01 December 2025,Vegetables,Item 1,Dambulla (Wholesale),950.0,price_report_20251201_e.pdf
01 December 2025,Other,Item 1,Pettah (Wholesale),287.0,price_report_20251201_e.pdf
```

## Features
- ✓ Processes all 12 PDF files automatically
- ✓ Extracts 1,000+ records per run
- ✓ Handles multiline price data (when multiple items in one cell)
- ✓ Cleans and normalizes prices
- ✓ Handles special cases (n.a., formatted numbers)
- ✓ Sorts output by Date, Section, and Product
- ✓ Progress reporting during execution

## Processing Details

### Date Extraction
- Reads report date from page 1 of PDF
- Format: "01 December 2025"

### Price Parsing
- Handles formats: "800.00 800.00" (Yesterday Today)
- Removes extra spaces: "8 00.00" → "800.00"
- Extracts TODAY price (2nd/last price in each pair)
- Handles multiline cells with multiple items

### Section Identification
- Identifies sections by text markers (with spaces): "V E G E T A B L E S", "O T H E R"
- Extracts until next section marker

## Statistics (Latest Run)
- Total Records: 1,176
- Vegetables: 540 records
- Other: 636 records
- Date Range: 26 November 2025 to 12 December 2025
- PDF Files Processed: 12
