#!/usr/bin/env python3
"""
Helper script to manage deals in Google Sheets
"""

import os
from savingsguru_scraper import SavingsGuruScraper
from datetime import datetime

def approve_sample_deals():
    """Approve some sample deals for testing"""
    scraper = SavingsGuruScraper(
        credentials_file='../../google_service_account.json',
        spreadsheet_id='1jkFjKFyOtv5zGw-l7ZF7H1i0e4MunSj3dP2bX7oA3zg'
    )
    
    # Get all records
    records = scraper.sheet.get_all_records()
    print(f"Found {len(records)} deals in the sheet")
    
    if len(records) == 0:
        print("No deals found. Run the scraper first.")
        return
    
    # Approve first 10 deals and add sample data
    print("Updating deals with sample data...")
    
    # Sample images and prices for testing
    sample_data = [
        {"image": "https://m.media-amazon.com/images/I/81vF8pFhOGL._AC_SX679_.jpg", "price": 89.99, "orig": 149.99},
        {"image": "https://m.media-amazon.com/images/I/71qJzK9mOFL._AC_SX679_.jpg", "price": 3.99, "orig": 5.49},
        {"image": "https://m.media-amazon.com/images/I/81Y9KvGLqnL._AC_SX679_.jpg", "price": 4.49, "orig": 6.99},
        {"image": "https://m.media-amazon.com/images/I/71bXyH9hGFL._AC_SX679_.jpg", "price": 119.99, "orig": 199.99},
        {"image": "https://m.media-amazon.com/images/I/61mSEaQ8YzL._AC_SX679_.jpg", "price": 24.99, "orig": 39.99},
        {"image": "https://m.media-amazon.com/images/I/81mKTnHBfPL._AC_SX679_.jpg", "price": 39.99, "orig": 59.99},
        {"image": "https://m.media-amazon.com/images/I/71zJ5JqVOvL._AC_SX679_.jpg", "price": 32.99, "orig": 52.99},
        {"image": "https://m.media-amazon.com/images/I/71cCx7JuOzL._AC_SX679_.jpg", "price": 189.99, "orig": 299.99},
        {"image": "https://m.media-amazon.com/images/I/71UVYGdPgJL._AC_SX679_.jpg", "price": 16.99, "orig": 24.99},
        {"image": "https://m.media-amazon.com/images/I/71wO+pEKHsL._AC_SX679_.jpg", "price": 22.99, "orig": 34.99}
    ]
    
    # Update each row
    for i, record in enumerate(records[:10]):
        row_num = i + 2  # +2 because row 1 is header, and sheets are 1-indexed
        
        if i < len(sample_data):
            data = sample_data[i]
            # Calculate discount
            discount = int((1 - data["price"] / data["orig"]) * 100)
            
            # Update cells
            scraper.sheet.update_cell(row_num, 5, data["price"])  # Price
            scraper.sheet.update_cell(row_num, 6, data["orig"])   # Original Price
            scraper.sheet.update_cell(row_num, 7, discount)       # Discount %
            scraper.sheet.update_cell(row_num, 8, data["image"])  # Image URL
            scraper.sheet.update_cell(row_num, 11, "approved")    # Status
            
            # Mark first 4 as featured
            if i < 4:
                scraper.sheet.update_cell(row_num, 13, "featured")  # Notes
            
            print(f"Updated row {row_num}: {record['Title'][:50]}...")
    
    print("\nGenerating new deals.json...")
    approved_deals = scraper.generate_deals_json()
    
    print(f"\nDone! {len(approved_deals)} deals are now approved and available.")
    print("Visit http://localhost:3002 to see the updated deals!")

if __name__ == "__main__":
    approve_sample_deals()