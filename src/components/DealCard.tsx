import React, { useState } from 'react';
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
    setIsExpanded(!isExpanded);
  };
  
  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    if (process.env.NODE_ENV === 'development') {
      console.warn('Image failed to load:', deal.imageUrl);
    }
    e.currentTarget.src = '/placeholder-deal.svg';
  };
  
  // Expanded overlay view
  if (isExpanded) {
    return (
      <>
        {/* Background overlay */}
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsExpanded(false)}
        />
        
        {/* Expanded card */}
        <div className="fixed inset-4 md:inset-8 lg:inset-16 z-50 flex items-center justify-center">
          <div className={`${bgColor} rounded-xl overflow-hidden w-full max-w-4xl max-h-full overflow-y-auto shadow-2xl`}>
            <div className="relative">
              {/* Close button */}
              <button
                onClick={() => setIsExpanded(false)}
                className="absolute top-4 right-4 bg-white rounded-full p-2 shadow-lg z-10 hover:bg-gray-100"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
              
              {/* Discount badge */}
              {deal.discountPercent > 0 && (
                <div className="absolute top-4 left-4 bg-red-500 text-white px-4 py-2 rounded-full text-lg font-bold z-10 shadow-lg">
                  {deal.discountPercent}% OFF
                </div>
              )}
              
              {/* Large image */}
              <div className="relative h-96 bg-white">
                <img 
                  src={deal.imageUrl} 
                  alt={deal.title}
                  className="w-full h-full object-contain p-8"
                  onError={handleImageError}
                  loading="lazy"
                  referrerPolicy="no-referrer"
                />
              </div>
              
              {/* Details section */}
              <div className="p-8 bg-white">
                <h2 className="text-3xl font-bold text-text-dark mb-4">{deal.title}</h2>
                
                <p className="text-lg text-gray-700 mb-6">{deal.description}</p>
                
                {/* Price section */}
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-baseline gap-4">
                    <p className="text-4xl font-bold text-primary-green">{priceDisplay.current}</p>
                    {priceDisplay.original && (
                      <p className="text-2xl text-gray-500 line-through">{priceDisplay.original}</p>
                    )}
                  </div>
                  
                  <a
                    href={deal.affiliateUrl}
                    target="__blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="bg-gradient-to-r from-primary-green to-green-600 text-white py-4 px-8 rounded-lg text-xl font-bold hover:from-green-600 hover:to-green-700 transition-colors shadow-lg"
                  >
                    Shop Now
                  </a>
                </div>
                
                {/* Additional details */}
                <div className="border-t pt-4">
                  <div className="flex flex-wrap gap-2">
                    {deal.category && (
                      <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">
                        {deal.category}
                      </span>
                    )}
                    {deal.featured && (
                      <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
                        Featured Deal
                      </span>
                    )}
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                      Added {new Date(deal.dateAdded).toLocaleDateString()}
                    </span>
                  </div>
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