#!/usr/bin/env python3
"""
Simple script to run the scraper and populate Google Sheets with real deals
"""

import os
import sys
from savingsguru_scraper import SavingsGuruScraper

def main():
    # Check for credentials
    creds_file = os.environ.get('GOOGLE_CREDS_FILE', '../credentials/google_service_account.json')
    sheet_id = os.environ.get('SPREADSHEET_ID')
    
    if not os.path.exists(creds_file):
        print("ERROR: Google credentials file not found!")
        print(f"Looking for: {creds_file}")
        print("\nPlease follow these steps:")
        print("1. Create credentials folder in project root")
        print("2. Add your google_service_account.json file")
        print("See GOOGLE_SHEETS_SETUP.md for details")
        return
    
    if not sheet_id:
        print("ERROR: SPREADSHEET_ID not set!")
        print("\nPlease set the environment variable:")
        print("Windows PowerShell: $env:SPREADSHEET_ID = 'your-sheet-id'")
        print("Windows CMD: set SPREADSHEET_ID=your-sheet-id")
        return
    
    print("Starting SavingsGuru scraper...")
    print(f"Using credentials: {creds_file}")
    print(f"Sheet ID: {sheet_id}")
    
    try:
        # Initialize scraper
        scraper = SavingsGuruScraper(
            credentials_file=creds_file,
            spreadsheet_id=sheet_id
        )
        
        print("\nFetching deals from RSS feed...")
        # This will fetch real deals and populate your Google Sheet
        scraper.update_sheet_from_rss()
        
        print("\nSuccess! Check your Google Sheet for new deals")
        print("Next steps:")
        print("1. Review deals in Google Sheet")
        print("2. Change Status to 'approved' for good deals")
        print("3. Run 'python automation.py' to generate deals.json")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting:")
        print("- Make sure the service account email has edit access to your sheet")
        print("- Check that Google Sheets API is enabled")
        print("- Verify your credentials JSON file is valid")

if __name__ == "__main__":
    main()