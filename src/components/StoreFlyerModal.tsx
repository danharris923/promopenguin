import React from 'react';
import { Store } from '../types/Store';

interface StoreFlyerModalProps {
  store: Store | null;
  isOpen: boolean;
  onClose: () => void;
}

const StoreFlyerModal: React.FC<StoreFlyerModalProps> = ({ store, isOpen, onClose }) => {
  if (!isOpen || !store) return null;

  // const formatDate = (dateStr: string) => {
  //   return new Date(dateStr).toLocaleDateString('en-CA', { 
  //     month: 'short', 
  //     day: 'numeric',
  //     year: 'numeric'
  //   });
  // };

  return (
    <div 
      className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div 
        className="bg-penguin-charcoal rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-penguin-gray"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="relative">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full bg-penguin-dark-gray hover:bg-penguin-gray text-penguin-white z-10"
            aria-label="Close modal"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          
          <div className="p-6">
            {/* Store Header */}
            <div className="flex flex-col md:flex-row gap-6 mb-8">
              <div className="md:w-1/3">
                <div className="bg-penguin-dark-gray rounded-xl p-4">
                  <img 
                    src={store.previewImage} 
                    alt={`${store.name} flyer`}
                    className="w-full h-64 object-contain rounded-lg"
                    onError={(e) => {
                      const img = e.currentTarget;
                      img.src = `data:image/svg+xml,%3Csvg width='400' height='400' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%23EAB2AB'/%3E%3Cstop offset='100%25' stop-color='%23ffffff'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='400' fill='url(%23grad)'/%3E%3Ctext x='50%25' y='45%25' text-anchor='middle' fill='%23333' font-family='sans-serif' font-size='18' font-weight='bold'%3E🏪%3C/text%3E%3Ctext x='50%25' y='60%25' text-anchor='middle' fill='%23333' font-family='sans-serif' font-size='14'%3E${encodeURIComponent(store.name)}%3C/text%3E%3C/svg%3E`;
                    }}
                    loading="lazy"
                    referrerPolicy="no-referrer"
                  />
                </div>
              </div>
              
              <div className="md:w-2/3">
                <h2 className="text-3xl font-bold text-penguin-white mb-4">
                  {store.name} Weekly Flyer
                </h2>
                
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
                  <div className="bg-penguin-dark-gray rounded-xl p-4 text-center">
                    <div className="text-2xl font-bold text-penguin-ice-blue">{store.totalDeals}</div>
                    <div className="text-sm text-gray-400">Total Deals</div>
                  </div>
                  <div className="bg-penguin-dark-gray rounded-xl p-4 text-center">
                    <div className="text-2xl font-bold text-green-400">{store.averageDiscount}%</div>
                    <div className="text-sm text-gray-400">Avg Discount</div>
                  </div>
                  <div className="bg-penguin-dark-gray rounded-xl p-4 text-center">
                    <div className="text-2xl font-bold text-red-400">{store.maxDiscount}%</div>
                    <div className="text-sm text-gray-400">Max Savings</div>
                  </div>
                </div>

                <p className="text-lg text-penguin-white leading-relaxed mb-4">
                  Browse all {store.totalDeals} deals from {store.name}'s weekly flyer. 
                  Find great savings with discounts up to {store.maxDiscount}% off regular prices.
                </p>
              </div>
            </div>

            {/* All Deals Grid */}
            <div className="mb-8">
              <h3 className="text-xl font-semibold text-penguin-white mb-6 flex items-center">
                🛍️ All {store.name} Deals ({store.totalDeals})
              </h3>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {store.deals.map(deal => (
                  <div key={deal.id} className="bg-penguin-dark-gray rounded-xl p-4 hover:bg-penguin-gray transition-colors group">
                    <div className="aspect-square mb-3 overflow-hidden rounded-lg bg-white">
                      <img
                        src={deal.imageUrl}
                        alt={deal.title}
                        className="w-full h-full object-contain p-2 group-hover:scale-105 transition-transform"
                        onError={(e) => {
                          const img = e.currentTarget;
                          const colors = ['#93C4D8', '#A8E6CF', '#C8B6F6', '#81D4E3', '#FFB3D9'];
                          const colorIndex = deal.id.charCodeAt(0) % colors.length;
                          const bgColor = colors[colorIndex];
                          img.src = `data:image/svg+xml,%3Csvg width='200' height='200' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='${bgColor}'/%3E%3Cstop offset='100%25' stop-color='%23ffffff'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='200' height='200' fill='url(%23grad)'/%3E%3Ctext x='50%25' y='45%25' text-anchor='middle' fill='%23333' font-family='sans-serif' font-size='16' font-weight='bold'%3E🛒%3C/text%3E%3Ctext x='50%25' y='60%25' text-anchor='middle' fill='%23333' font-family='sans-serif' font-size='12'%3E${encodeURIComponent(deal.title.substring(0, 10))}%3C/text%3E%3C/svg%3E`;
                        }}
                        loading="lazy"
                      />
                    </div>
                    
                    <h4 className="font-semibold text-sm text-penguin-white mb-2 line-clamp-2 leading-tight">
                      {deal.title}
                    </h4>
                    
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-2">
                        <span className="text-lg font-bold text-green-400">
                          ${deal.price.toFixed(2)}
                        </span>
                        {deal.originalPrice > deal.price && (
                          <span className="text-sm text-gray-400 line-through">
                            ${deal.originalPrice.toFixed(2)}
                          </span>
                        )}
                      </div>
                      {deal.discountPercent > 0 && (
                        <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full font-medium">
                          {deal.discountPercent}% OFF
                        </span>
                      )}
                    </div>

                    <div className="flex items-center justify-between text-xs">
                      <span className="bg-penguin-charcoal text-gray-300 px-2 py-1 rounded">
                        {deal.category}
                      </span>
                      {deal.featured && (
                        <span className="bg-penguin-ice-blue text-penguin-black px-2 py-1 rounded font-medium">
                          Featured
                        </span>
                      )}
                    </div>

                    {deal.description && (
                      <p className="text-xs text-gray-400 mt-2 line-clamp-2">
                        {deal.description.replace(/🔥|⚡|💫|🏆|⭐|🎯/g, '').trim()}
                      </p>
                    )}

                    <a
                      href={deal.affiliateUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="block w-full mt-3 bg-gradient-to-r from-penguin-ice-blue to-blue-400 text-penguin-black text-center py-2 px-3 rounded-lg text-sm font-bold hover:from-blue-400 hover:to-blue-500 transition-colors"
                    >
                      🛒 Get Deal
                    </a>
                  </div>
                ))}
              </div>
            </div>

            {/* Footer */}
            <div className="text-center pt-6 border-t border-penguin-dark-gray">
              <p className="text-sm text-gray-400 mb-2">
                All deals shown are from {store.name}'s current weekly flyer
              </p>
              <p className="text-xs text-gray-500">
                Prices and availability may vary by location • Valid until end of week
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StoreFlyerModal;