#!/usr/bin/env python3
"""
Test affiliate tag rewriting
"""

from savingsguru_scraper import SavingsGuruScraper

def test_rewrite():
    """Test the affiliate link rewriting"""
    scraper = SavingsGuruScraper(
        credentials_file='../../google_service_account.json',
        spreadsheet_id='1jkFjKFyOtv5zGw-l7ZF7H1i0e4MunSj3dP2bX7oA3zg'
    )
    
    # Test URLs with wrong tags
    test_urls = [
        "https://www.amazon.ca/?_encoding=UTF8&camp=15121&creative=390961&linkCode=ur2&tag=saviguru-20",
        "https://www.amazon.com/dp/B08N5WRWNW?tag=wrongtag-20",
        "https://www.amazon.ca/dp/B07ZPKN6XR?tag=saviguru-20&ref=sr_1_1",
        "https://www.amazon.com/gp/product/B08N5LNQCX",
        "https://amazon.ca/Some-Product/dp/B07FZ8S74R/ref=sr_1_1?tag=oldtag-20"
    ]
    
    print(f"Affiliate tag is set to: {scraper.affiliate_tag}\n")
    
    for url in test_urls:
        rewritten = scraper.rewrite_affiliate_link(url)
        print(f"Original: {url}")
        print(f"Rewritten: {rewritten}")
        print("-" * 80)

if __name__ == "__main__":
    test_rewrite()