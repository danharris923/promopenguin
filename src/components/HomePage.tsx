import React, { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import StoreCard from './StoreCard';
import StoreFlyerModal from './StoreFlyerModal';
import Sidebar from './Sidebar';
import { Deal } from '../types/Deal';
import { Store } from '../types/Store';
// import { useIsMobile } from '../utils/useIsMobile';

interface HomePageProps {
  onSearch?: (query: string) => void;
  searchQuery?: string;
}

const HomePage: React.FC<HomePageProps> = ({ searchQuery: propSearchQuery = '' }) => {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [stores, setStores] = useState<Store[]>([]);
  // const [additionalDeals, setAdditionalDeals] = useState<Deal[]>([]);
  const [showingAdditional, setShowingAdditional] = useState(false);
  const [loadingAdditional, setLoadingAdditional] = useState(false);
  const [selectedStore, setSelectedStore] = useState<Store | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(propSearchQuery);
  // const isMobile = useIsMobile(); // Not needed for store flyer modal

  useEffect(() => {
    setSearchQuery(propSearchQuery);
  }, [propSearchQuery]);

  // Function to extract store name from deal title
  const extractStoreName = (title: string): string => {
    // Remove common prefixes and extract store name
    const cleaned = title.replace(/^(Canada:|Canadian )/, '');
    const words = cleaned.split(/[:/-]/)[0].trim();
    
    // Handle special cases for store name extraction
    if (words.toLowerCase().includes('walmart')) return 'Walmart';
    if (words.toLowerCase().includes('costco')) return 'Costco';
    if (words.toLowerCase().includes('giant tiger')) return 'Giant Tiger';
    if (words.toLowerCase().includes('no frills')) return 'No Frills';
    if (words.toLowerCase().includes('sobeys')) return 'Sobeys';
    if (words.toLowerCase().includes('shoppers drug mart')) return 'Shoppers Drug Mart';
    if (words.toLowerCase().includes('canadian tire')) return 'Canadian Tire';
    if (words.toLowerCase().includes('loblaws')) return 'Loblaws';
    if (words.toLowerCase().includes('metro')) return 'Metro';
    if (words.toLowerCase().includes('best buy')) return 'Best Buy';
    if (words.toLowerCase().includes('abercrombie')) return 'Abercrombie & Fitch';
    if (words.toLowerCase().includes('suzy shier')) return 'Suzy Shier';
    if (words.toLowerCase().includes('steve madden')) return 'Steve Madden';
    if (words.toLowerCase().includes('herschel')) return 'Herschel';
    if (words.toLowerCase().includes('hatley')) return 'Hatley';
    if (words.toLowerCase().includes('lacoste')) return 'Lacoste';
    if (words.toLowerCase().includes('coach')) return 'Coach';
    if (words.toLowerCase().includes('gap')) return 'Gap';
    if (words.toLowerCase().includes('bouclair')) return 'Bouclair';
    
    // For generic deals, try to extract the first meaningful word(s)
    const firstWords = words.split(' ').slice(0, 2).join(' ');
    return firstWords || 'General Store';
  };

  // Function to group deals by store
  const groupDealsByStore = React.useCallback((deals: Deal[]): Store[] => {
    const storeGroups: { [key: string]: Deal[] } = {};
    
    deals.forEach(deal => {
      const storeName = extractStoreName(deal.title);
      if (!storeGroups[storeName]) {
        storeGroups[storeName] = [];
      }
      storeGroups[storeName].push(deal);
    });

    return Object.entries(storeGroups).map(([storeName, storeDeals]) => {
      const totalDeals = storeDeals.length;
      const averageDiscount = Math.round(
        storeDeals.reduce((sum, deal) => sum + deal.discountPercent, 0) / totalDeals
      );
      const maxDiscount = Math.max(...storeDeals.map(deal => deal.discountPercent));
      
      return {
        id: storeName.toLowerCase().replace(/[^a-z0-9]/g, ''),
        name: storeName,
        deals: storeDeals.sort((a, b) => b.discountPercent - a.discountPercent), // Sort by highest discount
        totalDeals,
        averageDiscount,
        maxDiscount,
        previewImage: storeDeals[0]?.imageUrl || '',
        category: storeDeals[0]?.category || 'General'
      };
    }).sort((a, b) => b.totalDeals - a.totalDeals); // Sort stores by deal count
  }, []);

  useEffect(() => {
    fetch('/deals.json')
      .then(res => res.json())
      .then(data => {
        setDeals(data);
        const groupedStores = groupDealsByStore(data);
        setStores(groupedStores);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading deals:', err);
        setLoading(false);
      });
  }, [groupDealsByStore]);

  const handleStoreClick = (store: Store) => {
    setSelectedStore(store);
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setTimeout(() => setSelectedStore(null), 300);
  };

  const loadAdditionalDeals = async () => {
    setLoadingAdditional(true);
    try {
      // Additional deals functionality removed - stores now show all deals
      setShowingAdditional(true);
    } catch (error) {
      console.error('Error loading additional deals:', error);
    } finally {
      setLoadingAdditional(false);
    }
  };


  const filteredStores = stores.filter(store => 
    store.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    store.deals.some(deal => deal.title.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const filteredDeals = deals.filter(deal => 
    deal.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Top deals for sidebar (still individual deals)
  const topDeals = filteredDeals
    .filter(deal => deal.featured)
    .sort((a, b) => b.discountPercent - a.discountPercent)
    .slice(0, 5);

  const displayStores = searchQuery 
    ? filteredStores
    : stores;

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

  const storesStructuredData = displayStores.slice(0, 10).map(store => ({
    "@type": "Store",
    "name": store.name,
    "description": `Browse ${store.totalDeals} deals with average savings of ${store.averageDiscount}%`,
    "image": store.previewImage,
    "category": store.category,
    "hasOfferCatalog": {
      "@type": "OfferCatalog",
      "numberOfItems": store.totalDeals,
      "itemListElement": store.deals.slice(0, 5).map(deal => ({
        "@type": "Offer",
        "name": deal.title,
        "price": deal.price,
        "priceCurrency": "CAD",
        "availability": "https://schema.org/InStock"
      }))
    }
  }));

  // Add structured data to document head
  useEffect(() => {
    const structuredDataScript = document.createElement('script');
    structuredDataScript.type = 'application/ld+json';
    structuredDataScript.innerHTML = JSON.stringify(structuredData);
    document.head.appendChild(structuredDataScript);

    const storesDataScript = document.createElement('script');
    storesDataScript.type = 'application/ld+json';
    storesDataScript.innerHTML = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "ItemList",
      "numberOfItems": displayStores.length,
      "itemListElement": storesStructuredData.map((store, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "item": store
      }))
    });
    document.head.appendChild(storesDataScript);

    return () => {
      document.head.removeChild(structuredDataScript);
      document.head.removeChild(storesDataScript);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [displayStores.length]);

  return (
    <>
      <main className="max-w-container mx-auto px-4 py-6">
        <div className="flex flex-col lg:flex-row gap-6">
          <div className="flex-1">

            <div className="mb-6">
              <h1 className="text-2xl font-bold text-penguin-white mb-1">
                {searchQuery ? `Search Results for "${searchQuery}"` : 'Browse Store Flyers & Weekly Deals 🐧'}
              </h1>
              <p className="text-gray-400">
                {searchQuery 
                  ? `Found ${displayStores.length} stores with deals matching your search`
                  : 'Discover store flyers and weekly specials from Canada\'s top retailers'
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
                  {displayStores.map((store, index) => (
                    <StoreCard
                      key={store.id}
                      storeName={store.name}
                      storeDeals={store.deals}
                      onClick={() => handleStoreClick(store)}
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
            onDealClick={(deal) => {
              // Find the store that contains this deal and open its flyer
              const store = stores.find(s => s.deals.some(d => d.id === deal.id));
              if (store) {
                handleStoreClick(store);
              }
            }}
          />
        </div>
      </main>
      
      {/* Store Flyer Modal */}
      <AnimatePresence exitBeforeEnter>
        {modalOpen && (
          <StoreFlyerModal
            key="store-flyer-modal"
            store={selectedStore}
            isOpen={modalOpen}
            onClose={handleCloseModal}
          />
        )}
      </AnimatePresence>
    </>
  );
};

export default HomePage;