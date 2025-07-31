#!/bin/bash
# Bash script to test scraper with environment variables locally

echo -e "\033[32mSetting up environment variables for testing...\033[0m"

# Check if credentials file exists
CREDS_FILE="../credentials/google_service_account.json"
if [ -f "$CREDS_FILE" ]; then
    # Read the JSON file content
    export GOOGLE_SHEETS_CREDS=$(cat "$CREDS_FILE")
    echo -e "\033[32m✓ Loaded credentials from file\033[0m"
else
    echo -e "\033[31m✗ Credentials file not found at: $CREDS_FILE\033[0m"
    echo -e "\033[33mPlease add your google_service_account.json to the credentials folder\033[0m"
    exit 1
fi

# Prompt for spreadsheet ID if not set
if [ -z "$SPREADSHEET_ID" ]; then
    read -p "Enter your Google Spreadsheet ID: " SPREADSHEET_ID
    export SPREADSHEET_ID="$SPREADSHEET_ID"
else
    echo -e "\033[32m✓ Using existing SPREADSHEET_ID: $SPREADSHEET_ID\033[0m"
fi

echo -e "\n\033[36mRunning scraper...\033[0m"
python scraper_env.py

echo -e "\n\033[32mDone! Check your Google Sheet for new deals.\033[0m"