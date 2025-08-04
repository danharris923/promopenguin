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
    
    def extract_affiliate_link(self, deal_url):
        """Extract the main affiliate/deal link from SmartCanucks post"""
        try:
            response = requests.get(deal_url, timeout=10)
            if response.status_code != 200:
                return None, 'unknown'
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for all external links in the post content, prioritizing bottom links
            content_area = soup.find('div', class_='entry-content') or soup.find('article') or soup
            
            # Skip unwanted links (SmartCanucks, app stores, social media)
            skip_domains = [
                'smartcanucks.ca', 'apps.apple.com', 'play.google.com', 
                'facebook.com', 'twitter.com', 'instagram.com', 'pinterest.com',
                'hotcanadadeals.ca', 'flipp.com'
            ]
            
            # Get all links and look for the best deal link
            all_links = content_area.find_all('a', href=True)
            
            # First pass: look for links with deal/sale/promo keywords
            for a in all_links:
                href = a['href']
                link_text = a.get_text().lower()
                
                # Skip unwanted domains
                if any(domain in href.lower() for domain in skip_domains):
                    continue
                    
                # Prioritize links with deal-related text
                if any(keyword in link_text for keyword in ['sale', 'deal', 'promo', 'clearance', 'offer', 'save', 'discount', 'shop now', 'get it']):
                    print(f"  Found deal link with text '{a.get_text()[:30]}': {href[:60]}...")
                    
                    # Check for Amazon links
                    if any(x in href.lower() for x in ['amzn.to/', 'amazon.ca', 'amazon.com']):
                        print(f"  Found Amazon deal link: {href}")
                        if 'amzn.to/' in href:
                            try:
                                redirect_response = requests.head(href, allow_redirects=True, timeout=10)
                                final_url = redirect_response.url
                                return self.clean_and_add_affiliate_tag(final_url, 'amazon'), 'amazon'
                            except:
                                return self.clean_and_add_affiliate_tag(href, 'amazon'), 'amazon'
                        else:
                            return self.clean_and_add_affiliate_tag(href, 'amazon'), 'amazon'
                    
                    # Skip shortened links
                    elif any(x in href.lower() for x in ['bit.ly/', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co']):
                        print(f"  Skipping shortened link: {href}")
                        continue
                    
                    # Accept other merchant links with deal text
                    elif 'http' in href and '.' in href:
                        print(f"  Found merchant deal link: {href}")
                        cleaned_url = self.clean_affiliate_link(href)
                        if cleaned_url:
                            return cleaned_url, 'other'
            
            # Second pass: if no deal-specific link found, look from bottom to top
            all_links.reverse()  # Start from bottom of post
            
            for a in all_links:
                href = a['href']
                
                # Skip unwanted links first
                if any(domain in href.lower() for domain in skip_domains):
                    continue
                
                print(f"  Checking link: {href[:60]}...")
                    
                # Check for Amazon links (amzn.to, amazon.ca, amazon.com)
                if any(x in href.lower() for x in ['amzn.to/', 'amazon.ca', 'amazon.com']):
                    print(f"  Found Amazon link: {href}")
                    if 'amzn.to/' in href:
                        try:
                            redirect_response = requests.head(href, allow_redirects=True, timeout=10)
                            final_url = redirect_response.url
                            return self.clean_and_add_affiliate_tag(final_url, 'amazon'), 'amazon'
                        except:
                            return self.clean_and_add_affiliate_tag(href, 'amazon'), 'amazon'
                    else:
                        return self.clean_and_add_affiliate_tag(href, 'amazon'), 'amazon'
                
                # Skip shortened links (bit.ly, etc.) - don't process these
                elif any(x in href.lower() for x in ['bit.ly/', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co']):
                    print(f"  Skipping shortened link: {href}")
                    continue
                
                # Any other merchant links - accept them all (clean and ready for future affiliate tags)
                elif 'http' in href and '.' in href:
                    print(f"  Found merchant link: {href}")
                    cleaned_url = self.clean_affiliate_link(href)
                    if cleaned_url:  # Only return if it passed the safety check
                        return cleaned_url, 'other'
            
            return None, 'unknown'
            
        except Exception as e:
            print(f"Error extracting affiliate link: {e}")
            return None, 'unknown'
    
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
            for entry in feed.entries:
                if count >= limit:
                    break
                    
                try:
                    print(f"Processing: {entry.title[:50]}...")
                except UnicodeEncodeError:
                    print(f"Processing: {entry.title[:30].encode('ascii', 'replace').decode('ascii')}...")
                
                # Create unique ID
                deal_id = re.sub(r'[^a-zA-Z0-9]', '', entry.title.lower())[:20]
                
                # Extract affiliate link from the actual post page (not RSS content)
                print(f"  Scraping individual post: {entry.link}")
                affiliate_url, link_type = self.extract_affiliate_link(entry.link)
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