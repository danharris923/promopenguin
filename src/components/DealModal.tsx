import React from 'react';
import { Deal } from '../types/Deal';

interface DealModalProps {
  deal: Deal | null;
  isOpen: boolean;
  onClose: () => void;
}

const DealModal: React.FC<DealModalProps> = ({ deal, isOpen, onClose }) => {
  if (!isOpen || !deal) return null;

  return (
    <div 
      className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div 
        className="bg-penguin-charcoal rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-penguin-gray"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="relative">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full bg-penguin-dark-gray hover:bg-penguin-gray text-penguin-white"
            aria-label="Close modal"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          
          <div className="p-6">
            <div className="flex flex-col md:flex-row gap-6">
              <div className="md:w-1/2">
                <div className="bg-penguin-dark-gray rounded-xl p-4">
                  <img 
                    src={deal.imageUrl} 
                    alt={deal.title}
                    className="w-full h-64 object-contain"
                    onError={(e) => {
                      if (process.env.NODE_ENV === 'development') {
                        console.warn('Modal image failed to load:', deal.imageUrl);
                      }
                      e.currentTarget.src = '/placeholder-deal.svg';
                    }}
                    loading="lazy"
                    referrerPolicy="no-referrer"
                  />
                </div>
              </div>
              
              <div className="md:w-1/2">
                <div className="mb-2 text-sm text-gray-400">{deal.category}</div>
                <h2 className="text-2xl font-bold text-penguin-white mb-4">{deal.title}</h2>
                
                <div className="mb-6 text-center">
                  <p className="text-lg text-penguin-white leading-relaxed">{deal.description}</p>
                </div>
                
                
                <a
                  href={deal.affiliateUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full text-penguin-black text-center py-4 px-6 rounded-xl font-bold transition-all transform hover:scale-105 shadow-lg bg-gradient-to-r from-penguin-ice-blue to-blue-400 hover:from-blue-400 hover:to-blue-500"
                >
                  🛒 Shop This Deal
                </a>
                
                <p className="text-xs text-gray-400 mt-4 text-center">
                  Deal added on {new Date(deal.dateAdded).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DealModal;