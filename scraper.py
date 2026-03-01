import requests
from bs4 import BeautifulSoup
import json
import os
import time

# ── Configuration ─────────────────────────────────────────────────────────────

ROOT_URL    = "https://en.wikipedia.org"
LIST_URL    = f"{ROOT_URL}/wiki/List_of_countries"
OUTPUT_PATH = "data/countries"
OUTPUT_FILE = f"{OUTPUT_PATH}/countries.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; wiki-country-scraper/1.0)"
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def save_json(filepath: str, data: dict, description: str = "records") -> None:
    """Persist a dictionary to a JSON file, creating directories as needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[✓] Saved {len(data)} {description} → '{filepath}'")


# ── Core scraper ──────────────────────────────────────────────────────────────

def scrape_countries() -> dict:
    """
    Fetch Wikipedia's List of Countries and extract all country names + URLs.

    Returns:
        dict: { "Country Name": "https://en.wikipedia.org/wiki/Country_Name" }
    """
    print(f">> Scraping: {LIST_URL}\n")

    response = requests.get(LIST_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    content_div = soup.find("div", {"id": "mw-content-text"})

    if not content_div:
        raise RuntimeError("Could not locate main content div — page structure may have changed.")

    data = {}
    links = content_div.find_all("a", href=True)

    for link in links:
        href = link.get("href", "")
        name = link.get_text(strip=True)

        # Keep only internal article links; skip meta pages (File:, Category:, etc.)
        if (
            href.startswith("/wiki/")
            and ":" not in href
            and name
            and len(name) > 1
        ):
            data[name] = ROOT_URL + href

    return data


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    start = time.time()

    countries = scrape_countries()
    save_json(OUTPUT_FILE, countries, description="countries")

    elapsed = time.time() - start
    print(f"\n── Summary ───────────────────────────────")
    print(f"  Total countries scraped : {len(countries)}")
    print(f"  Output file             : {OUTPUT_FILE}")
    print(f"  Time elapsed            : {elapsed:.2f}s")
    print(f"──────────────────────────────────────────")
    print(f"\nSample entries:")
    for name, url in list(countries.items())[:5]:
        print(f"  {name:30s} → {url}")
