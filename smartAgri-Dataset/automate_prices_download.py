import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

BASE = "https://www.cbsl.gov.lk"
PAGE_URL = "https://www.cbsl.gov.lk/en/statistics/economic-indicators/price-report?page={page}"

session = requests.Session()

# Create main output folder
output_folder = "new_price_pdf"
os.makedirs(output_folder, exist_ok=True)

total_downloaded = 0
total_skipped = 0
all_pdf_links = set()

# First, collect all PDF links from all pages
print("Scanning all pages for PDF links...")
page = 0
empty_pages = 0

while empty_pages < 3:  # Stop after 3 consecutive empty pages
    url = PAGE_URL.format(page=page)
    try:
        resp = session.get(url, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Find all price report PDF links
        found = 0
        for a in soup.select("a"):
            href = a.get("href")
            if href and "price_report" in href and ".pdf" in href:
                if not href.startswith("http"):
                    href = BASE + href
                if href not in all_pdf_links:
                    all_pdf_links.add(href)
                    found += 1
        
        if found > 0:
            print(f"Page {page}: Found {found} new PDFs (Total: {len(all_pdf_links)})")
            empty_pages = 0
        else:
            empty_pages += 1
            print(f"Page {page}: No new PDFs found")
        
        page += 1
        
    except Exception as e:
        print(f"Error on page {page}: {e}")
        page += 1
        continue

print(f"\nTotal unique PDFs found: {len(all_pdf_links)}")
print("\nDownloading PDFs...")

# Download all PDFs
for pdf_url in tqdm(sorted(all_pdf_links), desc="Downloading"):
    try:
        filename = pdf_url.split("/")[-1]
        save_path = os.path.join(output_folder, filename)
        
        if os.path.exists(save_path):
            total_skipped += 1
            continue
        
        r = session.get(pdf_url, timeout=60)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        total_downloaded += 1
        
    except Exception as e:
        print(f"\nError downloading {pdf_url}: {e}")
        continue

print(f"\n{'='*50}")
print(f"Download complete!")
print(f"Total downloaded: {total_downloaded}")
print(f"Total skipped (already existed): {total_skipped}")
