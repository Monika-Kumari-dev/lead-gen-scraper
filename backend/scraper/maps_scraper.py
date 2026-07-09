"""
Selenium scraper for Google Maps listings.

Maps needs a real browser session (JS-rendered results, infinite scroll),
which is why this uses Selenium instead of BeautifulSoup - unlike the
directory sites, which are static HTML (see directory_scraper.py).
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from scraper.rate_limiter import RateLimiter
from scraper.config import MAPS_CATEGORIES, REGIONS


def build_driver(headless: bool = True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1280,900")

    # webdriver-manager downloads/matches the right ChromeDriver version
    # automatically - no manual driver installs or PATH setup needed.
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def search_maps(query: str, region: str, limiter: RateLimiter, driver=None):
    """
    Search Google Maps for `query` in `region` and return a list of
    raw lead dicts. Caller is responsible for saving to DB.

    NOTE: stub - fill in actual scraping logic (search box input,
    scrolling results panel, extracting each listing's name/address/
    website/phone) once you're ready to build this piece.
    """
    owns_driver = driver is None
    if owns_driver:
        driver = build_driver()

    results = []
    try:
        limiter.wait()
        search_query = f"{query} {region}"
        driver.get(f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}")

        # TODO: wait for results panel, scroll to load more listings,
        # then extract each listing card.
        # for card in driver.find_elements(By.CSS_SELECTOR, "..."):
        #     limiter.wait()
        #     results.append({
        #         "company_name": ...,
        #         "address": ...,
        #         "website": ...,
        #         "phone": ...,
        #         "source": "google_maps",
        #         "source_url": driver.current_url,
        #         "region": region,
        #     })

    finally:
        if owns_driver:
            driver.quit()

    return results


def run_maps_scrape(industries=None, regions=None):
    """Loop over categories x regions and collect all leads."""
    regions = regions or REGIONS
    limiter = RateLimiter()
    driver = build_driver()

    all_leads = []
    try:
        for region in regions:
            for query in MAPS_CATEGORIES:
                leads = search_maps(query, region, limiter, driver=driver)
                all_leads.extend(leads)
    finally:
        driver.quit()

    return all_leads
