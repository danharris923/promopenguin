import React, { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import DealCard from './DealCard';
import DealModal from './DealModal';
import BottomSheet from './BottomSheet';
import Sidebar from './Sidebar';
import { Deal } from '../types/Deal';
import { useIsMobile } from '../utils/useIsMobile';

interface HomePageProps {
  onSearch?: (query: string) => void;
  searchQuery?: string;
}

const HomePage: React.FC<HomePageProps> = ({ searchQuery: propSearchQuery = '' }) => {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [additionalDeals, setAdditionalDeals] = useState<Deal[]>([]);
  const [showingAdditional, setShowingAdditional] = useState(false);
  const [loadingAdditional, setLoadingAdditional] = useState(false);
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(propSearchQuery);
  const isMobile = useIsMobile();

  useEffect(() => {
    setSearchQuery(propSearchQuery);
  }, [propSearchQuery]);

  useEffect(() => {
    fetch('/deals.json')
      .then(res => res.json())
      .then(data => {
        setDeals(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading deals:', err);
        setLoading(false);
      });
  }, []);

  const handleDealClick = (deal: Deal) => {
    setSelectedDeal(deal);
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setTimeout(() => setSelectedDeal(null), 300);
  };

  const loadAdditionalDeals = async () => {
    setLoadingAdditional(true);
    try {
      const response = await fetch('/additional_deals.json');
      const data = await response.json();
      setAdditionalDeals(data);
      setShowingAdditional(true);
    } catch (error) {
      console.error('Error loading additional deals:', error);
    } finally {
      setLoadingAdditional(false);
    }
  };


  const filteredDeals = deals.filter(deal => 
    deal.title.toLowerCase().includes(searchQuery.toLowerCase())
  );
  
  const filteredAdditionalDeals = additionalDeals.filter(deal => 
    deal.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Show main deals first, then additional deals separately
  const displayDeals = showingAdditional 
    ? [...filteredDeals, ...filteredAdditionalDeals]
    : filteredDeals;

  // Top deals should come from main deals only initially
  const topDeals = filteredDeals
    .filter(deal => deal.featured)
    .sort((a, b) => b.discountPercent - a.discountPercent)
    .slice(0, 5);

  const mainDeals = displayDeals.sort((a, b) => 
    new Date(b.dateAdded).getTime() - new Date(a.dateAdded).getTime()
  );

  // Generate structured data for SEO
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "PromoPenguin",
    "description": "Canada's coolest deal site! Find the best Amazon deals, coupons, and flyer specials.",
    "url": "https://promopenguin.vercel.app",
    "publisher": {
      "@type": "Organization",
      "name": "PromoPenguin",
      "logo": {
        "@type": "ImageObject",
        "url": "https://promopenguin.vercel.app/logo192.png"
      }
    },
    "potentialAction": {
      "@type": "SearchAction",
      "target": "https://promopenguin.vercel.app/?search={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  };

  const dealsStructuredData = mainDeals.slice(0, 10).map(deal => ({
    "@type": "Offer",
    "name": deal.title,
    "description": deal.description,
    "url": deal.affiliateUrl,
    "image": deal.imageUrl,
    "category": deal.category,
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "Amazon"
    }
  }));

  // Add structured data to document head
  useEffect(() => {
    const structuredDataScript = document.createElement('script');
    structuredDataScript.type = 'application/ld+json';
    structuredDataScript.innerHTML = JSON.stringify(structuredData);
    document.head.appendChild(structuredDataScript);

    const dealsDataScript = document.createElement('script');
    dealsDataScript.type = 'application/ld+json';
    dealsDataScript.innerHTML = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "ItemList",
      "numberOfItems": mainDeals.length,
      "itemListElement": dealsStructuredData.map((deal, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "item": deal
      }))
    });
    document.head.appendChild(dealsDataScript);

    return () => {
      document.head.removeChild(structuredDataScript);
      document.head.removeChild(dealsDataScript);
    };
  }, [mainDeals]);

  return (
    <>
      <main className="max-w-container mx-auto px-4 py-6">
        <div className="flex flex-col lg:flex-row gap-6">
          <div className="flex-1">

            <div className="mb-6">
              <h1 className="text-2xl font-bold text-penguin-white mb-1">
                {searchQuery ? `Search Results for "${searchQuery}"` : 'Latest Canada Deals & Amazon Savings 🐧'}
              </h1>
              <p className="text-gray-400">
                {searchQuery 
                  ? `Found ${mainDeals.length} Canadian deals matching your search`
                  : 'Discover ice-cold savings on furniture, electronics, home decor & more'
                }
              </p>
            </div>
            
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-80 bg-penguin-dark-gray rounded-2xl animate-pulse" />
                ))}
              </div>
            ) : (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                  {mainDeals.map((deal, index) => (
                    <DealCard
                      key={deal.id}
                      deal={deal}
                      onClick={() => handleDealClick(deal)}
                      colorIndex={index}
                    />
                  ))}
                </div>
                
                {/* Load More Button */}
                {!showingAdditional && !searchQuery && (
                  <div className="mt-8 text-center">
                    <button
                      onClick={loadAdditionalDeals}
                      disabled={loadingAdditional}
                      className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-penguin-ice-blue to-blue-400 text-penguin-black rounded-xl font-bold hover:from-blue-400 hover:to-blue-500 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {loadingAdditional ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Loading More Deals...
                        </>
                      ) : (
                        <>
                          🛒 Load More Deals
                          <svg className="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                          </svg>
                        </>
                      )}
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
          
          <Sidebar 
            topDeals={topDeals}
            onDealClick={handleDealClick}
          />
        </div>
      </main>
      
      {/* Desktop: Modal, Mobile: Bottom Sheet */}
      <AnimatePresence exitBeforeEnter>
        {modalOpen && (
          isMobile ? (
            <BottomSheet
              key="bottom-sheet"
              deal={selectedDeal}
              isOpen={modalOpen}
              onClose={handleCloseModal}
            />
          ) : (
            <DealModal
              key="desktop-modal"
              deal={selectedDeal}
              isOpen={modalOpen}
              onClose={handleCloseModal}
            />
          )
        )}
      </AnimatePresence>
    </>
  );
};

export default HomePage;