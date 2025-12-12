import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

BASE = "https://www.cbsl.gov.lk"
YEAR = 2025
MONTH = 1   # January is 1

URL = f"https://www.cbsl.gov.lk/en/statistics/economic-indicators/price-report?year={YEAR}&month={MONTH}"

session = requests.Session()
output_folder = f"price_pdfs_{YEAR}_{MONTH:02d}"
os.makedirs(output_folder, exist_ok=True)

resp = session.get(URL)
soup = BeautifulSoup(resp.text, "html.parser")

# find direct PDF links
pdf_links = []
for a in soup.select("a"):
    href = a.get("href")
    
    # Look for PDF links with price report format
    if href and href.endswith(".pdf") and "price_report" in href.lower():
        if not href.startswith("http"):
            href = BASE + href
        pdf_links.append(href)

pdf_links = list(set(pdf_links))

print(f"Found {len(pdf_links)} reports for {YEAR}-{MONTH:02d}")

# download each PDF
for pdf_url in tqdm(pdf_links):
    try:
        filename = pdf_url.split("/")[-1]
        save_path = os.path.join(output_folder, filename)

        if not os.path.exists(save_path):
            r = session.get(pdf_url)
            r.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(r.content)
    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")
        continue

print("Download complete!")
