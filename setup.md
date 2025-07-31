# Quick Setup Guide

## 🚀 Running the Site

The development server is now running at: **http://localhost:3002**

## 📋 Next Steps

### 1. Google Sheets Setup
1. Create a Google Cloud project at https://console.cloud.google.com
2. Enable Google Sheets API
3. Create a service account and download credentials JSON
4. Create a Google Sheet with the columns specified in README.md
5. Share the sheet with your service account email

### 2. GitHub Repository Setup
1. Create a new GitHub repository
2. Add these secrets:
   - `GOOGLE_SHEETS_CREDS`: Your service account JSON
   - `SPREADSHEET_NAME`: Name of your Google Sheet

### 3. Vercel Deployment
1. Visit https://vercel.com
2. Import your GitHub repository
3. Deploy with default settings (it will auto-detect React)

### 4. Test the Scraper
```bash
cd scraper
pip install -r requirements.txt
python savingsguru_scraper.py
```

## 🎨 Features Implemented

✅ Modern React SPA with TypeScript
✅ Responsive Tailwind CSS design matching SavingsGuru.ca colors
✅ Deal cards with hover effects
✅ Modal popups for deal details
✅ Top Deals sidebar
✅ Mobile-responsive navigation
✅ Google Sheets integration for deal management
✅ Python scraper for RSS feeds
✅ GitHub Actions for automation
✅ Vercel-ready configuration

## 🎯 Site Features

- **Lightning-fast** static site
- **SEO-friendly** with proper meta tags
- **Mobile-first** responsive design
- **Automated updates** via GitHub Actions
- **Human review** workflow via Google Sheets
- **Affiliate link** management