#!/usr/bin/env python3
"""
Quick script to fetch 100 posts using REST API
"""

from rest_api_scraper import RestApiScraper

def main():
    print("Fetching 100 latest posts from SavingsGuru REST API...")
    
    scraper = RestApiScraper()
    deals = scraper.generate_deals_json(100)
    
    print(f"\nDone! Generated {len(deals)} deals")
    print("The site now shows the latest 100 posts instead of just 22!")

if __name__ == "__main__":
    main()