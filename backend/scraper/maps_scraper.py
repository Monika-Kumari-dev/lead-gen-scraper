from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from scraper.rate_limiter import RateLimiter
from scraper.config import MAPS_CATEGORIES, REGIONS


def build_driver(headless: bool = True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1280,900")

    # Selenium 4.6+ has built-in driver management (Selenium Manager) -
    # it downloads and matches the right ChromeDriver automatically.
    # No webdriver-manager needed (its path resolution had a bug on Mac ARM).
    return webdriver.Chrome(options=options)


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
                try:
                    leads = search_maps(query, region, limiter, driver=driver)
                    all_leads.extend(leads)
                except Exception as e:
                    print(f"[maps_scraper] Skipped '{query}' in {region}: {e}")
                    continue
    finally:
        driver.quit()

    return all_leads
