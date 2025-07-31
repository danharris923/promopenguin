# Google Sheets Setup Guide

## Quick Setup Steps

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Create Project" 
3. Name it "SavingsGuru Scraper"

### 2. Enable Google Sheets API
1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Sheets API"
3. Click on it and press "Enable"
4. Also search and enable "Google Drive API"

### 3. Create Service Account
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name: "savingsguru-scraper"
4. Click "Create and Continue"
5. Skip optional steps, click "Done"

### 4. Download Credentials
1. Click on your service account email
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Save the downloaded file as `google_service_account.json`

### 5. Create Google Sheet
1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it "SavingsGuru Deals"
4. Add these column headers in row 1:
   - A1: ID
   - B1: Title
   - C1: Original URL
   - D1: Amazon URL
   - E1: Price
   - F1: Original Price
   - G1: Discount %
   - H1: Image URL
   - I1: Description
   - J1: Category
   - K1: Status
   - L1: Date Added
   - M1: Notes

### 6. Share Sheet with Service Account
1. In your Google Sheet, click "Share" button
2. Copy the service account email from your JSON file (looks like: savingsguru-scraper@project-name.iam.gserviceaccount.com)
3. Paste the email and give "Editor" access
4. Click "Send"

### 7. Get Sheet ID
1. Look at your Google Sheet URL
2. Copy the ID between `/d/` and `/edit`
3. Example: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit`

## Running the Scraper Locally

1. **Create credentials folder:**
   ```bash
   mkdir credentials
   ```

2. **Copy your JSON file:**
   ```bash
   cp ~/Downloads/google_service_account.json credentials/
   ```

3. **Set environment variables (Windows PowerShell):**
   ```powershell
   $env:GOOGLE_CREDS_FILE = "credentials/google_service_account.json"
   $env:SPREADSHEET_ID = "YOUR_SHEET_ID_HERE"
   ```

4. **Run the scraper:**
   ```bash
   cd scraper
   python savingsguru_scraper.py
   ```

## GitHub Secrets for Automation

Add these to your GitHub repo (Settings → Secrets → Actions):

1. **GOOGLE_SHEETS_CREDS**: 
   - Open your `google_service_account.json` file
   - Copy the ENTIRE contents
   - Paste as the secret value

2. **SPREADSHEET_ID**:
   - Your Google Sheet ID from step 7

## Verify It's Working

After running the scraper:
1. Check your Google Sheet - it should have new deals
2. Review and approve deals by setting Status to "approved"
3. Run `python automation.py` to generate deals.json
4. Check `public/deals.json` has real data