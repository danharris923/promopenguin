# PromoPenguin - Canada's Premier Deals Platform 🐧

<div align="center">
  
  ![PromoPenguin](https://img.shields.io/badge/PromoPenguin-1.0-blue?style=for-the-badge)
  ![React](https://img.shields.io/badge/React-18.2-blue?style=for-the-badge&logo=react)
  ![TypeScript](https://img.shields.io/badge/TypeScript-4.9-blue?style=for-the-badge&logo=typescript)
  ![Vercel](https://img.shields.io/badge/Vercel-Deployed-black?style=for-the-badge&logo=vercel)
  
  **🚀 Automatically aggregating the hottest Amazon deals for Canadian shoppers**
  
  [Live Site](https://promopenguin.com) • [Report Bug](https://github.com/danharris923/promopenguin/issues)
  
</div>

---

## 🎯 The Mission

We're not just another deals site. PromoPenguin is on a mission to save Canadians millions by intelligently aggregating and curating the absolute best deals from across the web. Our automated platform works 24/7 so you never miss a legendary deal.

## ✨ What Makes Us Different

- **🤖 AI-Powered Curation** - Our scraper intelligently finds and validates real deals, not junk
- **⚡ Real-Time Updates** - New deals every hour, automatically deployed
- **🍁 Canada-First** - Built for Canadian shoppers, with Canadian prices
- **📱 Mobile-First Design** - Beautiful experience on any device
- **🔒 Safe & Secure** - All affiliate links validated, no sketchy redirects

## 🛠️ Tech Stack

### Frontend
- **React 18** with **TypeScript** for type-safe, blazing-fast UI
- **Tailwind CSS** for beautiful, responsive design
- **Framer Motion** for smooth animations
- **React Router** for seamless navigation

### Backend & Automation
- **Python Scraper** with BeautifulSoup for intelligent deal extraction
- **WordPress REST API** integration for content fetching
- **GitHub Actions** for automated hourly updates
- **Vercel** for instant global deployments

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/danharris923/promopenguin.git
cd promopenguin-modern

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## 📊 Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  WordPress API  │────▶│ Python       │────▶│ deals.json  │
│  (Source Deals) │     │ Scraper      │     │ (Static)    │
└─────────────────┘     └──────────────┘     └─────────────┘
                               │                     │
                               ▼                     ▼
                        ┌──────────────┐     ┌─────────────┐
                        │ GitHub       │────▶│ Vercel      │
                        │ Actions      │     │ (CDN)       │
                        └──────────────┘     └─────────────┘
                                                    │
                                                    ▼
                                            ┌─────────────┐
                                            │ React App   │
                                            │ (Users)     │
                                            └─────────────┘
```

## 🔄 Automated Deal Pipeline

1. **Scraper runs hourly** via GitHub Actions
2. **Fetches 200+ deals** from WordPress REST API
3. **Validates affiliate links** (Amazon with proper tags, ShopStyle)
4. **Generates static JSON** with prices, images, descriptions
5. **Commits to GitHub** triggering automatic deployment
6. **Vercel deploys globally** in under 30 seconds
7. **Users see fresh deals** without any manual intervention

## 🎨 Design Philosophy

- **Speed First**: Static generation means instant load times
- **Clean & Modern**: Inspired by top e-commerce experiences
- **Accessible**: WCAG compliant, works for everyone
- **Delightful**: Smooth animations and interactions

## 📈 Performance Metrics

- ⚡ **< 1s** First Contentful Paint
- 🚀 **100/100** Lighthouse Performance Score
- 📱 **60fps** Smooth scrolling on all devices
- 🌍 **Global CDN** via Vercel's edge network

## 🤝 Contributing

We believe in building in public! Contributions are welcome:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

MIT License - feel free to use this code for your own projects!

## 🙏 Acknowledgments

- Built with React & Create React App
- Deployed on Vercel's incredible platform
- Inspired by the Canadian deal-hunting community

---

<div align="center">
  
  **Built with ❤️ for Canadian shoppers**
  
  [Visit PromoPenguin](https://promopenguin.com)
  
</div>