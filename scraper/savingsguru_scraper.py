import os
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import feedparser
import re
from urllib.parse import urlparse, parse_qs
import time
from description_enhancer import DescriptionEnhancer

class SavingsGuruScraper:
    def __init__(self, credentials_file, spreadsheet_id=None, spreadsheet_name=None):
        # Google Sheets setup
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        self.client = gspread.authorize(creds)
        
        # Open by ID if provided, otherwise by name
        if spreadsheet_id:
            self.sheet = self.client.open_by_key(spreadsheet_id).sheet1
        else:
            self.sheet = self.client.open(spreadsheet_name).sheet1
        
        # Amazon affiliate tag
        self.affiliate_tag = "savingsgurucc-20"
        
        # Description enhancer
        self.desc_enhancer = DescriptionEnhancer()
        
    def parse_rss_feed(self, feed_url="https://www.savingsguru.ca/feed/"):
        """Parse RSS feed from SavingsGuru.ca"""
        feed = feedparser.parse(feed_url)
        deals = []
        
        for entry in feed.entries[:20]:  # Get latest 20 entries
            deal = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
                'description': entry.get('summary', ''),
                'status': 'approved'
            }
            deals.append(deal)
            
        return deals
    
    def extract_amazon_link(self, deal_url):
        """Extract Amazon link from deal page"""
        try:
            response = requests.get(deal_url, timeout=10)
            content = response.text
            
            # Look for Amazon links in various formats
            amazon_patterns = [
                r'https?://(?:www\.)?amazon\.(?:com|ca)/[^\s"\'>]+',
                r'href="(https?://[^"]*amazon[^"]*)"',
                r'<a[^>]*href="([^"]*amazon[^"]*)"'
            ]
            
            for pattern in amazon_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    # Clean up the URL
                    url = matches[0]
                    # Remove HTML entities
                    url = url.replace('&amp;', '&')
                    url = url.replace('&#038;', '&')
                    return url
        except:
            pass
        return None
    
    def rewrite_affiliate_link(self, amazon_url):
        """Rewrite Amazon link with our affiliate tag"""
        if not amazon_url:
            return None
            
        # Clean HTML entities first
        amazon_url = amazon_url.replace('&amp;', '&').replace('&#038;', '&')
        
        # Extract ASIN from various Amazon URL formats
        asin_patterns = [
            r'/dp/([A-Z0-9]{10})',
            r'/gp/product/([A-Z0-9]{10})',
            r'/exec/obidos/ASIN/([A-Z0-9]{10})',
            r'amazon\.(?:com|ca)/[^/]*?([A-Z0-9]{10})',  # More flexible ASIN extraction
            r'/([A-Z0-9]{10})(?:[/?&]|$)'  # Fallback pattern
        ]
        
        asin = None
        for pattern in asin_patterns:
            match = re.search(pattern, amazon_url)
            if match:
                asin = match.group(1)
                # Validate ASIN format (starts with letter, 10 chars total)
                if len(asin) == 10 and asin[0].isalpha():
                    break
                else:
                    asin = None
                    
        if asin:
            # Build proper Amazon affiliate link (Canadian site)
            return f"https://www.amazon.ca/dp/{asin}?tag={self.affiliate_tag}"
        
        # If no ASIN found but it's still an Amazon URL, use sed-style replacement
        if 'amazon' in amazon_url.lower():
            # Replace old affiliate tag with new one, keep original URL structure
            # Replace any existing tag parameter
            result = re.sub(r'tag=[^&]*', f'tag={self.affiliate_tag}', amazon_url)
            # If no tag was found, add it
            if 'tag=' not in result:
                separator = '&' if '?' in result else '?'
                result = f"{result}{separator}tag={self.affiliate_tag}"
            return result
        
        # Not an Amazon URL, return original
        return amazon_url
    
    def scrape_amazon_details(self, amazon_url):
        """Scrape product details from Amazon"""
        try:
            if not amazon_url:
                return {'price': 0, 'original_price': 0, 'image_url': '', 'in_stock': True}
                
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(amazon_url, headers=headers, timeout=10)
            if response.status_code != 200:
                return {'price': 0, 'original_price': 0, 'image_url': '', 'in_stock': True}
                
            content = response.text
            
            # Extract product image URL
            image_url = ''
            image_patterns = [
                r'"hiRes":"([^"]*)"',
                r'"large":"([^"]*)"',
                r'data-old-hires="([^"]*)"',
                r'id="landingImage"[^>]*src="([^"]*)"'
            ]
            
            for pattern in image_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    image_url = matches[0].replace('\\u002F', '/')
                    if 'images-amazon' in image_url and image_url.startswith('http'):
                        break
                        
            return {
                'price': 0,  # Placeholder - Amazon makes price scraping difficult
                'original_price': 0,
                'image_url': image_url,
                'in_stock': True
            }
            
        except Exception as e:
            print(f"Error scraping Amazon details: {e}")
            return {'price': 0, 'original_price': 0, 'image_url': '', 'in_stock': True}
    
    def calculate_discount(self, price, original_price):
        """Calculate discount percentage"""
        if original_price > 0 and price < original_price:
            return round((1 - price / original_price) * 100)
        return 0
    
    def update_google_sheet(self, deals):
        """Update Google Sheets with scraped deals"""
        # Clear existing content
        self.sheet.clear()
        
        # Add headers
        headers = ['ID', 'Title', 'Original URL', 'Amazon URL', 'Price', 
                   'Original Price', 'Discount %', 'Image URL', 'Description', 
                   'Category', 'Status', 'Date Added', 'Notes']
        self.sheet.append_row(headers)
        
        # Add deals
        for i, deal in enumerate(deals, 1):
            amazon_url = self.extract_amazon_link(deal['link'])
            affiliate_url = self.rewrite_affiliate_link(amazon_url)
            
            # Placeholder for Amazon details
            amazon_details = self.scrape_amazon_details(amazon_url)
            
            # Enhance description
            enhanced_desc = self.desc_enhancer.enhance_description_local(
                title=deal['title'],
                original_desc=deal['description'],
                price=amazon_details['price'],
                discount=self.calculate_discount(amazon_details['price'], amazon_details['original_price'])
            )
            
            row = [
                str(i),
                deal['title'],
                deal['link'],
                affiliate_url or '',
                amazon_details['price'],
                amazon_details['original_price'],
                self.calculate_discount(amazon_details['price'], amazon_details['original_price']),
                amazon_details['image_url'],
                enhanced_desc[:200],  # Enhanced description, limit length
                'Amazon',  # Default category
                'approved',
                datetime.now().isoformat(),
                ''  # Notes field for manual editing
            ]
            
            self.sheet.append_row(row)
            time.sleep(1)  # Rate limiting
    
    def fetch_approved_deals(self):
        """Fetch approved deals from Google Sheets"""
        records = self.sheet.get_all_records()
        approved_deals = []
        
        for record in records:
            if record.get('Status', '').lower() == 'approved':
                deal = {
                    'id': record['ID'],
                    'title': record['Title'],
                    'imageUrl': record['Image URL'],
                    'price': float(record['Price'] or 0),
                    'originalPrice': float(record['Original Price'] or 0),
                    'discountPercent': int(record['Discount %'] or 0),
                    'category': record['Category'],
                    'description': record['Description'],
                    'affiliateUrl': record['Amazon URL'],
                    'featured': record.get('Notes', '').lower() == 'featured',
                    'dateAdded': record['Date Added']
                }
                approved_deals.append(deal)
                
        return approved_deals
    
    def generate_deals_json(self, output_path='../public/deals.json'):
        """Generate deals.json file from approved deals"""
        approved_deals = self.fetch_approved_deals()
        
        # Sort by date added (newest first)
        approved_deals.sort(key=lambda x: x['dateAdded'], reverse=True)
        
        # Write to JSON file
        with open(output_path, 'w') as f:
            json.dump(approved_deals, f, indent=2)
            
        print(f"Generated {output_path} with {len(approved_deals)} deals")
        
        return approved_deals

# Example usage
if __name__ == "__main__":
    # Using provided Google Sheets credentials
    scraper = SavingsGuruScraper(
        credentials_file='../../google_service_account.json',
        spreadsheet_id='1jkFjKFyOtv5zGw-l7ZF7H1i0e4MunSj3dP2bX7oA3zg'
    )
    
    # Scrape new deals
    print("Scraping RSS feed...")
    deals = scraper.parse_rss_feed()
    
    print(f"Found {len(deals)} deals")
    print("Updating Google Sheet...")
    scraper.update_google_sheet(deals)
    
    print("Fetching approved deals...")
    scraper.generate_deals_json()