# GitHub Secrets Setup for SavingsGuru

## Required Secrets

You need to add these two secrets to your GitHub repository:

### 1. GOOGLE_SHEETS_CREDS
This is your entire Google service account JSON file content.

**How to add:**
1. Open your `google_service_account.json` file in a text editor
2. Select ALL content (Ctrl+A) and copy it
3. Go to your GitHub repo: https://github.com/danharris923/savingsguru.cc
4. Click **Settings** → **Secrets and variables** → **Actions**
5. Click **New repository secret**
6. Name: `GOOGLE_SHEETS_CREDS`
7. Value: Paste the entire JSON content
8. Click **Add secret**

### 2. SPREADSHEET_ID
This is your Google Sheet ID.

**How to find:**
1. Open your Google Sheet
2. Look at the URL: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
3. Copy the ID part (between `/d/` and `/edit`)

**How to add:**
1. In GitHub Settings → Secrets → Actions
2. Click **New repository secret**
3. Name: `SPREADSHEET_ID`
4. Value: Your sheet ID (e.g., `1jkFjKFyOtv5zGw-l7ZF7H1i0e4MunSj3dP2bX7oA3zg`)
5. Click **Add secret**

## Testing Locally First

Before committing, test locally using PowerShell:

```powershell
cd scraper
.\test_env_locally.ps1
```

This will:
1. Load your local credentials file
2. Prompt for your Spreadsheet ID
3. Run the scraper
4. Populate your Google Sheet with real deals

## What Happens Next

1. **Local Testing**: Run the scraper locally to populate your sheet
2. **Review Deals**: Go to your Google Sheet and change Status from "pending" to "approved" for good deals
3. **Generate JSON**: Run the script again to create `deals.json` with approved deals
4. **Commit & Push**: Push your changes to GitHub
5. **GitHub Actions**: Will run hourly to update deals automatically
6. **Vercel**: Will auto-deploy when `deals.json` changes

## Troubleshooting

**"Authentication failed"**
- Make sure you shared your Google Sheet with the service account email
- Check that both Google Sheets API and Google Drive API are enabled

**"Spreadsheet not found"**
- Verify the SPREADSHEET_ID is correct
- Ensure the service account has edit access to the sheet

**GitHub Action fails**
- Check the Actions tab for error logs
- Verify both secrets are set correctly
- Make sure there are no extra spaces or quotes in the secrets