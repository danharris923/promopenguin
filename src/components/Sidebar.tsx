import React from 'react';
import { Deal } from '../types/Deal';

interface SidebarProps {
  topDeals: Deal[];
  onDealClick: (deal: Deal) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ topDeals, onDealClick }) => {
  return (
    <aside className="w-full lg:w-80">
      <div className="bg-penguin-charcoal rounded-2xl shadow-sm p-4">
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
        
        <div className="mt-6 pt-4 border-t border-penguin-dark-gray">
          <h2 className="font-semibold text-penguin-white mb-3">Latest News 📰</h2>
          <div className="space-y-3 text-sm">
            <a href="https://shopstyle.it/l/cj22Z" className="flex items-start space-x-3 hover:text-penguin-ice-blue text-penguin-white p-2 rounded-lg hover:bg-penguin-dark-gray transition-colors">
              <img 
                src="https://logo.clearbit.com/lululemon.com" 
                alt="Lululemon" 
                className="w-8 h-8 rounded object-contain bg-white p-1"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = 'https://via.placeholder.com/32x32/000/fff?text=L';
                }}
              />
              <div className="flex-1">
                <p className="font-medium line-clamp-2">Lululemon We Made Too Much SALE 🔥</p>
                <p className="text-xs text-gray-400 mt-1">2 hours ago</p>
              </div>
            </a>
            <a href="https://shopstyle.it/l/cj24C" className="flex items-start space-x-3 hover:text-penguin-ice-blue text-penguin-white p-2 rounded-lg hover:bg-penguin-dark-gray transition-colors">
              <img 
                src="https://logo.clearbit.com/gap.com" 
                alt="Gap" 
                className="w-8 h-8 rounded object-contain bg-white p-1"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = 'https://via.placeholder.com/32x32/000/fff?text=G';
                }}
              />
              <div className="flex-1">
                <p className="font-medium line-clamp-2">Gap SALE - Up to 70% Off Everything 💥</p>
                <p className="text-xs text-gray-400 mt-1">4 hours ago</p>
              </div>
            </a>
            <a href="https://www.basspro.ca/home?utm_source=RAN&utm_medium=affiliate&utm_content=Living+off+the+GRID+in+Canada&ranMID=50435&ranEAID=sUVpAjRtGL4&ranSiteID=sUVpAjRtGL4-Ycc1ydj30YCWas34PH9jlg" className="flex items-start space-x-3 hover:text-penguin-ice-blue text-penguin-white p-2 rounded-lg hover:bg-penguin-dark-gray transition-colors">
              <img 
                src="https://logo.clearbit.com/cabelas.ca" 
                alt="Cabela's" 
                className="w-8 h-8 rounded object-contain bg-white p-1"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = 'https://logo.clearbit.com/basspro.ca';
                  (e.target as HTMLImageElement).onerror = () => {
                    (e.target as HTMLImageElement).src = 'https://via.placeholder.com/32x32/2d5a27/fff?text=C';
                  };
                }}
              />
              <div className="flex-1">
                <p className="font-medium line-clamp-2">Cabela's Fall Classic SALE 🍂</p>
                <p className="text-xs text-gray-400 mt-1">6 hours ago</p>
              </div>
            </a>
          </div>
        </div>

      </div>
    </aside>
  );
};

export default Sidebar;