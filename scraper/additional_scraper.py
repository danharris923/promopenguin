#!/usr/bin/env python3
"""
Additional scraper that extracts Amazon product URLs and swaps affiliate tags
"""

import json
import feedparser
import requests
import re
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class AdditionalScraper:
    def __init__(self):
        self.affiliate_tag = os.getenv('AFFILIATE_TAG', 'promopenguin-20')
        self.base_url = 'https://savingsguru.ca'
        self.limit = int(os.getenv('DEAL_LIMIT', '99'))
        
        print(f"=== ADDITIONAL SCRAPER ===")
        print(f"Affiliate Tag: {self.affiliate_tag}")
        print(f"Deal Limit: {self.limit}")
        print(f"===========================")

    def resolve_amazon_shortlink(self, short_url):
        """Resolve Amazon short links to full URLs and swap affiliate tags"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Follow redirects to get the final Amazon URL
            response = requests.get(short_url, headers=headers, timeout=5, allow_redirects=True)
            final_url = response.url
            
            # Check if it's an Amazon URL
            if 'amazon.' in final_url:
                # Parse the URL and swap the affiliate tag
                parsed = urlparse(final_url)
                query_params = parse_qs(parsed.query)
                
                # Replace or add our affiliate tag
                query_params['tag'] = [self.affiliate_tag]
                
                # Remove other affiliate parameters that might conflict
                unwanted_params = ['ascsubtag', 'ref', 'pf_rd_r', 'pf_rd_p', 'pf_rd_m', 'pf_rd_s', 'pf_rd_t', 'pf_rd_i']
                for param in unwanted_params:
                    query_params.pop(param, None)
                
                # Rebuild the URL with our affiliate tag
                new_query = urlencode(query_params, doseq=True)
                new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
                
                print(f"  Resolved: {short_url[:50]}... -> Amazon with our tag")
                return new_url
            else:
                print(f"  Not Amazon: {final_url[:50]}...")
                return final_url
                
        except Exception as e:
            print(f"  Error resolving {short_url}: {e}")
            return short_url


    def extract_shortlink_and_image(self, post_url):
        """Extract shortlink from beginning of post and steal WordPress image"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            print(f"  Visiting post: {post_url[:50]}...")
            response = requests.get(post_url, headers=headers, timeout=8)
            if response.status_code != 200:
                return None, None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find shortlink at the beginning of post body
            shortlink = None
            post_content = soup.select_one('.entry-content, .post-content, .content, article')
            
            if post_content:
                # Look for first Amazon shortlink in the post content
                first_links = post_content.find_all('a', href=True)[:5]  # Check first 5 links
                for link in first_links:
                    href = link.get('href', '')
                    if any(domain in href for domain in ['amzn.to', 'amazon.com', 'amazon.ca', 'a.co']):
                        shortlink = href
                        print(f"  Found shortlink: {shortlink[:50]}...")
                        break
            
            # Steal the WordPress image - look for screenshots first
            image_url = None
            
            # Look for actual product images first, then fall back to screenshots
            all_images = soup.find_all('img')
            product_image = None
            screenshot_image = None
            fallback_image = None
            
            for img in all_images:
                src = img.get('src', '')
                if not src:
                    continue
                
                # Skip obvious buttons and small images
                if any(skip in src.lower() for skip in ['button', '238-2384957', 'find-out-more', 'click-here']):
                    continue
                
                # Look for Amazon product images (they usually have specific patterns)
                if any(pattern in src.lower() for pattern in ['_ac_sx', '_ac_sy', 'amazon', 'ssl-images-amazon']):
                    product_image = src
                    print(f"  Found Amazon product image: {src[:50]}...")
                    break
                
                # Look for other high-quality product images
                elif any(pattern in src.lower() for pattern in ['.jpg', '.jpeg', '.png']) and not any(skip in src.lower() for skip in ['icon', 'logo', 'button', '100x100', '150x150', 'placeholder']):
                    # Check if it looks like a product image (reasonable size, not tiny)
                    if ('uploads/' in src and not screenshot_image) or not fallback_image:
                        if 'screenshot' in src.lower():
                            screenshot_image = src
                        else:
                            fallback_image = src
            
            # Priority: Product image > Fallback image > Screenshot
            if product_image:
                image_url = product_image
                print(f"  Using Amazon product image: {product_image[:50]}...")
            elif fallback_image:
                image_url = fallback_image
                print(f"  Using fallback image: {fallback_image[:50]}...")
            elif screenshot_image:
                image_url = screenshot_image
                print(f"  Using screenshot as last resort: {screenshot_image[:50]}...")
            else:
                image_url = None
            
            if image_url:
                if image_url.startswith('//'):
                    image_url = 'https:' + image_url
                elif image_url.startswith('/'):
                    image_url = self.base_url + image_url
                print(f"  Stole WordPress image: {image_url[:50]}...")
            
            # Extract actual content after the Ashly Fraser intro
            actual_content = self.extract_content_after_intro(post_content)
            
            return shortlink, image_url, actual_content
            
        except Exception as e:
            print(f"  Error extracting from post {post_url}: {e}")
            return None, None, None

    def extract_content_after_intro(self, post_content):
        """Extract the actual descriptive text after Ashly Fraser's standard intro, excluding social links"""
        if not post_content:
            return ""
        
        # Get all text content
        full_text = post_content.get_text()
        
        # Look for the end of the standard intro pattern
        intro_patterns = [
            r"If you're not sure whether to buy, add to cart, and you can come back to it later!\*\*",
            r"add to cart, and you can come back to it later!",
            r"read some of the reviews and see people thought of the product",
        ]
        
        # Try to find where the intro ends
        content_start = 0
        for pattern in intro_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                content_start = match.end()
                break
        
        # Extract content after the intro
        actual_content = full_text[content_start:].strip()
        
        # Remove social media links and URLs
        social_patterns = [
            r'https?://[^\s]+',  # Any URLs
            r'www\.[^\s]+',      # www links
            r'facebook\.com[^\s]*', 
            r'twitter\.com[^\s]*',
            r'instagram\.com[^\s]*',
            r'youtube\.com[^\s]*',
            r'tiktok\.com[^\s]*',
            r'Follow us on[^\n]*',
            r'Like us on[^\n]*',
            r'Subscribe[^\n]*',
        ]
        
        for pattern in social_patterns:
            actual_content = re.sub(pattern, '', actual_content, flags=re.IGNORECASE)
        
        # If we didn't find much content after the intro, just return the title
        if len(actual_content.strip()) < 50:
            # Get the title from the beginning (before "sells on Amazon")
            title_match = re.search(r'^(.*?)(?:\s+sells on Amazon|$)', full_text, re.IGNORECASE)
            if title_match:
                actual_content = title_match.group(1).strip()
                # Remove the author name and date if it's there
                actual_content = re.sub(r'^.*?\d{4}\s+\d+\s+', '', actual_content).strip()
        
        # Clean up whitespace and limit length
        actual_content = re.sub(r'\s+', ' ', actual_content).strip()
        return actual_content[:300] + ('...' if len(actual_content) > 300 else '')

    def resolve_and_retag_url(self, original_url):
        """Resolve any shortened/redirect URLs and retag to our Amazon affiliate"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Follow redirects to get final URL
            response = requests.get(original_url, headers=headers, timeout=5, allow_redirects=True)
            final_url = response.url
            
            # Check if final URL is Amazon
            if any(domain in final_url.lower() for domain in ['amazon.com', 'amazon.ca', 'amazon.co.uk', 'amzn.to']):
                # Parse and retag Amazon URL
                parsed = urlparse(final_url)
                query_params = parse_qs(parsed.query)
                
                # Replace with our affiliate tag
                query_params['tag'] = [self.affiliate_tag]
                
                # Remove conflicting affiliate parameters
                unwanted_params = ['ascsubtag', 'ref_', 'pf_rd_r', 'pf_rd_p', 'pf_rd_m', 'pf_rd_s', 'pf_rd_t', 'pf_rd_i']
                for param in unwanted_params:
                    query_params.pop(param, None)
                
                # Rebuild URL with our tag
                new_query = urlencode(query_params, doseq=True)
                tagged_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
                
                print(f"  [OK] Tagged Amazon URL: {original_url[:50]}...")
                return tagged_url, True
            else:
                print(f"  [SKIP] Not Amazon URL: {final_url[:50]}...")
                return final_url, False
                
        except Exception as e:
            print(f"  [ERROR] Error resolving URL {original_url}: {e}")
            return original_url, False

    def scrape_additional_deals(self):
        """Scrape deals from additional RSS feed and resolve/retag links"""
        all_deals = []
        
        # Try multiple RSS endpoints to get more deals
        feed_urls = [
            'https://savingsguru.ca/feed/',
            'https://savingsguru.ca/feed/?paged=2',
            'https://savingsguru.ca/feed/?paged=3',
            'https://savingsguru.ca/category/amazon/feed/',
            'https://savingsguru.ca/category/deals/feed/',
        ]
        
        processed_urls = set()  # Track processed posts to avoid duplicates
        
        for feed_url in feed_urls:
            if len(all_deals) >= self.limit:
                break
                
            print(f"Processing feed: {feed_url}")
            
            try:
                feed = feedparser.parse(feed_url)
                print(f"Found {len(feed.entries)} entries")
                
                for i, entry in enumerate(feed.entries):
                    if len(all_deals) >= self.limit:
                        break
                        
                    title = entry.title.strip()
                    post_url = entry.link
                    
                    # Skip duplicates
                    if post_url in processed_urls:
                        continue
                    processed_urls.add(post_url)
                    
                    print(f"\nProcessing [{len(all_deals)+1}/{self.limit}]: {title[:50]}...")
                    
                    # First try direct URL resolution
                    resolved_url, is_amazon = self.resolve_and_retag_url(post_url)
                    
                    # Always extract shortlink and image from the blog post
                    print(f"  [INFO] Extracting shortlink and image from post...")
                    shortlink, image_url, actual_content = self.extract_shortlink_and_image(post_url)
                    
                    if not shortlink:
                        print(f"  [SKIP] No Amazon shortlink found in post...")
                        continue
                    
                    # Resolve shortlink to long Amazon URL and swap affiliate tag
                    resolved_url = self.resolve_amazon_shortlink(shortlink)
                    if not resolved_url or 'amazon.' not in resolved_url:
                        print(f"  [SKIP] Failed to resolve shortlink to Amazon URL...")
                        continue
                    
                    # Generate deal data from RSS entry
                    deal_id = re.sub(r'[^a-z0-9]', '', title.lower())[:20] or f"add{len(all_deals)}"
                    
                    # Use blank/null for pricing instead of 0
                    price = None
                    original_price = None
                    discount = 0
                    
                    # Clean up title (remove price info and common prefixes)
                    clean_title = re.sub(r'\$\d+(?:\.\d{2})?(?:\s*(?:off|sale|deal|save))?', '', title, flags=re.IGNORECASE)
                    clean_title = re.sub(r'^(?:deal|sale|save|hot)\s*:?\s*', '', clean_title, flags=re.IGNORECASE)
                    clean_title = clean_title.strip()
                    
                    # Use actual content extracted from post, or title if empty
                    if actual_content and len(actual_content.strip()) > 10:
                        description = actual_content
                    else:
                        # If no good content found, just double the title
                        description = f"{clean_title} - {clean_title}"
                    
                    # Use extracted image or placeholder
                    if not image_url:
                        image_url = f"https://via.placeholder.com/300x200/93c4d8/ffffff?text=Amazon+Deal+{len(all_deals)+1}"
                    
                    # Get entry date
                    date_added = datetime.now().strftime('%Y-%m-%d')
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        try:
                            date_added = time.strftime('%Y-%m-%d', entry.published_parsed)
                        except:
                            pass
                    
                    deal = {
                        'id': deal_id,
                        'title': clean_title,
                        'imageUrl': image_url,
                        'price': price,
                        'originalPrice': original_price,
                        'discountPercent': discount,
                        'category': 'Amazon',
                        'description': description,
                        'affiliateUrl': resolved_url,
                        'featured': len(all_deals) < 3,  # First 3 are featured
                        'dateAdded': date_added,
                        'source': 'Additional'
                    }
                    
                    all_deals.append(deal)
                    print(f"  [OK] Added Amazon deal: {clean_title[:30]}...")
                    
                    time.sleep(0.2)  # Be respectful to the server
                    
            except Exception as e:
                print(f"Error processing feed {feed_url}: {e}")
                continue
        
        return all_deals

    def save_deals(self, deals):
        """Save deals to JSON file"""
        output_path = '../public/additional_deals.json'
        
        print(f"\nSaving {len(deals)} additional deals to {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(deals, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Saved {len(deals)} additional deals successfully!")
        return deals

def main():
    scraper = AdditionalScraper()
    deals = scraper.scrape_additional_deals()
    if deals:
        scraper.save_deals(deals)
        print(f"\n[SUCCESS] Generated {len(deals)} additional deals total!")
    else:
        print("\n[WARNING] No deals found!")

if __name__ == "__main__":
    main()