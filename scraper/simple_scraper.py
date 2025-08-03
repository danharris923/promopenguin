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
    
    def fetch_wordpress_posts(self, base_url="https://www.savingsguru.ca", limit=500):
        """Fetch posts using WordPress REST API with pagination for 500+ posts"""
        all_posts = []
        page = 1
        per_page = 100  # WordPress API max per request
        
        try:
            while len(all_posts) < limit:
                api_url = f"{base_url}/wp-json/wp/v2/posts"
                params = {
                    'per_page': per_page,
                    'page': page,
                    'orderby': 'date',
                    'order': 'desc'
                }
                
                print(f"Fetching page {page} of posts...")
                response = requests.get(api_url, params=params, timeout=15)
                
                if response.status_code == 200:
                    posts = response.json()
                    if not posts:  # No more posts
                        break
                    
                    all_posts.extend(posts)
                    print(f"Got {len(posts)} posts, total: {len(all_posts)}")
                    
                    if len(posts) < per_page:  # Last page
                        break
                    
                    page += 1
                    time.sleep(0.5)  # Be nice to the API
                else:
                    print(f"WordPress API page {page} failed: {response.status_code}")
                    break
            
            return all_posts[:limit]  # Return up to the limit
            
        except Exception as e:
            print(f"WordPress API error: {e}, falling back to RSS")
            return None
    
    def scrape_deals_from_wordpress(self, limit=100):
        """Scrape deals directly from WordPress site using Beautiful Soup"""
        print(f"Scraping deals from WordPress site...")
        
        deals = []
        page = 1
        per_page = 20  # Posts per page on the site
        
        while len(deals) < limit:
            # Try different URL patterns to get more posts
            urls_to_try = [
                f"https://www.savingsguru.ca/page/{page}/",
                f"https://www.savingsguru.ca/category/amazon/page/{page}/",
            ]
            
            found_posts = False
            for url in urls_to_try:
                try:
                    print(f"Checking page {page}: {url}")
                    response = requests.get(url, timeout=15)
                    if response.status_code != 200:
                        continue
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for post links
                    post_links = soup.find_all('a', href=True)
                    post_urls = []
                    
                    for link in post_links:
                        href = link['href']
                        # Match post pattern: /YYYY/MM/DD/post-name/
                        if re.match(r'https://www\.savingsguru\.ca/\d{4}/\d{2}/\d{2}/.+/', href):
                            if href not in [deal.get('source_url') for deal in deals]:
                                post_urls.append(href)
                    
                    if post_urls:
                        found_posts = True
                        print(f"Found {len(post_urls)} posts on page {page}")
                        
                        for post_url in post_urls[:limit - len(deals)]:
                            if len(deals) >= limit:
                                break
                                
                            # Extract post title from URL
                            title_match = re.search(r'/([^/]+)/$', post_url)
                            if title_match:
                                title = title_match.group(1).replace('-', ' ').title()
                            else:
                                title = f"Deal {len(deals) + 1}"
                            
                            print(f"Processing: {title[:50]}...")
                            
                            # Create unique ID
                            deal_id = re.sub(r'[^a-zA-Z0-9]', '', title.lower())[:20]
                            
                            # Extract Amazon link and image
                            amazon_url = self.extract_amazon_link(post_url)
                            product_image = self.extract_product_image(post_url)
                            
                            # Generate pricing
                            current_price, original_price, discount = self.generate_price_and_discount(title)
                            
                            # Generate description
                            description = self.generate_description(title)
                            
                            deal = {
                                'id': deal_id,
                                'title': title,
                                'imageUrl': product_image or '/placeholder-deal.svg',
                                'price': current_price,
                                'originalPrice': original_price,
                                'discountPercent': discount,
                                'category': 'General',
                                'description': description,
                                'affiliateUrl': amazon_url or post_url,
                                'featured': len(deals) < 5,  # First 5 are featured
                                'dateAdded': datetime.now().strftime('%Y-%m-%d'),
                                'source_url': post_url
                            }
                            
                            deals.append(deal)
                            time.sleep(0.3)  # Be nice to the server
                        
                        break  # Found posts, no need to try other URLs
                
                except Exception as e:
                    print(f"Error scraping page {page}: {e}")
                    continue
            
            if not found_posts:
                print(f"No more posts found after page {page}")
                break
                
            page += 1
            if page > 10:  # Safety limit
                break
        
        return deals
    
    def parse_rss_and_generate_json(self, feed_url="https://www.savingsguru.ca/feed/", limit=500):
        """Use WordPress REST API to get more posts than RSS limit"""
        print(f"Fetching posts via WordPress REST API...")
        
        # Try WordPress REST API first
        wp_posts = self.fetch_wordpress_posts(limit=limit)
        deals = []
        
        if wp_posts:
            print(f"Found {len(wp_posts)} posts via REST API")
            for i, post in enumerate(wp_posts):
                if len(deals) >= limit:
                    break
                    
                title = post.get('title', {}).get('rendered', f'Deal {i+1}')
                post_url = post.get('link', '')
                
                print(f"Processing: {title[:50]}...")
                
                # Create unique ID
                deal_id = re.sub(r'[^a-zA-Z0-9]', '', title.lower())[:20]
                
                # Extract Amazon link and image
                amazon_url = self.extract_amazon_link(post_url)
                product_image = self.extract_product_image(post_url)
                
                # SAFETY CHECK: Only include deals with valid affiliate links (Amazon or ShopStyle)
                is_amazon = amazon_url and 'amazon' in amazon_url.lower() and 'savingsgurucc-20' in amazon_url
                is_shopstyle = amazon_url and 'shopstyle.it' in amazon_url.lower()
                
                if not amazon_url or not (is_amazon or is_shopstyle):
                    print(f"⚠️  SKIPPING: No valid affiliate link found for '{title[:30]}...'")
                    continue
                
                # SAFETY CHECK: Never use source URLs as affiliate links
                if amazon_url and ('savingsguru.ca' in amazon_url or post_url in amazon_url):
                    print(f"⚠️  SKIPPING: Source URL detected as affiliate link for '{title[:30]}...'")
                    continue
                
                # Generate pricing
                current_price, original_price, discount = self.generate_price_and_discount(title)
                
                # Generate description
                description = self.generate_description(title)
                
                deal = {
                    'id': deal_id,
                    'title': title,
                    'imageUrl': product_image or '/placeholder-deal.svg',
                    'price': current_price,
                    'originalPrice': original_price,
                    'discountPercent': discount,
                    'category': 'General',
                    'description': description,
                    'affiliateUrl': amazon_url,  # NEVER fallback to post_url
                    'featured': len(deals) < 5,  # First 5 are featured
                    'dateAdded': datetime.now().strftime('%Y-%m-%d')
                }
                
                deals.append(deal)
                print(f"✅ Added deal: {title[:30]}... -> {amazon_url[:50]}...")
                time.sleep(0.2)  # Be nice to the server
        
        if len(deals) < 10:  # Fallback to RSS if REST API failed
            print(f"WordPress scraping got {len(deals)} deals, falling back to RSS...")
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
                
                # SAFETY CHECK: Only include deals with valid affiliate links (Amazon or ShopStyle)
                is_amazon = amazon_url and 'amazon' in amazon_url.lower() and 'savingsgurucc-20' in amazon_url
                is_shopstyle = amazon_url and 'shopstyle.it' in amazon_url.lower()
                
                if not amazon_url or not (is_amazon or is_shopstyle):
                    print(f"⚠️  SKIPPING RSS: No valid affiliate link found for '{entry.title[:30]}...'")
                    continue
                
                # SAFETY CHECK: Never use source URLs as affiliate links
                if amazon_url and ('savingsguru.ca' in amazon_url or entry.link in amazon_url):
                    print(f"⚠️  SKIPPING RSS: Source URL detected as affiliate link for '{entry.title[:30]}...'")
                    continue
                
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
                    'affiliateUrl': amazon_url,  # NEVER fallback to entry.link
                    'featured': count < 5,  # First 5 are featured
                    'dateAdded': datetime.now().strftime('%Y-%m-%d')
                }
                
                deals.append(deal)
                print(f"✅ Added RSS deal: {entry.title[:30]}... -> {amazon_url[:50]}...")
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
    scraper.parse_rss_and_generate_json(limit=500)

if __name__ == "__main__":
    main()