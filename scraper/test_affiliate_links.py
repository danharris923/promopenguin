#!/usr/bin/env python3
"""
Test affiliate link rewriting with real examples
"""

from savingsguru_scraper import SavingsGuruScraper

def test_affiliate_rewriting():
    """Test the affiliate link rewriting with various URL formats"""
    scraper = SavingsGuruScraper(
        credentials_file='../../google_service_account.json',
        spreadsheet_id='1jkFjKFyOtv5zGw-l7ZF7H1i0e4MunSj3dP2bX7oA3zg'
    )
    
    # Test URLs with various formats
    test_urls = [
        # Bad current format from deals.json
        "https://www.amazon.ca/?_encoding=UTF8&#038;camp=15121&#038;creative=390961&#038;linkCode=ur2&#038;tag=saviguru-20",
        
        # Proper product URLs
        "https://www.amazon.com/dp/B08N5WRWNW?ref=sr_1_1",
        "https://www.amazon.ca/VASAGLE-Bakers-Rack-Power-Outlet/dp/B07ZPKN6XR/",
        "https://amazon.com/gp/product/B08N5LNQCX?keywords=pretzel+crisps",
        "https://www.amazon.com/OREO-Cakesters-Soft-Snack-Cakes/dp/B07FZ8S74R?tag=wrongtag-20",
        
        # Non-Amazon URL
        "https://walmart.com/some-product"
    ]
    
    print("Testing Affiliate Link Rewriting")
    print(f"Target tag: {scraper.affiliate_tag}\n")
    
    for url in test_urls:
        rewritten = scraper.rewrite_affiliate_link(url)
        print(f"Original:  {url}")
        print(f"Rewritten: {rewritten}")
        print("-" * 80)

if __name__ == "__main__":
    test_affiliate_rewriting()