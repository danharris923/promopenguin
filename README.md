# SavingsGuru Modern - React Affiliate Deals Site

A modern, lightning-fast affiliate deals site inspired by SavingsGuru.ca, built with React and Tailwind CSS.

## Features

- **Modern React SPA** with TypeScript
- **Tailwind CSS** for responsive, pixel-perfect design
- **Static deployment** on Vercel for blazing-fast performance
- **Google Sheets integration** for deal management
- **Automated scraping** and content updates via GitHub Actions
- **Mobile-first** responsive design
- **Deal modal popups** with smooth animations
- **Top deals sidebar** with featured products

## Tech Stack

- **Frontend**: React 18, TypeScript, Tailwind CSS
- **Deployment**: Vercel (static hosting)
- **Backend Automation**: Python scraper + Google Sheets API
- **CI/CD**: GitHub Actions for hourly updates
- **Data Storage**: JSON file (generated from Google Sheets)

## Project Structure

```
savingsguru-modern/
├── src/
│   ├── components/       # React components
│   ├── types/           # TypeScript interfaces
│   ├── App.tsx          # Main app component
│   └── index.css        # Tailwind imports
├── public/
│   └── deals.json       # Static deals data
├── scraper/
│   ├── savingsguru_scraper.py  # Main scraper logic
│   ├── automation.py    # VPS automation script
│   └── requirements.txt # Python dependencies
└── .github/workflows/   # GitHub Actions
```

## Setup Instructions

### 1. Frontend Development

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### 2. Google Sheets Setup

1. Create a Google Cloud project
2. Enable Google Sheets API
3. Create service account credentials
4. Share your Google Sheet with the service account email
5. Add credentials as GitHub secret: `GOOGLE_SHEETS_CREDS`

### 3. Vercel Deployment

1. Connect GitHub repo to Vercel
2. Set framework preset to "Create React App"
3. Deploy with automatic updates on push

### 4. VPS Automation (Optional)

For VPS-based automation instead of GitHub Actions:

```bash
# Install dependencies
cd scraper
pip install -r requirements.txt

# Set up cron job (runs hourly)
crontab -e
0 * * * * cd /path/to/project/scraper && python automation.py
```

## Environment Variables

### GitHub Secrets
- `GOOGLE_SHEETS_CREDS`: Service account JSON credentials
- `SPREADSHEET_NAME`: Name of your Google Sheet

### Local Development
Create `.env.local`:
```
REACT_APP_API_URL=http://localhost:3000
```

## Google Sheets Format

Your Google Sheet should have these columns:
- ID
- Title
- Original URL
- Amazon URL
- Price
- Original Price
- Discount %
- Image URL
- Description
- Category
- Status (pending/approved/rejected)
- Date Added
- Notes (use "featured" for top deals)

## Workflow

1. **Scraper** runs hourly, fetches deals from SavingsGuru RSS
2. **Google Sheets** populated with new deals (status: pending)
3. **Human review** - approve deals, edit titles/images
4. **Automation** fetches approved deals, generates deals.json
5. **GitHub push** triggers Vercel deployment
6. **Site updates** with new deals automatically

## Color Scheme

Matched from SavingsGuru.ca:
- Primary Green: `#7AB857`
- Accent Yellow: `#FCD144`
- Card backgrounds: Pink `#EAB2AB`, Blue `#93C4D8`, Yellow `#FCE3AB`

## License

This project is for educational purposes. Ensure you have permission to scrape content and use appropriate affiliate tags.