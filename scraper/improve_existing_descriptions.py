#!/usr/bin/env python3
"""
Improve existing descriptions in deals.json with real Amazon content
"""

import json
import os
import sys
from pathlib import Path
import time

# Add parent directory to path to find .env
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env file (optional, for testing with real Amazon URLs)
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

from scraper_env import SavingsGuruScraperEnv

def improve_descriptions():
    """Improve descriptions in deals.json with real Amazon content"""
    
    deals_path = Path(__file__).parent.parent / 'public' / 'deals.json'
    
    if not deals_path.exists():
        print("deals.json not found!")
        return
    
    # Load existing deals
    with open(deals_path) as f:
        deals = json.load(f)
    
    print(f"Loaded {len(deals)} deals from deals.json")
    
    # Create scraper instance (will work even without Google Sheets access)
    try:
        scraper = SavingsGuruScraperEnv()
        has_sheets_access = True
    except:
        # Create minimal scraper just for Amazon description scraping
        class MinimalScraper:
            def scrape_amazon_description(self, amazon_url):
                # Copy the scrape_amazon_description method from SavingsGuruScraperEnv
                try:
                    from bs4 import BeautifulSoup
                    import requests
                    import re
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Accept-Language': 'en-CA,en;q=0.9',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    }
                    
                    response = requests.get(amazon_url, headers=headers, timeout=15)
                    if response.status_code != 200:
                        return None
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Try to extract title and basic info for products without feature bullets
                    title_elem = soup.select_one('#productTitle')
                    product_title = title_elem.get_text().strip() if title_elem else ""
                    
                    # Try multiple description selectors in order of preference
                    description_approaches = [
                        # Approach 1: Feature bullets with colons (detailed descriptions)
                        {
                            'selectors': ['#feature-bullets ul li span.a-list-item', '[data-feature-name="featurebullets"] ul li span'],
                            'requires_colon': True,
                            'min_length': 20
                        },
                        # Approach 2: Product description paragraphs
                        {
                            'selectors': ['#productDescription p', '#aplus_feature_div p'],
                            'requires_colon': False,
                            'min_length': 30
                        },
                        # Approach 3: Any feature bullets (less strict)
                        {
                            'selectors': ['#feature-bullets .a-list-item', '.a-unordered-list.a-nostyle.a-vertical li span'],
                            'requires_colon': False,
                            'min_length': 15
                        }
                    ]
                    
                    for approach in description_approaches:
                        for selector in approach['selectors']:
                            elements = soup.select(selector)
                            if elements:
                                descriptions = []
                                for elem in elements[:3]:  # Take first 3 elements
                                    text = elem.get_text().strip()
                                    text = ' '.join(text.split())  # Clean whitespace
                                    
                                    skip_phrases = ['make sure', 'please note', 'important', 'clothing, shoes & accessories', 
                                                  'home & kitchen', 'sports & outdoors', 'health & personal care',
                                                  'date first available', 'best sellers rank', 'customer reviews']
                                    
                                    colon_check = ':' in text if approach['requires_colon'] else True
                                    
                                    if (text and len(text) > approach['min_length'] and len(text) < 300 and 
                                        not any(skip in text.lower() for skip in skip_phrases) and
                                        colon_check and not text.startswith('•') and not text.startswith('-')):
                                        descriptions.append(text)
                                
                                if descriptions:
                                    # Join descriptions, limit to ~150 chars for cards
                                    combined = '. '.join(descriptions)
                                    if len(combined) > 150:
                                        combined = combined[:147] + "..."
                                    print(f"Extracted Amazon description: {combined[:50]}...")
                                    return combined
                    
                    # Fallback: Use product title with a generic description if we can't find anything
                    if product_title and len(product_title) > 10:
                        fallback = f"{product_title[:100]}... - High quality product with great value"
                        if len(fallback) > 150:
                            fallback = fallback[:147] + "..."
                        print(f"Using title fallback: {fallback[:50]}...")
                        return fallback
                    
                    return None
                    
                except Exception as e:
                    print(f"Error scraping Amazon description: {e}")
                    return None
        
        scraper = MinimalScraper()
        has_sheets_access = False
    
    updated_count = 0
    
    # Process each deal
    for i, deal in enumerate(deals):
        # Check if description needs improvement (generic phrases or short content)
        current_desc = deal.get('description', '')
        needs_update = any([
            "🔥 DEAL ALERT!" in current_desc,
            "⚡ HOT DEAL!" in current_desc,
            "🎯 This deal is" in current_desc,
            "💫 Your new favorite" in current_desc,
            "🚀 Level up" in current_desc,
            "⭐ Customer favorite" in current_desc,
            len(current_desc) < 50  # Very short descriptions
        ])
        
        if needs_update and deal.get('affiliateUrl') and 'amazon.ca' in deal['affiliateUrl']:
            print(f"\nImproving description for: {deal['title'][:40]}...")
            
            # Try to get real Amazon description
            amazon_desc = scraper.scrape_amazon_description(deal['affiliateUrl'])
            
            if amazon_desc:
                deal['description'] = amazon_desc
                updated_count += 1
                print("Updated with Amazon content")
            else:
                print("Could not extract Amazon description")
            
            # Rate limiting
            time.sleep(2)
        else:
            print(f"Skipping {deal['title'][:30]} - description looks good")
    
    if updated_count > 0:
        # Save updated deals.json
        with open(deals_path, 'w') as f:
            json.dump(deals, f, indent=2)
        
        print(f"\nUpdated {updated_count} descriptions with real Amazon content!")
        print(f"Saved to {deals_path}")
    else:
        print("\nAll descriptions already look good!")

if __name__ == "__main__":
    improve_descriptions()