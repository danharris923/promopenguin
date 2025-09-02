import React from 'react';
import { Deal } from '../types/Deal';

interface SidebarProps {
  topDeals: Deal[];
  onDealClick: (deal: Deal) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ topDeals, onDealClick }) => {
  // Custom news items - easily configurable
  const newsItems = [
    {
      title: "Lululemon We Made Too Much SALE 🔥",
      url: "https://shopstyle.it/l/cj22Z",
      logo: "https://logo.clearbit.com/lululemon.com",
      fallbackText: "L",
      timeAgo: "2 hours ago"
    },
    {
      title: "Gap SALE - Up to 70% Off Everything 💥", 
      url: "https://shopstyle.it/l/cj24C",
      logo: "https://logo.clearbit.com/gap.com",
      fallbackText: "G",
      timeAgo: "4 hours ago"
    },
    {
      title: "Cabela's Fall Classic SALE 🍂",
      url: "https://www.basspro.ca/home?utm_source=RAN&utm_medium=affiliate&utm_content=Living+off+the+GRID+in+Canada&ranMID=50435&ranEAID=sUVpAjRtGL4&ranSiteID=sUVpAjRtGL4-Ycc1ydj30YCWas34PH9jlg",
      logo: "https://logo.clearbit.com/cabelas.ca",
      fallbackLogo: "https://logo.clearbit.com/basspro.ca",
      fallbackText: "C",
      timeAgo: "6 hours ago"
    },
    // Add more news items here as needed
    {
      title: "Walmart FLASH SALE ⚡",
      url: "https://shopstyle.it/l/cugdG",
      logo: "https://logo.clearbit.com/walmart.ca",
      fallbackText: "W",
      timeAgo: "1 hour ago"
    },
    {
      title: "Best Buy Boxing Day Preview Sale 📦",
      url: "https://bestbuy.ca/?tag=promopenguin-20",
      logo: "https://logo.clearbit.com/bestbuy.ca",
      fallbackText: "BB",
      timeAgo: "8 hours ago"
    }
  ];

  return (
    <aside className="w-full lg:w-80">
      <div className="bg-penguin-charcoal rounded-2xl shadow-sm p-4">
        
        {/* Latest News Section - NOW FIRST */}
        <div className="mb-6">
          <div className="flex items-center mb-4">
            <div className="bg-card-arctic-mint px-3 py-1 rounded-lg flex items-center">
              <svg className="w-5 h-5 mr-1 text-penguin-black" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clipRule="evenodd" />
                <path d="M15 7h1a2 2 0 012 2v5.5a1.5 1.5 0 01-3 0V9a1 1 0 00-1-1h-1v-1z" />
              </svg>
              <span className="font-bold text-penguin-black">LATEST NEWS 📰</span>
            </div>
          </div>
          <div className="space-y-3 text-sm">
            {newsItems.map((item, index) => (
              <a 
                key={index}
                href={item.url} 
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-start space-x-3 hover:text-penguin-ice-blue text-penguin-white p-2 rounded-lg hover:bg-penguin-dark-gray transition-colors"
              >
                <img 
                  src={item.logo} 
                  alt={item.title} 
                  className="w-8 h-8 rounded object-contain bg-white p-1"
                  onError={(e) => {
                    const img = e.target as HTMLImageElement;
                    if (item.fallbackLogo && !img.dataset.fallbackAttempted) {
                      img.dataset.fallbackAttempted = '1';
                      img.src = item.fallbackLogo;
                    } else {
                      img.src = `https://via.placeholder.com/32x32/93C4D8/000?text=${item.fallbackText}`;
                    }
                  }}
                />
                <div className="flex-1">
                  <p className="font-medium line-clamp-2">{item.title}</p>
                  <p className="text-xs text-gray-400 mt-1">{item.timeAgo}</p>
                </div>
              </a>
            ))}
          </div>
        </div>

        {/* Top Deals Section - NOW SECOND */}
        <div className="pt-4 border-t border-penguin-dark-gray">
          <div className="flex items-center mb-4">
            <div className="bg-penguin-ice-blue px-3 py-1 rounded-lg flex items-center">
              <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              <span className="font-bold text-penguin-black">TOP DEALS ❄️</span>
            </div>
          </div>
          
          <div className="space-y-4">
            {topDeals.map((deal, index) => (
              <div
                key={deal.id}
                onClick={() => onDealClick(deal)}
                className="cursor-pointer group"
              >
                <div className="flex gap-3 p-3 rounded-lg hover:bg-penguin-dark-gray transition-colors">
                  <div className="w-20 h-20 flex-shrink-0 bg-penguin-white rounded-lg overflow-hidden">
                    <img 
                      src={deal.imageUrl} 
                      alt={deal.title}
                      className="w-full h-full object-contain p-1"
                      onError={(e) => {
                        e.currentTarget.src = '/placeholder-deal.svg';
                      }}
                    />
                  </div>
                  <div className="flex-1 min-w-0 flex flex-col justify-between">
                    <h4 className="font-medium text-sm text-penguin-white line-clamp-2 group-hover:text-penguin-ice-blue">
                      {deal.title}
                    </h4>
                    <button className="mt-2 bg-gradient-to-r from-penguin-ice-blue to-blue-400 text-penguin-black text-xs px-3 py-1 rounded-lg font-bold hover:from-blue-400 hover:to-blue-500 transition-colors">
                      🛒 Shop Deal
                    </button>
                  </div>
                </div>
                {index < topDeals.length - 1 && <hr className="mt-2 border-penguin-dark-gray" />}
              </div>
            ))}
          </div>
        </div>

      </div>
    </aside>
  );
};

export default Sidebar;