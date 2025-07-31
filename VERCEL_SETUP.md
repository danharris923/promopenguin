# Vercel Deployment Setup Guide

## Quick Start

### 1. Deploy to Vercel (One-Click)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/savingsguru-modern)

### 2. Manual Setup

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```

3. **Connect GitHub for Auto-Deploy**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will auto-detect Create React App settings

## GitHub Secrets Setup

Add these secrets to your GitHub repository (Settings → Secrets → Actions):

1. **GOOGLE_SHEETS_CREDS**
   - Your Google service account JSON (entire contents)
   - Get from Google Cloud Console → Service Accounts

2. **SPREADSHEET_ID**
   - Your Google Sheets ID
   - Find in sheet URL: `docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`

## Architecture Overview

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  GitHub Actions │────►│ Google Sheets│────►│ deals.json  │
│  (Hourly Cron) │     │   (Review)   │     │  (in repo)  │
└─────────────────┘     └──────────────┘     └──────┬───────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │   Vercel    │
                                              │ (Auto-Deploy)│
                                              └─────────────┘
```

## How It Works

1. **GitHub Actions** runs the Python scraper hourly
2. **Scraper** fetches deals from RSS feeds
3. **Google Sheets** stores deals for human review
4. **Automation** generates `deals.json` from approved deals
5. **Git commit** triggers Vercel auto-deployment
6. **Site updates** within seconds globally

## Initial Setup Checklist

- [ ] Fork/clone this repository
- [ ] Create Google Cloud project & enable Sheets API
- [ ] Create service account & download JSON credentials
- [ ] Create Google Sheet with required columns
- [ ] Share sheet with service account email
- [ ] Add GitHub secrets (GOOGLE_SHEETS_CREDS, SPREADSHEET_ID)
- [ ] Deploy to Vercel
- [ ] Enable GitHub Actions in your repo
- [ ] Test manual workflow run

## Testing the Setup

1. **Test GitHub Action Manually**
   - Go to Actions tab in GitHub
   - Click "Update Deals" workflow
   - Click "Run workflow"
   - Check for green checkmark

2. **Verify Deployment**
   - Check Vercel dashboard for successful deployment
   - Visit your site URL
   - Confirm deals are displaying

## Troubleshooting

**GitHub Action fails:**
- Check secrets are properly set
- Verify Google Sheets permissions
- Check Actions logs for specific errors

**No deals showing:**
- Ensure deals are marked "approved" in Google Sheets
- Check `public/deals.json` exists and has content
- Verify GitHub Action ran successfully

**Vercel deployment fails:**
- Check build logs in Vercel dashboard
- Ensure `vercel.json` is present
- Verify no build errors locally with `npm run build`