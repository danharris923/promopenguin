# PowerShell script to test scraper with environment variables locally

Write-Host "Setting up environment variables for testing..." -ForegroundColor Green

# Check if credentials file exists
$credsFile = "../credentials/google_service_account.json"
if (Test-Path $credsFile) {
    # Read the JSON file content
    $env:GOOGLE_SHEETS_CREDS = Get-Content $credsFile -Raw
    Write-Host "✓ Loaded credentials from file" -ForegroundColor Green
} else {
    Write-Host "✗ Credentials file not found at: $credsFile" -ForegroundColor Red
    Write-Host "Please add your google_service_account.json to the credentials folder" -ForegroundColor Yellow
    exit 1
}

# Prompt for spreadsheet ID if not set
if (-not $env:SPREADSHEET_ID) {
    $spreadsheetId = Read-Host "Enter your Google Spreadsheet ID"
    $env:SPREADSHEET_ID = $spreadsheetId
} else {
    Write-Host "✓ Using existing SPREADSHEET_ID: $env:SPREADSHEET_ID" -ForegroundColor Green
}

Write-Host "`nRunning scraper..." -ForegroundColor Cyan
python scraper_env.py

Write-Host "`nDone! Check your Google Sheet for new deals." -ForegroundColor Green