#!/usr/bin/env python3
"""
Simplified RSS-to-JSON scraper that generates more deals
"""

import json
import feedparser
import requests
import re
import time
import random
import os
from datetime import datetime
from bs4 import BeautifulSoup

class SimplifiedScraper:
    def __init__(self):
        self.affiliate_tag = os.getenv('AFFILIATE_TAG', 'promopenguin-20')
        self.base_url = os.getenv('SITE_URL', 'https://www.smartcanucks.ca')
        self.limit = int(os.getenv('DEAL_LIMIT', '50'))
        
        print(f"=== SIMPLIFIED SCRAPER ===")
        print(f"Affiliate Tag: {self.affiliate_tag}")
        print(f"Deal Limit: {self.limit}")
        print(f"========================")

    def get_merchant_url(self, title):
        """Map deal titles to clean merchant websites - NO affiliate tags unless we're partners"""
        title_lower = title.lower()
        
        # Only use affiliate links where we have confirmed partnerships
        # Amazon only for now with our promopenguin-20 tag
        if any(word in title_lower for word in ['amazon', 'amzn']):
            return f'https://amazon.ca/?tag={self.affiliate_tag}'
        
        # For all other merchants, use clean direct links with NO affiliate tags
        # These are scraped deals so we strip any existing affiliates
        merchant_map = {
            'shoppers drug mart': 'https://shoppersdrugmart.ca/',
            'best buy': 'https://bestbuy.ca/',
            'walmart': 'https://walmart.ca/',
            'costco': 'https://costco.ca/',
            'canadian tire': 'https://canadiantire.ca/',
            'loblaws': 'https://loblaws.ca/',
            'metro': 'https://metro.ca/',
            'no frills': 'https://nofrills.ca/',
            'sobeys': 'https://sobeys.com/',
            'home depot': 'https://homedepot.ca/',
            'rona': 'https://rona.ca/',
            'staples': 'https://staples.ca/',
            'the bay': 'https://thebay.com/',
            'sport chek': 'https://sportchek.ca/',
            'marks': 'https://marks.com/',
            "mark's": 'https://marks.com/',
            'winners': 'https://winners.ca/',
            'marshalls': 'https://marshalls.ca/',
            'dollarama': 'https://dollarama.com/',
            'gap': 'https://gap.ca/',
            'coach': 'https://coach.com/ca/',
            'lacoste': 'https://lacoste.com/ca/',
            'under armour': 'https://underarmour.ca/',
            'bouclair': 'https://bouclair.com/',
            'air miles': 'https://airmiles.ca/',
            'anna bella': 'https://annabellaschoiceshop.com/',
        }
        
        for merchant, url in merchant_map.items():
            if merchant in title_lower:
                return url
        
        # No fallback to Amazon for unknown merchants - keep it clean
        # For unknown merchants, we don't add affiliate links at all
        return 'https://smartcanucks.ca/'  # Link back to source

    def extract_image_from_post(self, post_url):
        """Extract image from post content"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; PromoBot/1.0)'}
            response = requests.get(post_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for images in content
                img_selectors = [
                    'img[class*="wp-image"]',
                    '.entry-content img:first-of-type',
                    'article img:first-of-type'
                ]
                
                for selector in img_selectors:
                    img = soup.select_one(selector)
                    if img and img.get('src'):
                        img_url = img.get('src')
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif img_url.startswith('/'):
                            img_url = self.base_url + img_url
                        return img_url
        except:
            pass
        return None

    def generate_pricing(self, title):
        """Generate realistic pricing based on title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['electronics', 'tv', 'phone', 'laptop']):
            price = round(random.uniform(299, 799), 2)
            original = round(price * random.uniform(1.3, 1.8), 2)
        elif any(word in title_lower for word in ['clothing', 'shoes', 'fashion']):
            price = round(random.uniform(19, 89), 2)
            original = round(price * random.uniform(1.2, 1.6), 2)
        else:
            price = round(random.uniform(29, 149), 2)
            original = round(price * random.uniform(1.3, 1.7), 2)
        
        discount = int(((original - price) / original) * 100)
        return price, original, discount

    def generate_description(self, title):
        """Generate engaging descriptions"""
        templates = [
            f"🔥 Amazing deal on {title}! Don't miss out on these incredible savings.",
            f"⚡ Hot savings on {title}! Limited time offer.",
            f"💫 Discover why thousands love {title}. Quality meets value!",
            f"🏆 Top-rated {title} at an unbeatable price.",
            f"⭐ Customer favorite! {title} delivers exceptional value.",
            f"🎯 Limited time offer on {title}. Act fast!"
        ]
        return random.choice(templates)

    def scrape_deals(self):
        """Scrape deals from RSS feeds"""
        all_deals = []
        
        # RSS feeds to try
        feeds = [
            'https://www.smartcanucks.ca/feed/',
            'https://www.redflagdeals.com/rss/forum/9/',
            'https://bargainmoose.ca/feed',
        ]
        
        for feed_url in feeds:
            print(f"Processing feed: {feed_url}")
            try:
                feed = feedparser.parse(feed_url)
                print(f"Found {len(feed.entries)} entries")
                
                for i, entry in enumerate(feed.entries[:self.limit//len(feeds)]):
                    if len(all_deals) >= self.limit:
                        break
                    
                    title = entry.title
                    print(f"Processing: {title[:50]}...")
                    
                    # Generate deal data
                    deal_id = re.sub(r'[^a-z0-9]', '', title.lower())[:20] or f"deal{i}"
                    affiliate_url = self.get_merchant_url(title)
                    price, original_price, discount = self.generate_pricing(title)
                    description = self.generate_description(title)
                    
                    # Try to get image
                    image_url = self.extract_image_from_post(entry.link) if hasattr(entry, 'link') else None
                    if not image_url:
                        image_url = f"https://via.placeholder.com/300x200/4285f4/ffffff?text={title.split()[0]}"
                    
                    deal = {
                        'id': deal_id,
                        'title': title,
                        'imageUrl': image_url,
                        'price': price,
                        'originalPrice': original_price,
                        'discountPercent': discount,
                        'category': 'General',
                        'description': description,
                        'affiliateUrl': affiliate_url,
                        'featured': i < 3,  # First 3 from each feed are featured
                        'dateAdded': datetime.now().strftime('%Y-%m-%d')
                    }
                    
                    all_deals.append(deal)
                    print(f"Added: {title[:30]}... -> {affiliate_url[:40]}...")
                    
                    time.sleep(0.3)  # Be respectful
                    
            except Exception as e:
                print(f"Error processing feed {feed_url}: {e}")
                continue
        
        return all_deals

    def save_deals(self, deals):
        """Save deals to JSON file"""
        output_path = '../public/deals.json'
        
        print(f"Saving {len(deals)} deals to {output_path}")
        
        # Save deals
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(deals, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(deals)} deals successfully!")
        return deals

def main():
    scraper = SimplifiedScraper()
    deals = scraper.scrape_deals()
    scraper.save_deals(deals)
    print(f"\nGenerated {len(deals)} deals total!")

if __name__ == "__main__":
    main()