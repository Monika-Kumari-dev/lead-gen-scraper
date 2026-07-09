"""
BeautifulSoup scraper for static directory pages (IndiaMART, Europages, etc.)

These pages don't need JS rendering, so plain requests + BeautifulSoup is
enough - no reason to spin up a full browser session for them.
"""

import requests
from bs4 import BeautifulSoup

from scraper.rate_limiter import RateLimiter
from scraper.config import DIRECTORY_SOURCES

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def scrape_directory_page(url: str, limiter: RateLimiter):
    """
    Fetch and parse a single directory listing page.

    NOTE: stub - selectors depend on each directory site's HTML structure.
    Build one parser function per directory (they won't share a layout).
    """
    limiter.wait()
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # TODO: replace with real selectors once a specific directory is chosen.
    # Example shape of what each parser should return:
    lead = {
        "company_name": None,   # soup.select_one("...").get_text(strip=True)
        "website": None,
        "email": None,
        "phone": None,
        "address": None,
        "source": "directory",
        "source_url": url,
    }
    return lead


def run_directory_scrape(region: str):
    """Loop over configured directory sources for a region."""
    limiter = RateLimiter()
    sources = DIRECTORY_SOURCES.get(region, [])

    all_leads = []
    for source in sources:
        listing_url = source["url"] + source.get("category_path", "")
        lead = scrape_directory_page(listing_url, limiter)
        lead["region"] = region
        all_leads.append(lead)

    return all_leads
