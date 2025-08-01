#!/usr/bin/env python3
"""
Test Amazon description scraping on a specific product
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

def test_description_scraping():
    """Test description scraping on specific Amazon URLs"""
    
    # Test URLs from our deals.json
    test_urls = [
        "https://www.amazon.ca/dp/B0DLB2Y432?asc_item-id=amzn1.ideas.3S99BPJVAJDZI&th=1&psc=1&linkCode=sl1&tag=savingsgurucc-20&linkId=e3df9bfb76a86c89073032b58f997780&language=en_CA&ref_=as_li_ss_tl",  # Tank tops
        "https://www.amazon.ca/dp/B07ZVXK5K9?asc_item-id=amzn1.ideas.3S99BPJVAJDZI&linkCode=sl1&tag=savingsgurucc-20&linkId=6dc085c27e89e3bf54670b713e4f509a&language=en_CA&ref_=as_li_ss_tl",  # e.l.f. kit
        "https://www.amazon.ca/dp/B0CF8WRDJF?asc_item-id=amzn1.ideas.3ONGK4HFHBU4O&th=1&psc=1&linkCode=sl1&tag=savingsgurucc-20&linkId=076c0b1f6554420707141c53712a6156&language=en_CA&ref_=as_li_ss_tl"  # Leggings
    ]
    
    scraper = SavingsGuruScraperEnv()
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n--- Testing URL {i} ---")
        print(f"URL: {url[:80]}...")
        
        description = scraper.scrape_amazon_description(url)
        if description:
            # Handle Unicode for display
            safe_desc = description.encode('ascii', 'ignore').decode('ascii')
            print(f"Success! Description: {safe_desc}")
        else:
            print("No description found")

if __name__ == "__main__":
    test_description_scraping()