#!/usr/bin/env python3
"""
Update all existing deal descriptions in Google Sheet with snappy SEO-friendly descriptions
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
    print("Updating all existing descriptions with SEO-friendly content...")
    
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
        title_col = headers.index('Title') if 'Title' in headers else 1
        description_col = headers.index('Description') if 'Description' in headers else 8
        
        updated_count = 0
        
        # Process each deal (skip header)
        for i, row in enumerate(all_data[1:], start=2):  # Start from row 2
            if len(row) > max(title_col, description_col):
                deal_title = row[title_col] if len(row) > title_col else f"Deal {i-1}"
                current_description = row[description_col] if len(row) > description_col else ""
                
                # Check if description needs updating (contains HTML tags or old RSS content)
                if current_description and ("<p>" in current_description or "&#8230;" in current_description or "savingsguru.ca" in current_description or "**If you" in current_description or "<a href" in current_description):
                    print(f"\nUpdating row {i}: {deal_title[:40]}...")
                    
                    # Generate new SEO-friendly description
                    new_description = scraper.clean_description(current_description, deal_title)
                    
                    # Update the sheet with new description
                    scraper.sheet.update_cell(i, description_col + 1, new_description)  # +1 for 1-based indexing
                    
                    updated_count += 1
                    
                    # Rate limiting to avoid hitting API limits
                    time.sleep(2)
                else:
                    print(f"Skipping {deal_title[:30]} - description looks good")
        
        print(f"\nUpdated {updated_count} deal descriptions with SEO-friendly content!")
        
        # Now regenerate deals.json
        print("\nRegenerating deals.json with updated descriptions...")
        deals = scraper.generate_deals_json('../public/deals.json')
        print(f"Generated deals.json with {len(deals)} deals and snappy descriptions!")
        
        # Show some examples
        if deals:
            print("\nSample SEO-friendly descriptions:")
            for deal in deals[:5]:
                if not deal['description'].startswith('<p>'):
                    # Remove emojis for display to avoid Unicode issues
                    display_desc = deal['description'].encode('ascii', 'ignore').decode('ascii')
                    print(f"- {deal['title'][:30]}: {display_desc[:100]}...")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()