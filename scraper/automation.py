#!/usr/bin/env python3
"""
VPS Automation Script
Runs hourly to:
1. Fetch approved deals from Google Sheets
2. Generate deals.json
3. Commit and push to GitHub
"""

import os
import subprocess
import json
from datetime import datetime
from savingsguru_scraper import SavingsGuruScraper

def run_command(cmd):
    """Execute shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"Error: {result.stderr}")
    return result.stdout

def main():
    print(f"Starting automation run at {datetime.now()}")
    
    # Initialize scraper
    scraper = SavingsGuruScraper(
        credentials_file=os.environ.get('GOOGLE_CREDS_FILE', '../../google_service_account.json'),
        spreadsheet_id=os.environ.get('SPREADSHEET_ID', '1jkFjKFyOtv5zGw-l7ZF7H1i0e4MunSj3dP2bX7oA3zg')
    )
    
    # Generate deals.json from approved deals
    print("Fetching approved deals from Google Sheets...")
    deals = scraper.generate_deals_json(output_path='../public/deals.json')
    
    if not deals:
        print("No approved deals found. Exiting.")
        return
    
    # Git operations
    os.chdir('..')  # Move to project root
    
    # Check if there are changes
    status = run_command('git status --porcelain public/deals.json')
    
    if not status.strip():
        print("No changes to deals.json. Exiting.")
        return
    
    print("Changes detected. Committing and pushing...")
    
    # Add changes
    run_command('git add public/deals.json')
    
    # Commit with timestamp
    commit_msg = f"Update deals.json - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    run_command(f'git commit -m "{commit_msg}"')
    
    # Push to GitHub
    run_command('git push origin main')
    
    print("Successfully updated deals.json and pushed to GitHub!")
    print(f"Updated {len(deals)} deals")

if __name__ == "__main__":
    main()