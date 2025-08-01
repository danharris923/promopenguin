# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SavingsGuru Modern is a React-based affiliate deals website that displays curated deals from Google Sheets. The site features automated deal scraping, human review workflow, and static deployment on Vercel.

## Common Development Commands

### Frontend Development
```bash
# Install dependencies
npm install

# Start development server (runs on port 3002)
npm start

# Build for production
npm run build

# Run tests
npm test

# Type checking (TypeScript)
npx tsc --noEmit

# Note: This project uses Create React App with built-in ESLint configuration
# Linting runs automatically during development with npm start
```

### Python Scraper
```bash
cd scraper

# Install Python dependencies
pip install -r requirements.txt

# Run the main scraper (requires environment variables)
python scraper_env.py

# Run automation script (fetches deals and updates Git)
python automation.py

# Run REST API scraper
python rest_api_scraper.py

# Run scraper with environment variables
python run_scraper_with_env.py
python run_with_env.py
```

## Architecture Overview

### Frontend Architecture
- **React SPA** with TypeScript using Create React App
- **State Management**: React hooks (useState, useEffect) - no external state management
- **Styling**: Tailwind CSS with custom color scheme matching SavingsGuru.ca
- **Data Flow**: Fetches static `/public/deals.json` on load, displays in cards and modals
- **Key Components**:
  - `App.tsx`: Main orchestrator, handles deal loading and modal state
  - `DealCard.tsx`: Individual deal display with color rotation
  - `DealModal.tsx`: Popup for detailed deal view
  - `Sidebar.tsx`: Featured/top deals display
  - `Header.tsx`: Navigation and branding

### Backend Architecture
- **Data Pipeline**: RSS → Python Scraper → Google Sheets → Human Review → deals.json → Vercel
- **Scraper**: `savingsguru_scraper.py` fetches from SavingsGuru RSS, enriches data, writes to Google Sheets
- **Automation**: `automation.py` reads approved deals from Sheets, generates deals.json, commits to Git
- **Deal Management**: Google Sheets acts as CMS with pending/approved/rejected workflow

### Key Data Flow
1. Scraper runs (manually or via cron/GitHub Actions)
2. New deals added to Google Sheets as "pending"
3. Human reviews and approves deals in Sheets
4. Automation script fetches approved deals
5. Generates static `deals.json` file
6. Git commit triggers Vercel deployment
7. Site updates with new deals

### Deal Data Structure
```typescript
interface Deal {
  id: string;
  title: string;
  imageUrl: string;
  price: number;
  originalPrice: number;
  discountPercent: number;
  category: string;
  description: string;
  affiliateUrl: string;
  featured?: boolean;
  dateAdded: string;
}
```

## Important Implementation Details

- **Affiliate Links**: All Amazon links must use tag `savingsguru0a-20`
- **Color Scheme**: Cards rotate through pink (#EAB2AB), blue (#93C4D8), yellow (#FCE3AB)
- **Image Handling**: Placeholder SVG for missing images, lazy loading for performance
- **Price Display**: Always show both current and original price with discount percentage
- **Responsive Design**: Mobile-first approach, sidebar hidden on mobile
- **Static Deployment**: No backend server, all data served as static JSON

## Environment Variables & Secrets

### Required GitHub Secrets
**IMPORTANT**: These secrets must be added to your GitHub repository settings (Settings → Secrets and variables → Actions) for the workflow to run:

- `GOOGLE_SHEETS_CREDS`: Service account JSON credentials for Google Sheets API (entire JSON file contents)
- `SPREADSHEET_ID`: The ID of your Google Sheet containing deals

To add these secrets:
1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret with the exact names above

#### Getting Google Sheets Credentials:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Sheets API
4. Create a Service Account (APIs & Services → Credentials → Create Credentials → Service Account)
5. Download the JSON key file
6. Copy the entire contents of the JSON file as the `GOOGLE_SHEETS_CREDS` secret
7. Share your Google Sheet with the service account email (found in the JSON file)

#### Finding your Spreadsheet ID:
The spreadsheet ID is in the URL of your Google Sheet:
`https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`

### Troubleshooting

#### GitHub Actions Dependency Issues
If the scraper fails in GitHub Actions due to dependency issues:
1. The workflow now includes `pip install --upgrade pip setuptools wheel` before installing requirements
2. Alternative `requirements-stable.txt` includes additional dependencies that oauth2client might need
3. Common problematic packages: `oauth2client` (deprecated but still used), `gspread`
4. To use alternative requirements: change `pip install -r requirements.txt` to `pip install -r requirements-stable.txt` in workflow