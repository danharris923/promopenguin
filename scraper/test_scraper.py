#!/usr/bin/env python3
"""
Test script to run the scraper and populate Google Sheets with real deals
"""

import os
import sys
from savingsguru_scraper import SavingsGuruScraper

def main():
    # Check for credentials
    creds_file = os.environ.get('GOOGLE_CREDS_FILE', '../credentials/google_service_account.json')
    sheet_id = os.environ.get('SPREADSHEET_ID')
    
    if not os.path.exists(creds_file):
        print("❌ ERROR: Google credentials file not found!")
        print(f"   Looking for: {creds_file}")
        print("\n📋 Please follow these steps:")
        print("1. Create a Google Cloud project")
        print("2. Enable Google Sheets API")
        print("3. Create a service account")
        print("4. Download the JSON credentials")
        print("5. Save as: credentials/google_service_account.json")
        print("\nSee GOOGLE_SHEETS_SETUP.md for detailed instructions")
        return
    
    if not sheet_id:
        print("❌ ERROR: SPREADSHEET_ID not set!")
        print("\n📋 Please set the environment variable:")
        print("   Windows: $env:SPREADSHEET_ID = 'your-sheet-id'")
        print("   Linux/Mac: export SPREADSHEET_ID='your-sheet-id'")
        return
    
    print("🚀 Starting SavingsGuru scraper...")
    print(f"📄 Using credentials: {creds_file}")
    print(f"📊 Sheet ID: {sheet_id}")
    
    try:
        # Initialize scraper
        scraper = SavingsGuruScraper(
            credentials_file=creds_file,
            spreadsheet_id=sheet_id
        )
        
        print("\n📡 Fetching deals from RSS feed...")
        # This will fetch real deals and populate your Google Sheet
        scraper.update_sheet_from_rss()
        
        print("\n✅ Success! Check your Google Sheet for new deals")
        print("📝 Next steps:")
        print("1. Review deals in Google Sheet")
        print("2. Change Status to 'approved' for good deals")
        print("3. Run 'python automation.py' to generate deals.json")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n🔧 Common issues:")
        print("- Make sure the service account email has edit access to your sheet")
        print("- Check that Google Sheets API is enabled in your project")
        print("- Verify your credentials JSON file is valid")

if __name__ == "__main__":
    main()