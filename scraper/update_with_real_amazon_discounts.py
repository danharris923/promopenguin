#!/usr/bin/env python3
"""
Update existing deals with real Amazon discount percentages by scraping Amazon pages
"""

import os
import sys
from pathlib import Path
import time

# Add parent directory to path to find .env
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env file
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Load credentials from file
if 'GOOGLE_CREDS_FILE' in os.environ:
    creds_path = Path(__file__).parent.parent / os.environ['GOOGLE_CREDS_FILE']
    if creds_path.exists():
        with open(creds_path) as f:
            os.environ['GOOGLE_SHEETS_CREDS'] = f.read()

from scraper_env import SavingsGuruScraperEnv

def main():
    print("Updating deals with REAL Amazon discount percentages...")
    
    try:
        scraper = SavingsGuruScraperEnv()
        
        # Get all data from sheet
        all_data = scraper.sheet.get_all_values()
        
        if len(all_data) <= 1:
            print("No deals found in sheet")
            return
        
        headers = all_data[0]
        print(f"Headers: {headers}")
        
        # Find column indices
        amazon_url_col = headers.index('Amazon URL') if 'Amazon URL' in headers else 3
        discount_col = headers.index('Discount %') if 'Discount %' in headers else 6
        
        updated_count = 0
        
        # Process each deal (skip header)
        for i, row in enumerate(all_data[1:], start=2):  # Start from row 2
            if len(row) > amazon_url_col:
                deal_title = row[1] if len(row) > 1 else f"Deal {i-1}"
                amazon_url = row[amazon_url_col] if len(row) > amazon_url_col else ""
                
                if amazon_url and "/dp/" in amazon_url:
                    print(f"\\nUpdating row {i}: {deal_title[:40]}...")
                    print(f"Scraping discount from: {amazon_url[:60]}...")
                    
                    # Get REAL discount percentage from Amazon page
                    real_discount = scraper.scrape_amazon_discount(amazon_url)
                    
                    if real_discount > 0:
                        print(f"Found real Amazon discount: {real_discount}%")
                        
                        # Update the sheet with real Amazon discount
                        scraper.sheet.update_cell(i, discount_col + 1, real_discount)  # +1 for 1-based indexing
                        
                        updated_count += 1
                        
                        # Rate limiting to avoid hitting API limits
                        time.sleep(3)
                    else:
                        print("No discount found on Amazon page")
                else:
                    print(f"Skipping {deal_title[:30]} - no valid Amazon URL")
        
        print(f"\\nUpdated {updated_count} deals with real Amazon discount percentages!")
        
        # Now regenerate deals.json
        print("\\nRegenerating deals.json with real Amazon discounts...")
        deals = scraper.generate_deals_json()
        print(f"Generated deals.json with {len(deals)} deals and real Amazon discounts!")
        
        # Show some examples
        if deals:
            print("\\nReal Amazon discounts:")
            for deal in deals[:8]:
                if deal['discountPercent'] > 0:
                    print(f"- {deal['title'][:35]}: {deal['discountPercent']}% off (real Amazon discount)")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()