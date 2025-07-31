#!/usr/bin/env python3
"""
Update all existing deals to approved status and generate deals.json
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
import time

def main():
    print("Updating all deals to approved status...")
    
    try:
        scraper = SavingsGuruScraperEnv()
        
        # Get all data
        all_data = scraper.sheet.get_all_values()
        
        if len(all_data) <= 1:
            print("No deals found in sheet")
            return
        
        # Find status column index (should be column K, index 10)
        headers = all_data[0]
        status_col = headers.index('Status') if 'Status' in headers else 10
        
        # Update all deals to approved
        updated_count = 0
        for i, row in enumerate(all_data[1:], start=2):  # Start from row 2 (after header)
            if len(row) > status_col and row[status_col] != 'approved':
                # Update status to approved
                scraper.sheet.update_cell(i, status_col + 1, 'approved')  # +1 because sheets are 1-indexed
                updated_count += 1
                time.sleep(0.5)  # Rate limiting
        
        print(f"Updated {updated_count} deals to approved status")
        
        # Generate deals.json
        print("\nGenerating deals.json...")
        deals = scraper.generate_deals_json()
        
        print(f"\nSuccessfully generated deals.json with {len(deals)} deals!")
        print("\nYour site now has real deals! Next:")
        print("1. git add -A")
        print("2. git commit -m 'Add real deals from SavingsGuru'")
        print("3. git push")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()