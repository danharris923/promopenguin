import React, { useState, useEffect } from 'react';
import { Deal } from '../types/Deal';
import { getPriceDisplay } from '../utils/dealUtils';
import { getPriceVisibility } from '../utils/priceVisibility';

interface DealCardProps {
  deal: Deal;
  onClick: () => void;
  variant?: 'default' | 'featured';
  colorIndex?: number;
}

const DealCard: React.FC<DealCardProps> = ({ deal, onClick, variant = 'default', colorIndex = 0 }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const bgColors = ['bg-card-pink', 'bg-card-blue', 'bg-card-yellow'];
  const bgColor = bgColors[colorIndex % bgColors.length];
  
  const isLarge = variant === 'featured';
  const priceDisplay = getPriceDisplay(deal.originalPrice, deal.price, deal.discountPercent);
  const priceVisibility = getPriceVisibility(deal.id);
  
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
  
  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    if (process.env.NODE_ENV === 'development') {
      console.warn('Image failed to load:', deal.imageUrl);
    }
    e.currentTarget.src = '/placeholder-deal.svg';
  };
  
  // Mobile center-sliding modal
  if (isExpanded && window.innerWidth < 768) {
    return (
      <>
        {/* Backdrop - More transparent to show background */}
        <div 
          className="fixed inset-0 bg-black/30 backdrop-blur-[2px] z-50 animate-in fade-in duration-300"
          onClick={() => setIsExpanded(false)}
        />
        
        {/* Center Modal - More padding to show background */}
        <div className="fixed inset-0 z-50 flex items-center justify-center p-8 animate-in slide-in-from-bottom-6 duration-300">
          <div className={`${bgColor} w-full max-w-xs max-h-[75vh] rounded-2xl shadow-2xl overflow-hidden`}>
            {/* Header */}
            <div className="relative bg-white/95 backdrop-blur-sm px-4 py-3 border-b border-gray-100">
              <button
                onClick={() => setIsExpanded(false)}
                className="absolute right-3 top-3 w-8 h-8 flex items-center justify-center rounded-full bg-gray-100 hover:bg-gray-200 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
              <h3 className="font-semibold text-gray-900 pr-10">Deal Details</h3>
            </div>
            
            {/* Scrollable Content */}
            <div className="overflow-y-auto max-h-full">
              {/* Image Section */}
              <div className="relative bg-white">
                {/* Discount badge */}
                {deal.discountPercent > 0 && (
                  <div className="absolute top-3 left-3 bg-red-500 text-white px-2 py-1 rounded-full text-xs font-bold z-10 shadow-lg">
                    {deal.discountPercent}% OFF
                  </div>
                )}
                
                <div className="aspect-square">
                  <img 
                    src={deal.imageUrl} 
                    alt={deal.title}
                    className="w-full h-full object-contain p-4"
                    onError={handleImageError}
                    loading="lazy"
                    referrerPolicy="no-referrer"
                  />
                </div>
              </div>
              
              {/* Details Section */}
              <div className="bg-white p-4">
                <h2 className="text-lg font-bold text-text-dark mb-2">{deal.title}</h2>
                
                <p className="text-sm text-gray-600 mb-4 leading-relaxed">{deal.description}</p>
                
                {/* Price Section */}
                <div className="mb-4">
                  <div className="flex items-baseline gap-2 mb-3">
                    <p className="text-2xl font-bold text-primary-green">{priceDisplay.current}</p>
                    {priceDisplay.original && (
                      <p className="text-lg text-gray-500 line-through">{priceDisplay.original}</p>
                    )}
                  </div>
                  
                  {/* Action Button */}
                  <a
                    href={deal.affiliateUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="block w-full bg-blue-500 text-white py-3 rounded-xl text-center font-semibold hover:bg-blue-600 transition-colors shadow-sm"
                  >
                    Shop Now
                  </a>
                </div>
              
                {/* Tags */}
                <div className="flex flex-wrap gap-2 pt-3 border-t border-gray-100">
                  {deal.category && (
                    <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full text-xs">
                      {deal.category}
                    </span>
                  )}
                  {deal.featured && (
                    <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs">
                      Featured
                    </span>
                  )}
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                    {new Date(deal.dateAdded).toLocaleDateString()}
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
      className={`${bgColor} rounded-lg overflow-hidden cursor-pointer ${
        isLarge ? 'h-96' : 'h-80'
      }`}
      onClick={handleCardClick}
    >
      <div className="relative h-full flex flex-col">
        {/* Discount percentage badge */}
        {deal.discountPercent > 0 && (
          <div className="absolute top-2 left-2 bg-red-500 text-white px-3 py-1 rounded-full text-sm font-bold z-10 shadow-md">
            {deal.discountPercent}% OFF
          </div>
        )}
        
        
        <div className={`relative ${isLarge ? 'h-64' : 'h-48'} overflow-hidden`}>
          <img 
            src={deal.imageUrl} 
            alt={deal.title}
            className="w-full h-full object-contain p-4"
            onError={handleImageError}
            loading="lazy"
            referrerPolicy="no-referrer"
          />
        </div>
        
        <div className="flex-1 p-4 bg-white/90 flex flex-col justify-between">
          <h3 className={`font-semibold text-text-dark ${isLarge ? 'text-lg' : 'text-base'} line-clamp-2 mb-2`}>
            {deal.title}
          </h3>
          
          <div className="flex items-end justify-between">
            {priceVisibility.showPrice ? (
              // Show price for ~10% of deals
              <>
                <div>
                  <div className="flex items-baseline gap-2">
                    <p className="text-2xl font-bold text-primary-green">{priceDisplay.current}</p>
                    {priceDisplay.original && (
                      <p className="text-base text-gray-500 line-through">{priceDisplay.original}</p>
                    )}
                  </div>
                </div>
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    window.open(deal.affiliateUrl, '_blank');
                  }}
                  className="bg-primary-green text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors shadow-sm"
                >
                  Shop Now
                </button>
              </>
            ) : (
              // Show "Check Price" button for ~80% of deals (badge already shown at top)
              <div className="w-full">
                <div className="text-center mb-3">
                  <p className="text-sm text-text-dark leading-tight">{deal.description}</p>
                </div>
                <a
                  href={deal.affiliateUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={(e) => e.stopPropagation()}
                  className="block w-full bg-gradient-to-r from-primary-green to-green-600 text-white py-3 px-4 rounded-lg text-center font-bold hover:from-green-600 hover:to-green-700 transition-colors shadow-lg"
                >
                  {priceVisibility.checkPriceMessage}
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DealCard;