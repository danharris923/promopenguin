#!/usr/bin/env python3
"""
Simple RSS-to-JSON scraper that works without Google Sheets
"""

import json
import feedparser
import requests
import re
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import time
from bs4 import BeautifulSoup
import random

class SimpleScraper:
    def __init__(self):
        self.affiliate_tag = "savingsgurucc-20"
    
    def extract_amazon_link(self, deal_url):
        """Extract real Amazon product link from SavingsGuru post"""
        try:
            response = requests.get(deal_url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for amzn.to short links
            for a in soup.find_all('a', href=True):
                href = a['href']
                if 'amzn.to/' in href:
                    redirect_response = requests.head(href, allow_redirects=True, timeout=10)
                    final_url = redirect_response.url
                    return self.add_affiliate_tag(final_url)
            
            # Fallback: direct Amazon URLs
            for a in soup.find_all('a', href=True):
                href = a['href']
                if 'amazon' in href.lower() and ('/dp/' in href or '/gp/product/' in href):
                    return self.add_affiliate_tag(href)
                    
            return None
            
        except Exception as e:
            print(f"Error extracting Amazon link: {e}")
            return None
    
    def add_affiliate_tag(self, amazon_url):
        """Add affiliate tag to Amazon URL"""
        parsed = urlparse(amazon_url)
        params = parse_qs(parsed.query)
        params['tag'] = [self.affiliate_tag]
        
        new_query = '&'.join([f"{k}={v[0]}" for k, v in params.items()])
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
    
    def extract_product_image(self, deal_url):
        """Extract the main product image from SavingsGuru post"""
        try:
            response = requests.get(deal_url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the main product image
            content_img = soup.select_one('.entry-content img, .post-content img, article img')
            if content_img and content_img.get('src'):
                img_url = content_img.get('src')
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                elif img_url.startswith('/'):
                    img_url = 'https://www.savingsguru.ca' + img_url
                return img_url
            
            return None
            
        except Exception as e:
            print(f"Error extracting product image: {e}")
            return None
    
    def generate_price_and_discount(self, title):
        """Generate realistic prices based on product type"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['electronics', 'tech', 'phone', 'laptop', 'tv', 'lego', 'game']):
            current_price = random.uniform(199, 899)
            original_price = current_price * random.uniform(1.3, 1.6)
        elif any(word in title_lower for word in ['clothing', 'shirt', 'pants', 'dress', 'shoes', 'tight', 'under']):
            current_price = random.uniform(19, 79)
            original_price = current_price * random.uniform(1.2, 1.5)
        elif any(word in title_lower for word in ['home', 'kitchen', 'furniture', 'decor', 'backpack', 'bag']):
            current_price = random.uniform(29, 199)
            original_price = current_price * random.uniform(1.3, 1.7)
        else:
            current_price = random.uniform(24, 89)
            original_price = current_price * random.uniform(1.3, 1.6)
        
        discount = int(((original_price - current_price) / original_price) * 100)
        return round(current_price, 2), round(original_price, 2), discount
    
    def generate_description(self, title):
        """Generate engaging descriptions"""
        templates = [
            f"🔥 Amazing deal on {title}! Premium quality at an unbeatable price.",
            f"⚡ Hot savings on {title}! Don't miss this incredible offer.",
            f"💫 Discover why thousands love {title}. Quality meets value!",
            f"🏆 Top-rated {title} at a fantastic price. Your wallet will thank you!",
            f"⭐ Customer favorite! {title} delivers exceptional value.",
            f"🎯 Limited time offer on {title}. Act fast before it's gone!",
        ]
        return random.choice(templates)
    
    def parse_rss_and_generate_json(self, feed_url="https://www.savingsguru.ca/feed/", limit=100):
        """Parse RSS feed and generate deals.json directly"""
        print(f"Fetching RSS feed from {feed_url}...")
        feed = feedparser.parse(feed_url)
        deals = []
        
        count = 0
        for entry in feed.entries:
            if count >= limit:
                break
                
            print(f"Processing: {entry.title[:50]}...")
            
            # Create unique ID
            deal_id = re.sub(r'[^a-zA-Z0-9]', '', entry.title.lower())[:20]
            
            # Extract Amazon link and image
            amazon_url = self.extract_amazon_link(entry.link)
            product_image = self.extract_product_image(entry.link)
            
            # Generate pricing
            current_price, original_price, discount = self.generate_price_and_discount(entry.title)
            
            # Generate description
            description = self.generate_description(entry.title)
            
            deal = {
                'id': deal_id,
                'title': entry.title,
                'imageUrl': product_image or '/placeholder-deal.svg',
                'price': current_price,
                'originalPrice': original_price,
                'discountPercent': discount,
                'category': 'General',
                'description': description,
                'affiliateUrl': amazon_url or entry.link,
                'featured': count < 5,  # First 5 are featured
                'dateAdded': datetime.now().strftime('%Y-%m-%d')
            }
            
            deals.append(deal)
            count += 1
            time.sleep(0.5)  # Be nice to the server
        
        # Write to deals.json
        output_path = '../public/deals.json'
        with open(output_path, 'w') as f:
            json.dump(deals, f, indent=2)
        
        print(f"Generated {len(deals)} deals in {output_path}")
        return deals

def main():
    scraper = SimpleScraper()
    scraper.parse_rss_and_generate_json(limit=100)

if __name__ == "__main__":
    main()