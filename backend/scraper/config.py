"""
Scraper configuration: target industries, regions, and rate-limiting.

Fill in SOURCE_LIST once it's locked with Ashish. Keeping it here (not
hardcoded in the scraper) means adding/changing sources doesn't touch
scraper logic - just this file.
"""

# --- Target scope (per Ashish's email) ---
INDUSTRIES = [
    "pharma_manufacturing",
    "general_manufacturing",
]

REGIONS = [
    "India",
    "Southeast Asia",
    "Middle East",
    "Europe",
]

# --- Google Maps search categories ---
# One entry per (industry, query) - queries run per region.
MAPS_CATEGORIES = [
    "pharmaceutical manufacturer",
    "pharmaceutical company",
    "industrial manufacturer",
    "manufacturing company",
    "chemical manufacturer",
]

# --- Directory sites (fill in once locked) ---
# Example structure - add real category paths as you research each one.
DIRECTORY_SOURCES = {
    "India": [
        {"name": "IndiaMART", "url": "https://www.indiamart.com/", "category_path": ""},
        {"name": "TradeIndia", "url": "https://www.tradeindia.com/", "category_path": ""},
    ],
    "Southeast Asia": [
        {"name": "Kompass Asia", "url": "https://asia.kompass.com/", "category_path": ""},
    ],
    "Middle East": [
        {"name": "Kompass Middle East", "url": "https://www.kompass.com/", "category_path": ""},
    ],
    "Europe": [
        {"name": "Europages", "url": "https://www.europages.com/", "category_path": ""},
        {"name": "Kompass Europe", "url": "https://www.kompass.com/", "category_path": ""},
    ],
}

# --- Rate limiting (per Ashish's note: Google Maps + directories will
# block/rate-limit at volume if hit continuously) ---
MIN_DELAY_SECONDS = 3
MAX_DELAY_SECONDS = 8

# Rotate/limit requests per "session" before pausing longer, to avoid
# hammering the same IP continuously.
REQUESTS_BEFORE_COOLDOWN = 25
COOLDOWN_SECONDS = 60
