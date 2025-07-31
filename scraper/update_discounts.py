#!/usr/bin/env python3
"""
Update existing deals with corrected discount percentages
"""

import os
import sys
from pathlib import Path

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
    print("Updating discount percentages for existing deals...")
    
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
        price_col = headers.index('Price') if 'Price' in headers else 4
        original_price_col = headers.index('Original Price') if 'Original Price' in headers else 5
        discount_col = headers.index('Discount %') if 'Discount %' in headers else 6
        
        updated_count = 0
        
        # Process each deal (skip header)
        for i, row in enumerate(all_data[1:], start=2):  # Start from row 2
            if len(row) > original_price_col:
                deal_title = row[1] if len(row) > 1 else f"Deal {i-1}"
                current_price = float(row[price_col]) if len(row) > price_col and row[price_col] else 0
                original_price = float(row[original_price_col]) if len(row) > original_price_col and row[original_price_col] else 0
                
                # Calculate correct discount percentage
                if current_price > 0 and original_price > current_price:
                    correct_discount = int(((original_price - current_price) / original_price) * 100)
                    
                    print(f"\\nUpdating row {i}: {deal_title[:30]}...")
                    print(f"Price: ${current_price}, Original: ${original_price}")
                    print(f"Calculated discount: {correct_discount}%")
                    
                    # Update the sheet with correct discount
                    scraper.sheet.update_cell(i, discount_col + 1, correct_discount)  # +1 for 1-based indexing
                    
                    updated_count += 1
                else:
                    print(f"Skipping {deal_title[:30]} - no valid price data")
        
        print(f"\\nUpdated {updated_count} deals with correct discount percentages!")
        
        # Now regenerate deals.json
        print("\\nRegenerating deals.json with correct discounts...")
        deals = scraper.generate_deals_json()
        print(f"Generated deals.json with {len(deals)} deals and real discount percentages!")
        
        # Show some examples
        if deals:
            print("\\nExample discounts:")
            for deal in deals[:5]:
                if deal['discountPercent'] > 0:
                    print(f"- {deal['title'][:40]}: {deal['discountPercent']}% off")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()