# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PromoPenguin is a React-based affiliate deals website that displays curated deals from RSS feeds. The site features automated deal scraping, deal validation, and static deployment on Vercel.

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

# Run the simple RSS scraper (no dependencies required)
python simple_scraper.py
```

## Architecture Overview

### Frontend Architecture
- **React SPA** with TypeScript using Create React App
- **State Management**: React hooks (useState, useEffect) - no external state management
- **Styling**: Tailwind CSS with dark theme and ice blue accents
- **Data Flow**: Fetches static `/public/deals.json` on load, displays in cards and modals
- **Key Components**:
  - `App.tsx`: Main orchestrator, handles deal loading and modal state
  - `DealCard.tsx`: Individual deal display with color rotation
  - `DealModal.tsx`: Popup for detailed deal view
  - `Sidebar.tsx`: Featured/top deals display
  - `Header.tsx`: Navigation and branding

### Backend Architecture
- **Data Pipeline**: RSS → Python Scraper → deals.json → Vercel
- **Scraper**: `simple_scraper.py` fetches from RSS feeds, enriches data, generates static JSON
- **Automation**: Direct RSS-to-JSON conversion with automated Git commits
- **Deal Management**: Automated scraping with built-in filtering and validation

### Key Data Flow
1. Scraper runs (manually or via cron/GitHub Actions)
2. Fetches deals from RSS feed or WordPress REST API
3. Validates affiliate links and extracts product data
4. Generates static `deals.json` file with enriched data
5. Git commit triggers Vercel deployment
6. Site updates with new deals automatically

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

- **Affiliate Links**: All Amazon links must use tag `promopenguin-20`
- **Color Scheme**: Cards rotate through pink (#EAB2AB), blue (#93C4D8), yellow (#FCE3AB)
- **Image Handling**: Placeholder SVG for missing images, lazy loading for performance
- **Price Display**: Always show both current and original price with discount percentage
- **Responsive Design**: Mobile-first approach, sidebar hidden on mobile
- **Static Deployment**: No backend server, all data served as static JSON

## Environment Variables & Secrets

### Optional GitHub Secrets
For customizing data sources, you can optionally add these secrets to your GitHub repository settings (Settings → Secrets and variables → Actions):

- `FEED_URL`: RSS feed URL to scrape (defaults to current feed)
- `WORDPRESS_BASE_URL`: WordPress site base URL for REST API access

To add these secrets:
1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret with the exact names above

The scraper works without any secrets using the default RSS feed configuration.

### Troubleshooting

#### GitHub Actions Dependency Issues
If the scraper fails in GitHub Actions due to dependency issues:
1. The workflow now includes `pip install --upgrade pip setuptools wheel` before installing requirements
2. Alternative `requirements-stable.txt` includes additional dependencies that oauth2client might need
3. Common problematic packages: `oauth2client` (deprecated but still used), `gspread`
4. To use alternative requirements: change `pip install -r requirements.txt` to `pip install -r requirements-stable.txt` in workflow