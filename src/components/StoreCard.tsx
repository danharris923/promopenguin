import React, { useState, useEffect } from 'react';
import { Deal } from '../types/Deal';

interface StoreCardProps {
  storeName: string;
  storeDeals: Deal[];
  onClick: () => void;
  colorIndex?: number;
}

const StoreCard: React.FC<StoreCardProps> = ({ storeName, storeDeals, onClick, colorIndex = 0 }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const bgColors = ['bg-card-ice-blue', 'bg-card-arctic-mint', 'bg-card-snow-purple', 'bg-card-glacier-teal', 'bg-card-frost-pink'];
  const bgColor = bgColors[colorIndex % bgColors.length];
  
  const handleCardClick = () => {
    if (window.innerWidth < 768) { // Mobile - center modal
      setIsExpanded(!isExpanded);
    } else { // Desktop - original modal
      onClick();
    }
  };

  // Prevent body scroll when modal is open on mobile
  useEffect(() => {
    if (isExpanded && window.innerWidth < 768) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isExpanded]);

  // Get best deal image as store preview
  const previewDeal = storeDeals[0];
  const dealCount = storeDeals.length;
  const averageDiscount = Math.round(storeDeals.reduce((acc, deal) => acc + deal.discountPercent, 0) / dealCount);

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    const img = e.currentTarget;
    
    // Try different fallback strategies for mobile compatibility
    if (!img.dataset.fallbackAttempt) {
      img.dataset.fallbackAttempt = '1';
      
      // First: Try removing query parameters that might cause mobile issues
      const cleanUrl = previewDeal.imageUrl.split('?')[0];
      if (cleanUrl !== previewDeal.imageUrl) {
        img.src = cleanUrl;
        return;
      }
      
      // Second: Try HTTPS if it was HTTP
      if (previewDeal.imageUrl.startsWith('http://')) {
        img.src = previewDeal.imageUrl.replace('http://', 'https://');
        return;
      }
    }
    
    // Final fallback: Use a colorful SVG placeholder
    const colors = ['#93C4D8', '#A8E6CF', '#C8B6F6', '#81D4E3', '#FFB3D9'];
    const colorIndex = storeName.charCodeAt(0) % colors.length;
    const bgColor = colors[colorIndex];
    img.src = `data:image/svg+xml,%3Csvg width='400' height='400' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='${bgColor}'/%3E%3Cstop offset='100%25' stop-color='%23ffffff'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='400' fill='url(%23grad)'/%3E%3Ctext x='50%25' y='45%25' text-anchor='middle' fill='%23333' font-family='sans-serif' font-size='18' font-weight='bold'%3E🏪%3C/text%3E%3Ctext x='50%25' y='60%25' text-anchor='middle' fill='%23333' font-family='sans-serif' font-size='14'%3E${encodeURIComponent(storeName)}%3C/text%3E%3C/svg%3E`;
  };

  // Mobile center-sliding modal
  if (isExpanded && window.innerWidth < 768) {
    return (
      <>
        {/* Backdrop */}
        <div 
          className="fixed inset-0 bg-black/30 backdrop-blur-[2px] z-50 animate-in fade-in duration-300"
          onClick={() => setIsExpanded(false)}
        />
        
        {/* Center Modal */}
        <div className="fixed inset-0 z-50 flex items-center justify-center p-8 animate-in slide-in-from-bottom-6 duration-300">
          <div className={`${bgColor} w-full max-w-xs max-h-[75vh] rounded-3xl shadow-2xl overflow-hidden`}>
            {/* Header */}
            <div className="relative bg-penguin-charcoal/95 backdrop-blur-sm px-4 py-3 border-b border-penguin-dark-gray">
              <button
                onClick={() => setIsExpanded(false)}
                className="absolute right-3 top-3 w-8 h-8 flex items-center justify-center rounded-full bg-penguin-dark-gray hover:bg-penguin-ice-blue hover:text-penguin-black text-penguin-white transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
              <h3 className="font-semibold text-penguin-white pr-10">{storeName} Flyer</h3>
            </div>
            
            {/* Scrollable Content */}
            <div className="overflow-y-auto max-h-full">
              {/* Store Preview */}
              <div className="relative bg-penguin-white">
                <div className="aspect-square">
                  <img 
                    src={previewDeal.imageUrl} 
                    alt={`${storeName} flyer preview`}
                    className="w-full h-full object-cover p-2"
                    onError={handleImageError}
                    loading="lazy"
                  />
                </div>
                
                {/* Store info overlay */}
                <div className="absolute bottom-2 left-2 right-2 bg-black/70 text-white rounded-lg p-2">
                  <div className="text-sm font-bold">{storeName}</div>
                  <div className="text-xs">{dealCount} deals • Avg {averageDiscount}% off</div>
                </div>
              </div>
              
              {/* Store Details */}
              <div className="bg-penguin-white p-4">
                <h2 className="text-lg font-bold text-penguin-black mb-2">{storeName} Weekly Flyer</h2>
                
                <p className="text-sm text-gray-700 mb-4 leading-relaxed">
                  Browse {dealCount} hot deals with an average discount of {averageDiscount}%. 
                  Tap below to view the complete flyer with all products and prices.
                </p>
                
                {/* Action Button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setIsExpanded(false);
                    setTimeout(() => onClick(), 100);
                  }}
                  className="block w-full bg-gradient-to-r from-penguin-ice-blue to-blue-400 text-penguin-black py-3 rounded-xl text-center font-bold hover:from-blue-400 hover:to-blue-500 transition-colors shadow-lg"
                >
                  🏪 View Full Flyer
                </button>
              
                {/* Tags */}
                <div className="flex flex-wrap gap-2 pt-3 border-t border-gray-200 mt-4">
                  <span className="bg-penguin-charcoal text-penguin-white px-2 py-1 rounded-full text-xs">
                    {dealCount} Deals
                  </span>
                  <span className="bg-card-arctic-mint text-penguin-black px-2 py-1 rounded-full text-xs">
                    Avg {averageDiscount}% Off
                  </span>
                  <span className="bg-card-ice-blue text-penguin-black px-2 py-1 rounded-full text-xs">
                    Weekly Flyer
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </>
    );
  }
  
  // Regular card view
  return (
    <div 
      className={`${bgColor} rounded-2xl overflow-hidden cursor-pointer transition-all duration-200 hover:scale-[1.02] hover:shadow-xl h-80`}
      onClick={handleCardClick}
    >
      <div className="relative h-full flex flex-col">
        <div className="relative h-48 overflow-hidden">
          <img 
            src={previewDeal.imageUrl} 
            alt={`${storeName} flyer preview`}
            className="w-full h-full object-cover p-2"
            onError={handleImageError}
            loading="lazy"
          />
          
          {/* Store info overlay */}
          <div className="absolute bottom-2 left-2 right-2 bg-black/70 text-white rounded-lg p-2">
            <div className="text-sm font-bold">{storeName}</div>
            <div className="text-xs">{dealCount} deals • Avg {averageDiscount}% off</div>
          </div>
        </div>
        
        <div className="flex-1 p-4 bg-penguin-white/95 backdrop-blur-sm flex flex-col justify-between rounded-t-2xl">
          <h3 className="font-semibold text-penguin-black text-base line-clamp-2 mb-2">
            {storeName} Weekly Flyer
          </h3>
          
          <div className="w-full">
            <div className="text-center mb-3">
              <p className="text-sm text-penguin-black leading-tight">
                Browse {dealCount} hot deals with savings up to {Math.max(...storeDeals.map(d => d.discountPercent))}% off
              </p>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onClick();
              }}
              className="block w-full bg-gradient-to-r from-penguin-ice-blue to-blue-400 text-penguin-black py-3 px-4 rounded-xl text-center font-bold hover:from-blue-400 hover:to-blue-500 transition-colors shadow-lg"
            >
              🏪 View Full Flyer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StoreCard;