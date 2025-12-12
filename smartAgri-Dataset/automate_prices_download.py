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

# find links to each daily report page
report_links = []
for a in soup.select("a"):
    href = a.get("href")
    text = a.text.strip().lower()
    
    # Look for link text like "Daily Price Report - ..."
    if href and "daily-price-report" in href.lower():
        if href.startswith("/"):
            href = BASE + href
        report_links.append(href)

report_links = list(set(report_links))

print(f"Found {len(report_links)} reports for {YEAR}-{MONTH:02d}")

# download each PDF
for page_url in tqdm(report_links):
    page = session.get(page_url)
    page_soup = BeautifulSoup(page.text, "html.parser")

    pdf_link = page_soup.find("a", href=lambda x: x and x.endswith(".pdf"))
    if pdf_link:
        pdf_url = pdf_link["href"]
        if not pdf_url.startswith("http"):
            pdf_url = BASE + pdf_url

        filename = pdf_url.split("/")[-1]
        save_path = os.path.join(output_folder, filename)

        if not os.path.exists(save_path):
            r = session.get(pdf_url)
            with open(save_path, "wb") as f:
                f.write(r.content)

print("Download complete!")
