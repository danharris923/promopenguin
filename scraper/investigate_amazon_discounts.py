#!/usr/bin/env python3
"""
Investigate Amazon.ca discount elements using requests and BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup
import re

def investigate_amazon_discount_elements(amazon_url):
    """Investigate what discount elements are available on Amazon.ca"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-CA,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        
        print(f"Investigating: {amazon_url}")
        response = requests.get(amazon_url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Failed to fetch: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("\\n=== LOOKING FOR DISCOUNT ELEMENTS ===")
        
        # Look for various discount-related selectors
        discount_selectors = [
            '.savingsPercentage',
            '.a-price-savings-percentage', 
            '.a-text-strike + .a-text-price .a-offscreen',
            '[data-a-color="price"] .a-text-strike + .a-text-price',
            '.a-badge-text',
            '.a-price-savings',
            '.a-text-strike',
            '[class*="saving"]',
            '[class*="discount"]',
            '[class*="percent"]'
        ]
        
        found_elements = []
        
        for selector in discount_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"\\nFound {len(elements)} elements for selector: {selector}")
                for i, elem in enumerate(elements[:3]):  # Show first 3
                    text = elem.get_text().strip()
                    if text:
                        print(f"  [{i+1}] Text: '{text}'")
                        print(f"      Classes: {elem.get('class', [])}")
                        found_elements.append((selector, text, elem.get('class', [])))
        
        # Look for any text containing percentage
        print("\\n=== LOOKING FOR PERCENTAGE TEXT ===")
        percentage_pattern = r'\\d+%'
        all_text = soup.get_text()
        percentage_matches = re.findall(percentage_pattern, all_text)
        if percentage_matches:
            print(f"Found percentage text: {set(percentage_matches)}")
        
        # Look for price elements to understand structure
        print("\\n=== LOOKING FOR PRICE ELEMENTS ===")
        price_selectors = [
            '.a-price-whole',
            '.a-price .a-offscreen', 
            '.a-text-strike',
            '#priceblock_dealprice',
            '#priceblock_ourprice',
            '.a-price-range .a-offscreen'
        ]
        
        for selector in price_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"\\nFound {len(elements)} price elements for: {selector}")
                for i, elem in enumerate(elements[:2]):  # Show first 2
                    text = elem.get_text().strip()
                    if text:
                        print(f"  [{i+1}] Price text: '{text}'")
        
        return found_elements
        
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    # Test URLs from our deals
    test_urls = [
        "https://www.amazon.ca/dp/B09YZZML4W",  # SereneLife swing chair
        "https://www.amazon.ca/dp/B07ZVXK5K9",  # e.l.f. kit  
        "https://www.amazon.ca/dp/B08T7DSZYD",  # skincare kit
    ]
    
    for url in test_urls:
        investigate_amazon_discount_elements(url)
        print("\\n" + "="*80 + "\\n")

if __name__ == "__main__":
    main()