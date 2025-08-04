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
import os

class SimpleScraper:
    def __init__(self):
        self.affiliate_tag = os.getenv('AFFILIATE_TAG', 'offgriddisc06-20')
        self.base_url = os.getenv('SITE_URL', 'https://www.smartcanucks.ca')
        self.limit = int(os.getenv('DEAL_LIMIT', '10'))
        
        # Debug: Print the configuration being used
        print(f"=== SCRAPER CONFIGURATION ===")
        print(f"Site URL: {self.base_url}")
        print(f"Affiliate Tag: {self.affiliate_tag}")
        print(f"Deal Limit: {self.limit}")
        print(f"Feed URL will be: {self.base_url}/feed/")
        print(f"Environment variables:")
        print(f"  SITE_URL = {os.getenv('SITE_URL', 'NOT SET')}")
        print(f"  AFFILIATE_TAG = {os.getenv('AFFILIATE_TAG', 'NOT SET')}")
        print(f"  DEAL_LIMIT = {os.getenv('DEAL_LIMIT', 'NOT SET')}")
        print(f"=============================")
    
    def get_merchant_url_from_title(self, title):
        """Map deal titles to merchant websites"""
        title_lower = title.lower()
        
        # Merchant mapping based on common Canadian retailers
        merchant_map = {
            'reebok': 'https://reebok.ca/',
            'jysk': 'https://jysk.ca/',
            'marks': 'https://marks.com/',
            'mark\'s': 'https://marks.com/',
            'golf town': 'https://golftowncanada.ca/',
            'knix': 'https://knix.ca/',
            'healthy planet': 'https://healthyplanet.ca/',
            'shoppers drug mart': 'https://shoppersdrugmart.ca/',
            'best buy': 'https://bestbuy.ca/',
            'michaels': 'https://michaels.com/',
            'lovisa': 'https://lovisa.com/',
            'lenovo': 'https://lenovo.com/ca/',
            'loblaws': 'https://loblaws.ca/',
            'baskin robbins': 'https://baskinrobbins.ca/',
            'herman miller': 'https://hermanmiller.com/en_ca/',
        }
        
        for merchant, url in merchant_map.items():
            if merchant in title_lower:
                print(f"  Mapped '{merchant}' to {url}")
                return url, 'merchant'
        
        # Check for Amazon deals
        if 'amazon canada' in title_lower:
            return 'https://amazon.ca/', 'amazon'
        
        return None, 'unknown'
    
    def extract_affiliate_link_with_playwright(self, deal_url):
        """Use Playwright to extract JavaScript links from SmartCanucks posts"""
        from playwright.sync_api import sync_playwright
        
        try:
            print(f"  Using Playwright to load: {deal_url}")
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate and wait for content to load
                page.goto(deal_url, wait_until='networkidle')
                
                # Look for links in the content area
                content_selector = '.entry-content, article, .post-content'
                
                # Get all links that have onclick handlers or href attributes
                links = page.evaluate("""
                    () => {
                        const contentArea = document.querySelector('.entry-content, article, .post-content');
                        if (!contentArea) return [];
                        
                        const links = [];
                        const anchors = contentArea.querySelectorAll('a');
                        
                        anchors.forEach(a => {
                            let url = null;
                            let text = a.textContent.trim();
                            
                            // Check href first
                            if (a.href && a.href.startsWith('http')) {
                                url = a.href;
                            }
                            // Check onclick for JavaScript links
                            else if (a.onclick) {
                                const onclickStr = a.onclick.toString();
                                const urlMatch = onclickStr.match(/https?:\/\/[^'")]+/);
                                if (urlMatch) {
                                    url = urlMatch[0];
                                }
                            }
                            
                            if (url && text) {
                                links.push({ url, text });
                            }
                        });
                        
                        return links;
                    }
                """)
                
                browser.close()
                
                print(f"  Playwright found {len(links)} links")
                
                # Filter and select best link
                skip_domains = [
                    'smartcanucks.ca', 'apps.apple.com', 'play.google.com', 
                    'facebook.com', 'twitter.com', 'instagram.com', 'pinterest.com',
                    'hotcanadadeals.ca', 'flipp.com'
                ]
                
                valid_links = []
                for link in links:
                    url = link['url']
                    text = link['text']
                    
                    # Skip unwanted domains
                    if any(domain in url.lower() for domain in skip_domains):
                        continue
                    
                    # Skip shortened links
                    if any(x in url.lower() for x in ['bit.ly/', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co']):
                        continue
                    
                    print(f"  Valid link: {text[:30]} -> {url[:60]}")
                    
                    # Calculate priority
                    has_sale_text = any(keyword in text.lower() for keyword in 
                                      ['sale', 'deal', 'promo', 'clearance', 'offer', 'save', 'discount', 'shop now'])
                    path_depth = len([p for p in url.split('/')[3:] if p])  # Count path segments after domain
                    
                    valid_links.append({
                        'url': url,
                        'text': text,
                        'has_sale_text': has_sale_text,
                        'path_depth': path_depth
                    })
                
                if valid_links:
                    # Sort by sale text and path depth
                    valid_links.sort(key=lambda x: (x['has_sale_text'], x['path_depth']), reverse=True)
                    best_link = valid_links[0]
                    
                    print(f"  Selected: {best_link['text'][:30]} -> {best_link['url']}")
                    
                    # Handle Amazon links
                    if any(x in best_link['url'].lower() for x in ['amazon.ca', 'amazon.com']):
                        return self.clean_and_add_affiliate_tag(best_link['url'], 'amazon'), 'amazon'
                    else:
                        cleaned_url = self.clean_affiliate_link(best_link['url'])
                        return cleaned_url, 'other' if cleaned_url else None, 'unknown'
                
                return None, 'unknown'
                
        except Exception as e:
            print(f"  Playwright error: {e}")
            return None, 'error'
    
    def clean_and_add_affiliate_tag(self, amazon_url, platform='amazon'):
        """Clean existing affiliate tags and add our tag to Amazon URL"""
        parsed = urlparse(amazon_url)
        params = parse_qs(parsed.query)
        
        # Remove any existing affiliate tags
        affiliate_params = ['tag', 'ref', 'ref_', 'linkCode', 'linkId', 'camp', 'creative', 'creativeASIN']
        for param in affiliate_params:
            if param in params:
                del params[param]
        
        # Add our affiliate tag
        if platform == 'amazon':
            params['tag'] = [self.affiliate_tag]
        
        # Rebuild query string
        if params:
            new_query = '&'.join([f"{k}={v[0]}" for k, v in params.items()])
            return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
        else:
            return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    def clean_affiliate_link(self, url):
        """Clean affiliate parameters from non-Amazon URLs - NEVER link back to SmartCanucks"""
        # SAFETY CHECK: Never return unwanted URLs
        unwanted_domains = ['smartcanucks.ca', 'apps.apple.com', 'play.google.com', 'hotcanadadeals.ca']
        if any(domain in url.lower() for domain in unwanted_domains):
            return None
            
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # Remove common affiliate parameters
        affiliate_params = ['aff', 'affiliate', 'ref', 'referrer', 'source', 'utm_source', 'utm_medium', 'utm_campaign']
        for param in affiliate_params:
            if param in params:
                del params[param]
        
        # Rebuild URL without affiliate params (ready for our future tags)
        if params:
            new_query = '&'.join([f"{k}={v[0]}" for k, v in params.items()])
            return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
        else:
            return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    def extract_featured_image_from_api(self, post_data):
        """Extract featured image from WordPress REST API response"""
        try:
            # Check for embedded featured media (when using _embed parameter)
            if '_embedded' in post_data and 'wp:featuredmedia' in post_data['_embedded']:
                featured_media = post_data['_embedded']['wp:featuredmedia']
                if featured_media and len(featured_media) > 0:
                    media_item = featured_media[0]
                    if 'source_url' in media_item:
                        print(f"  Got featured image from API")
                        return media_item['source_url']
            
            # Fallback: Check Yoast SEO data for og:image
            if 'yoast_head_json' in post_data and 'og_image' in post_data['yoast_head_json']:
                og_images = post_data['yoast_head_json']['og_image']
                if og_images and len(og_images) > 0:
                    if 'url' in og_images[0]:
                        print(f"  📷 Got image from Yoast SEO")
                        return og_images[0]['url']
            
            return None
        except Exception as e:
            print(f"Error extracting featured image from API: {e}")
            return None
    
    def extract_product_image(self, deal_url):
        """Extract the main product image from SmartCanucks post"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(deal_url, headers=headers, timeout=10)
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
                    img_url = 'https://www.smartcanucks.ca' + img_url
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
    
    def fetch_wordpress_posts(self, base_url=None, limit=500):
        """Fetch posts using WordPress REST API with pagination for 500+ posts"""
        base_url = base_url or self.base_url
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
                    'order': 'desc',
                    '_embed': 'wp:featuredmedia'  # Include featured images in response
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
                f"https://www.smartcanucks.ca/page/{page}/",
                f"https://www.smartcanucks.ca/category/amazon/page/{page}/",
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
                        if re.match(r'https://www\.smartcanucks\.ca/\d{4}/\d{2}/\d{2}/.+/', href):
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
                            affiliate_url, link_type = self.extract_affiliate_link(post_url)
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
                                'affiliateUrl': affiliate_url,
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
    
    def parse_rss_and_generate_json(self, feed_url=None, limit=None):
        """Use WordPress REST API to get more posts than RSS limit"""
        feed_url = feed_url or f"{self.base_url}/feed/"
        limit = limit or self.limit
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
                
                # Extract Amazon link
                affiliate_url, link_type = self.extract_affiliate_link(post_url)
                
                # Extract image - try API first, then scraping
                product_image = self.extract_featured_image_from_api(post)
                if not product_image:
                    product_image = self.extract_product_image(post_url)
                    print(f"  Scraped image from post content")
                
                # SAFETY CHECK: Never use SmartCanucks URLs as affiliate links
                if affiliate_url and 'smartcanucks.ca' in affiliate_url.lower():
                    print(f"SKIPPING: SmartCanucks URL detected as affiliate link for '{title[:30]}...'")
                    continue
                
                # If no affiliate link found, skip this deal
                if not affiliate_url:
                    print(f"SKIPPING: No merchant link found for '{title[:30]}...'")
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
                    'affiliateUrl': affiliate_url,  # NEVER fallback to post_url
                    'featured': len(deals) < 5,  # First 5 are featured
                    'dateAdded': datetime.now().strftime('%Y-%m-%d')
                }
                
                deals.append(deal)
                print(f"Added deal: {title[:30]}... -> {affiliate_url[:50]}... [{link_type}]")
                time.sleep(0.2)  # Be nice to the server
        
        if len(deals) < 10:  # Fallback to RSS if REST API failed
            print(f"WordPress scraping got {len(deals)} deals, falling back to RSS...")
            feed = feedparser.parse(feed_url)
            deals = []
            
            count = 0
            batch_size = 10
            
            for entry in feed.entries:
                if count >= limit:
                    break
                
                # Sleep between batches to be respectful
                if count > 0 and count % batch_size == 0:
                    print(f"  Processed {count} deals, sleeping 3 seconds before next batch...")
                    time.sleep(3)
                    
                try:
                    print(f"Processing: {entry.title[:50]}...")
                except UnicodeEncodeError:
                    print(f"Processing: {entry.title[:30].encode('ascii', 'replace').decode('ascii')}...")
                
                # Create unique ID
                deal_id = re.sub(r'[^a-zA-Z0-9]', '', entry.title.lower())[:20]
                
                # SmartCanucks uses JavaScript links, use Playwright to extract them
                affiliate_url, link_type = self.extract_affiliate_link_with_playwright(entry.link)
                
                # Fallback to title mapping if Playwright fails
                if not affiliate_url:
                    print(f"  Playwright failed, trying title mapping...")
                    affiliate_url, link_type = self.get_merchant_url_from_title(entry.title)
                
                product_image = self.extract_product_image(entry.link)
                
                # SAFETY CHECK: Never use SmartCanucks URLs as affiliate links
                if affiliate_url and 'smartcanucks.ca' in affiliate_url.lower():
                    print(f"SKIPPING RSS: SmartCanucks URL detected as affiliate link for '{entry.title[:30]}...'")
                    continue
                
                # If no merchant link found, skip this deal
                if not affiliate_url:
                    print(f"SKIPPING RSS: No merchant link found for '{entry.title[:30]}...'")
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
                    'affiliateUrl': affiliate_url,  # NEVER fallback to entry.link
                    'featured': count < 5,  # First 5 are featured
                    'dateAdded': datetime.now().strftime('%Y-%m-%d')
                }
                
                deals.append(deal)
                print(f"Added RSS deal: {entry.title[:30]}... -> {affiliate_url[:50]}... [{link_type}]")
                count += 1
                time.sleep(1.0)  # Be nice to the server, avoid rate limiting
        
        # Write to deals.json
        output_path = '../public/deals.json'
        with open(output_path, 'w') as f:
            json.dump(deals, f, indent=2)
        
        print(f"Generated {len(deals)} deals in {output_path}")
        return deals

def main():
    scraper = SimpleScraper()
    scraper.parse_rss_and_generate_json()

if __name__ == "__main__":
    main()