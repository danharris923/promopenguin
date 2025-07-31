#!/usr/bin/env python3
"""
Refresh image URLs for existing deals
"""

import json
import requests
import re
import time

def scrape_amazon_image(amazon_url):
    """Scrape just the image URL from Amazon"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(amazon_url, headers=headers, timeout=15)
        if response.status_code != 200:
            return ''
            
        content = response.text
        
        # Extract product image URL
        image_patterns = [
            r'"hiRes":"([^"]*)"',
            r'"large":"([^"]*)"', 
            r'data-old-hires="([^"]*)"',
            r'id="landingImage"[^>]*src="([^"]*)"',
            r'"main":\{"[^"]*":"([^"]*)"'
        ]
        
        for pattern in image_patterns:
            matches = re.findall(pattern, content)
            if matches:
                image_url = matches[0].replace('\\u002F', '/').replace('\\/', '/')
                # Clean up common issues
                if image_url.startswith('//'):
                    image_url = 'https:' + image_url
                if 'images-amazon' in image_url and 'http' in image_url:
                    return image_url
                    
        return ''
        
    except Exception as e:
        print(f"Error scraping image from {amazon_url}: {e}")
        return ''

def refresh_images():
    """Refresh image URLs in deals.json"""
    # Read current deals
    with open('../public/deals.json', 'r') as f:
        deals = json.load(f)
    
    print(f"Refreshing images for {len(deals)} deals...")
    
    for i, deal in enumerate(deals):
        print(f"Deal {i+1}: {deal['title'][:50]}...")
        
        # Get fresh image URL from Amazon
        if deal.get('affiliateUrl'):
            fresh_image = scrape_amazon_image(deal['affiliateUrl'])
            if fresh_image:
                print(f"  -> Found new image: {fresh_image[:60]}...")
                deal['imageUrl'] = fresh_image
            else:
                print(f"  -> No image found, keeping existing")
        
        # Rate limiting
        time.sleep(2)
    
    # Write back to file
    with open('../public/deals.json', 'w') as f:
        json.dump(deals, f, indent=2)
    
    print("Done! Images refreshed in deals.json")

if __name__ == "__main__":
    refresh_images()