# 🌍 Wikipedia Country Scraper

A clean, dependency-light Python scraper that collects the names and Wikipedia URLs of every country in the world from [Wikipedia's List of Countries](https://en.wikipedia.org/wiki/List_of_countries).

---

## Why Wikipedia?

Most scraping targets fight back — rate limits, CAPTCHAs, bot detection, JavaScript rendering. Wikipedia has none of that. It's:

- **Open** — no login, no API key required
- **Stable** — consistent HTML structure across pages
- **Reliable** — near 100% uptime
- **Respectful** — explicitly allows scraping for non-commercial use

This makes it one of the few sources where you can achieve a true **100% success rate** on scrape runs.

---

## Output

Produces a single JSON file at `data/countries/countries.json`:

```json
{
  "Afghanistan": "https://en.wikipedia.org/wiki/Afghanistan",
  "Albania":     "https://en.wikipedia.org/wiki/Albania",
  "Algeria":     "https://en.wikipedia.org/wiki/Algeria",
  ...
}
```

~195 countries are returned, matching the UN-recognised sovereign states list.

---

## Project Structure

```
.
├── scraper.py                   # Main scraper script
├── README.md                    # This file
└── data/
    └── countries/
        └── countries.json       # Scraped output
```

---

## Setup

### 1. Clone / download the project

```bash
git clone https://github.com/yourname/wiki-country-scraper
cd wiki-country-scraper
```

### 2. Install dependencies

```bash
pip install requests beautifulsoup4 lxml
```

### 3. Run

```bash
python scraper.py
```

That's it. The JSON file will appear at `data/countries/countries.json`.

---

## How It Works

1. Sends a single `GET` request to `https://en.wikipedia.org/wiki/List_of_countries`
2. Parses the HTML with BeautifulSoup using the `lxml` parser
3. Finds all `<a href>` tags within the main content div
4. Filters to only internal Wikipedia article links (skipping `File:`, `Category:`, `Help:`, etc.)
5. Saves the results as a `{ name: url }` JSON dictionary

---

## Configuration

All configurable values live at the top of `scraper.py`:

| Variable | Default | Description |
|---|---|---|
| `ROOT_URL` | `https://en.wikipedia.org` | Wikipedia base URL |
| `LIST_URL` | `.../wiki/List_of_countries` | Page to scrape |
| `OUTPUT_FILE` | `data/countries/countries.json` | Output path |
| `HEADERS` | Mozilla user-agent string | Request headers |

---

## Extending the Scraper

Want to scrape a different Wikipedia list? Just swap `LIST_URL`:

```python
# Capitals of the world
LIST_URL = "https://en.wikipedia.org/wiki/List_of_national_capitals"

# World languages
LIST_URL = "https://en.wikipedia.org/wiki/List_of_languages_by_number_of_native_speakers"
```

The rest of the scraper works without modification.

---

## Requirements

- Python 3.8+
- `requests`
- `beautifulsoup4`
- `lxml`

MIT — free to use, modify, and distribute.
