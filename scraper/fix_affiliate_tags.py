#!/usr/bin/env python3
"""
Fix affiliate tags in Google Sheet from saviguru-20 to savingsgurucc-20
"""

from savingsguru_scraper import SavingsGuruScraper

def fix_affiliate_tags():
    """Update all affiliate tags in the sheet"""
    scraper = SavingsGuruScraper(
        credentials_file='../../google_service_account.json',
        spreadsheet_id='1jkFjKFyOtv5zGw-l7ZF7H1i0e4MunSj3dP2bX7oA3zg'
    )
    
    # Get all records
    records = scraper.sheet.get_all_records()
    print(f"Found {len(records)} deals to update")
    
    # Update each row
    for i, record in enumerate(records):
        row_num = i + 2  # +2 because row 1 is header, and sheets are 1-indexed
        
        # Get current Amazon URL
        amazon_url = record.get('Amazon URL', '')
        
        # Replace the affiliate tag
        if 'saviguru-20' in amazon_url:
            new_url = amazon_url.replace('saviguru-20', 'savingsgurucc-20')
            scraper.sheet.update_cell(row_num, 4, new_url)  # Column 4 is Amazon URL
            print(f"Updated row {row_num}: {record['Title'][:30]}...")
        elif 'tag=' in amazon_url and 'savingsgurucc-20' not in amazon_url:
            # Fix any other incorrect tags
            import re
            new_url = re.sub(r'tag=[^&]+', 'tag=savingsgurucc-20', amazon_url)
            scraper.sheet.update_cell(row_num, 4, new_url)
            print(f"Fixed tag in row {row_num}: {record['Title'][:30]}...")
    
    print("\nRegenerating deals.json with corrected tags...")
    scraper.generate_deals_json()
    
    print("Done! All affiliate tags have been updated to savingsgurucc-20")

if __name__ == "__main__":
    fix_affiliate_tags()