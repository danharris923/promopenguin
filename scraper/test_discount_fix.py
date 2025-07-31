#!/usr/bin/env python3
"""
Test the fixed discount scraping
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to find .env
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env file
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Load credentials from file
if 'GOOGLE_CREDS_FILE' in os.environ:
    creds_path = Path(__file__).parent.parent / os.environ['GOOGLE_CREDS_FILE']
    if creds_path.exists():
        with open(creds_path) as f:
            os.environ['GOOGLE_SHEETS_CREDS'] = f.read()

from scraper_env import SavingsGuruScraperEnv

def test_discount_scraping():
    scraper = SavingsGuruScraperEnv()
    
    test_urls = [
        "https://www.amazon.ca/dp/B09YZZML4W",  # Should show 7%
        "https://www.amazon.ca/dp/B07ZVXK5K9",  # Should show 15% or 20%
        "https://www.amazon.ca/dp/B08T7DSZYD",  # Should show 22% or 26%
    ]
    
    for url in test_urls:
        print(f"\\nTesting: {url}")
        discount = scraper.scrape_amazon_discount(url)
        print(f"Result: {discount}% discount")

if __name__ == "__main__":
    test_discount_scraping()