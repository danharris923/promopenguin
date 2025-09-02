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

    def extract_deal_url_from_post(self, post_url, title):
        """Extract the actual deal/sale URL from the blog post"""
        title_lower = title.lower()
        
        # Override specific merchants with our affiliate links
        if any(word in title_lower for word in ['walmart']):
            print(f"  Using Walmart affiliate override")
            return 'https://shopstyle.it/l/cuge4'
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; PromoBot/1.0)'}
            response = requests.get(post_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find all links in the post content
                content_selectors = ['.entry-content', '.post-content', 'article', '.content']
                all_links = []
                
                for selector in content_selectors:
                    content = soup.select_one(selector)
                    if content:
                        all_links.extend(content.find_all('a', href=True))
                        break
                
                if not all_links:
                    all_links = soup.find_all('a', href=True)
                
                # Look for sale/deal links - prefer longer ones first
                deal_urls = []
                
                for link in all_links:
                    href = link.get('href', '')
                    link_text = link.get_text(strip=True).lower()
                    
                    if not href or href.startswith('#'):
                        continue
                    
                    # Skip social media, smartcanucks internal links, competitors, unrelated sites
                    if any(x in href.lower() for x in ['facebook.com', 'twitter.com', 'instagram.com', 'smartcanucks.ca', 'mailto:', 'hotcanadadeals.ca', 'springshoessales.ca', 'targetcanadaflyer.ca']):
                        continue
                    
                    # Prioritize links that look like direct merchant links or have sale-related text
                    priority = 0
                    
                    # Higher priority for direct merchant domains
                    merchant_domains = ['walmart.ca', 'costco.ca', 'nofrills.ca', 'sobeys.com', 'shoppersdrugmart.ca', 
                                      'gap.ca', 'lacoste.com', 'coach.com', 'bouclair.com', 'airmiles.ca',
                                      'suzyshier.com', 'stevemadden.ca', 'herschel.ca', 'hatley.com']
                    
                    for domain in merchant_domains:
                        if domain in href.lower():
                            priority += 100
                            break
                    
                    # Higher priority for sale/promo URLs
                    if any(x in href.lower() for x in ['sale', 'deal', 'promo', 'coupon', 'discount', 'offer']):
                        priority += 50
                    
                    # Higher priority for "shop now", "get deal" type link text
                    if any(x in link_text for x in ['shop', 'deal', 'sale', 'buy', 'get', 'offer']):
                        priority += 25
                    
                    # Must be a real external link
                    if any(x in href.lower() for x in ['.ca/', '.com/']):
                        deal_urls.append((priority, len(href), href))
                
                # Sort by priority first, then length
                deal_urls.sort(key=lambda x: (x[0], x[1]), reverse=True)
                
                # Return the best URL after cleaning
                for priority, length, url in deal_urls[:5]:  # Check top 5 candidates
                    clean_url = self.strip_affiliate_tags(url)
                    if clean_url and not any(x in clean_url.lower() for x in ['smartcanucks.ca', 'hotcanadadeals.ca', 'apps.apple.com']):
                        print(f"  Found deal URL: {clean_url[:60]}...")
                        return clean_url
                        
        except Exception as e:
            print(f"  Error extracting deal URL: {e}")
        
        # Fallback to merchant homepage - but skip if it would link back to source
        fallback_url = self.get_merchant_homepage(title)
        if fallback_url and not any(x in fallback_url.lower() for x in ['smartcanucks.ca', 'hotcanadadeals.ca']):
            return fallback_url
        
        # If we'd link back to source, return None to skip this deal
        print(f"  Skipping deal - would link back to source")
        return None
    
    def strip_affiliate_tags(self, url):
        """Strip affiliate tags from URLs"""
        if not url:
            return url
            
        # Common affiliate parameters to remove
        affiliate_params = [
            'tag=', 'ref=', 'utm_', 'aff_', 'affiliate', 'referrer',
            'source=', 'medium=', 'campaign=', 'content=', 'term=',
            'clickid', 'tracking', 'partner', 'promo_id'
        ]
        
        if '?' in url:
            base_url, params = url.split('?', 1)
            
            # Filter out affiliate parameters
            clean_params = []
            for param in params.split('&'):
                if '=' in param:
                    key = param.split('=')[0].lower()
                    # Keep only non-affiliate parameters
                    if not any(aff in key for aff in affiliate_params):
                        clean_params.append(param)
            
            if clean_params:
                return base_url + '?' + '&'.join(clean_params)
            else:
                return base_url
        
        return url
    
    def get_merchant_homepage(self, title):
        """Get clean merchant homepage as fallback"""
        title_lower = title.lower()
        
        # Only use affiliate links where we have confirmed partnerships
        if any(word in title_lower for word in ['amazon', 'amzn']):
            return f'https://amazon.ca/?tag={self.affiliate_tag}'
        
        # Walmart deals go to our ShopStyle affiliate link
        if any(word in title_lower for word in ['walmart']):
            return 'https://shopstyle.it/l/cuge4'
        
        # Clean merchant homepages
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
        }
        
        for merchant, url in merchant_map.items():
            if merchant in title_lower:
                return url
        
        return 'https://smartcanucks.ca/'  # Last resort fallback

    def extract_image_from_post(self, post_url):
        """Extract the largest/best product image from blog post"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; PromoBot/1.0)'}
            response = requests.get(post_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try Open Graph image first (usually the best)
                og_image = soup.select_one('meta[property="og:image"]')
                if og_image and og_image.get('content'):
                    og_url = og_image.get('content')
                    if 'smartcanucks-01.png' not in og_url and 'logo' not in og_url.lower():
                        return og_url
                
                # Look for WordPress featured image
                wp_image = soup.select_one('.wp-post-image')
                if wp_image and wp_image.get('src'):
                    img_url = wp_image.get('src')
                    if 'smartcanucks-01.png' not in img_url and 'logo' not in img_url.lower():
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif img_url.startswith('/'):
                            img_url = self.base_url + img_url
                        return img_url
                
                # Look for largest image in content that's not a logo
                content_images = soup.select('.entry-content img, .post-content img, article img')
                best_image = None
                best_size = 0
                
                for img in content_images:
                    img_url = img.get('src', '')
                    if not img_url or 'logo' in img_url.lower() or 'smartcanucks-01.png' in img_url:
                        continue
                    
                    # Try to estimate image size from URL or attributes
                    width = img.get('width', '0')
                    height = img.get('height', '0')
                    
                    try:
                        size = int(width) * int(height) if width.isdigit() and height.isdigit() else 0
                    except:
                        size = 0
                    
                    # Look for size indicators in filename
                    if any(x in img_url for x in ['-500x', '-400x', '-300x', '-600x']):
                        size = 500  # Boost priority for explicitly sized images
                    
                    if size > best_size:
                        best_size = size
                        best_image = img_url
                
                if best_image:
                    if best_image.startswith('//'):
                        best_image = 'https:' + best_image
                    elif best_image.startswith('/'):
                        best_image = self.base_url + best_image
                    return best_image
                        
        except Exception as e:
            print(f"  Error extracting image: {e}")
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
                    
                    # Extract the real deal URL from the blog post
                    affiliate_url = self.extract_deal_url_from_post(entry.link, title) if hasattr(entry, 'link') else self.get_merchant_homepage(title)
                    
                    # Skip this deal if we couldn't find a valid URL
                    if not affiliate_url:
                        print(f"  Skipped: {title[:30]}... (no valid URL)")
                        continue
                    
                    price, original_price, discount = self.generate_pricing(title)
                    description = self.generate_description(title)
                    
                    # Try to get image from RSS first (better than scraping)
                    image_url = None
                    
                    # RSS feeds often have image in media_content or enclosures
                    if hasattr(entry, 'media_content') and entry.media_content:
                        image_url = entry.media_content[0]['url']
                    elif hasattr(entry, 'enclosures') and entry.enclosures:
                        for enc in entry.enclosures:
                            if enc.type.startswith('image/'):
                                image_url = enc.href
                                break
                    elif hasattr(entry, 'links'):
                        for link in entry.links:
                            if link.get('type', '').startswith('image/'):
                                image_url = link.href
                                break
                    
                    # Fallback to scraping post if no RSS image
                    if not image_url and hasattr(entry, 'link'):
                        image_url = self.extract_image_from_post(entry.link)
                    
                    # Final fallback to placeholder
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