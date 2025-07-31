#!/usr/bin/env python3
"""
Test Google Sheets integration with the provided credentials
"""

import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def test_google_sheets():
    try:
        # Setup credentials
        credentials_file = '../../google_service_account.json'
        sheet_id = '1jkFjKFyOtv5zGw-l7ZF7H1i0e4MunSj3dP2bX7oA3zg'
        
        print(f"Using credentials file: {credentials_file}")
        print(f"Connecting to sheet ID: {sheet_id}")
        
        # Google Sheets setup
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(creds)
        
        # Open the sheet by ID
        sheet = client.open_by_key(sheet_id).sheet1
        
        print("Successfully connected to Google Sheet!")
        
        # Get current data
        all_records = sheet.get_all_records()
        print(f"Current number of rows: {len(all_records)}")
        
        # Check if headers exist
        if len(all_records) == 0:
            print("Sheet is empty. Adding headers...")
            headers = ['ID', 'Title', 'Original URL', 'Amazon URL', 'Price', 
                       'Original Price', 'Discount %', 'Image URL', 'Description', 
                       'Category', 'Status', 'Date Added', 'Notes']
            sheet.append_row(headers)
            print("Headers added successfully!")
        else:
            print("Sheet already has data.")
            
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_google_sheets()