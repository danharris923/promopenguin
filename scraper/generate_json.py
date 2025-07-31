#!/usr/bin/env python3
"""
Generate deals.json from approved deals in Google Sheet
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
    print("Generating deals.json from approved deals...")
    
    try:
        scraper = SavingsGuruScraperEnv()
        deals = scraper.generate_deals_json()
        
        if deals:
            print(f"\nSuccessfully generated deals.json with {len(deals)} approved deals!")
            print("\nNext steps:")
            print("1. Commit and push to GitHub")
            print("2. Vercel will auto-deploy")
        else:
            print("\nNo approved deals found!")
            print("Please go to your Google Sheet and change some deals from 'pending' to 'approved'")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()