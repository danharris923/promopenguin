import React, { useState, useEffect } from 'react';

interface FlyerItem {
  id: string;
  store: string;
  storeLogo: string;
  title: string;
  price: number;
  originalPrice?: number;
  discountPercent?: number;
  imageUrl: string;
  validUntil: string;
  category: string;
  description?: string;
}

interface Flyer {
  id: string;
  storeName: string;
  storeId: string;
  storeLogo: string;
  validFrom: string;
  validUntil: string;
  pageCount: number;
  previewImage: string;
  items: FlyerItem[];
}

const Flyers: React.FC = () => {
  const [flyers, setFlyers] = useState<Flyer[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedStore, setSelectedStore] = useState<string>('all');
  const [selectedFlyer, setSelectedFlyer] = useState<Flyer | null>(null);

  // Enhanced Flipp API integration with detailed product information
  const fetchFlippData = async (postalCode: string = 'M5V3A8', query: string = 'groceries', limit: number = 100) => {
    try {
      // Enhanced URL with more detailed parameters for better product data
      const url = `https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code=${postalCode}&q=${query}&limit=${limit}&include_images=true&include_descriptions=true&sort=sale_price&order=asc`;
      console.log('Fetching enhanced data from URL:', url);
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        },
        mode: 'cors'
      });
      
      console.log('Enhanced response status:', response.status);
      console.log('Enhanced response headers:', response.headers);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Enhanced raw API data:', data);
      
      // Extract items from various possible response structures
      let items = [];
      if (data.items) {
        items = data.items;
      } else if (data.data && data.data.items) {
        items = data.data.items;
      } else if (Array.isArray(data)) {
        items = data;
      } else if (data.results) {
        items = data.results;
      }
      
      console.log(`Extracted ${items.length} items from enhanced API response`);
      return items;
    } catch (error) {
      console.error('Enhanced Flipp API error details:', error);
      return [];
    }
  };

  // Fetch detailed store information
  const fetchStoreDetails = async (storeId: string) => {
    try {
      const url = `https://backflipp.wishabi.com/flipp/merchants/${storeId}?locale=en-ca`;
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        mode: 'cors'
      });
      
      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Store details fetch error:', error);
    }
    return null;
  };

  // Enhanced conversion with detailed product information extraction - ONE FLYER PER STORE
  const convertFlippDataToFlyers = async (flippItems: any[]): Promise<Flyer[]> => {
    const storeGroups: { [key: string]: any[] } = {};
    
    console.log(`Converting ${flippItems.length} items to flyers with enhanced data`);
    
    // Group items by store with better merchant identification
    flippItems.forEach(item => {
      let storeName = item.merchant?.name || 
                       item.store_name || 
                       item.retailer?.name || 
                       'Unknown Store';
      
      // Normalize store names to prevent duplicates
      storeName = storeName.trim().replace(/\s+/g, ' ');
      
      // Group common store variations together
      if (storeName.toLowerCase().includes('walmart')) storeName = 'Walmart';
      else if (storeName.toLowerCase().includes('loblaws')) storeName = 'Loblaws';
      else if (storeName.toLowerCase().includes('no frills')) storeName = 'No Frills';
      else if (storeName.toLowerCase().includes('canadian tire')) storeName = 'Canadian Tire';
      else if (storeName.toLowerCase().includes('metro')) storeName = 'Metro';
      else if (storeName.toLowerCase().includes('sobeys')) storeName = 'Sobeys';
      else if (storeName.toLowerCase().includes('shoppers')) storeName = 'Shoppers Drug Mart';
      
      if (!storeGroups[storeName]) {
        storeGroups[storeName] = [];
      }
      storeGroups[storeName].push(item);
    });
    
    console.log(`Grouped items into ${Object.keys(storeGroups).length} unique stores:`, Object.keys(storeGroups));
    
    // Convert to flyer format - ONE FLYER PER STORE with ALL items for that store
    const flyers = await Promise.all(
      Object.entries(storeGroups).map(async ([storeName, allStoreItems]) => {
        const firstItem = allStoreItems[0];
        const storeId = storeName.toLowerCase().replace(/[^a-z0-9]/g, '');
        
        // Try to get enhanced store details
        const storeDetails = await fetchStoreDetails(firstItem.merchant?.id || storeId);
        
        const enhancedStoreLogo = storeDetails?.logo_url || 
                                 firstItem.merchant?.logo_url || 
                                 firstItem.merchant?.image_url ||
                                 `https://logo.clearbit.com/${storeId}.ca` ||
                                 `https://via.placeholder.com/60x60/0071ce/ffffff?text=${storeName.charAt(0)}`;
        
        return {
          id: `${storeId}-flyer-${Date.now()}`,
          storeName,
          storeId,
          storeLogo: enhancedStoreLogo,
          validFrom: firstItem.valid_from || new Date().toISOString().split('T')[0],
          validUntil: firstItem.valid_to || new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          pageCount: Math.ceil(allStoreItems.length / 8), // Better pagination based on all items
          previewImage: firstItem.flyer_image_url || 
                       firstItem.store_flyer_url ||
                       `https://via.placeholder.com/300x400/f8f8f8/333?text=${encodeURIComponent(storeName)}+Weekly+Flyer`,
          items: allStoreItems.map((item, itemIndex) => {
            // Enhanced price extraction
            const salePrice = parseFloat(item.sale_price || item.price || item.current_price || '0');
            const originalPrice = parseFloat(item.price || item.original_price || item.regular_price || salePrice || '0');
            const discount = salePrice < originalPrice ? Math.round(((originalPrice - salePrice) / originalPrice) * 100) : 0;
            
            // Enhanced image URL selection with Flipp API field names
            const imageUrl = item.clean_image_url || 
                           item.clipping_image_url ||
                           item.large_image_url || 
                           item.image_url || 
                           item.product_image_url ||
                           item.thumbnail_url ||
                           item.images?.[0]?.url ||
                           `https://via.placeholder.com/200x200/f8f8f8/666?text=${encodeURIComponent(item.name || item.title || 'Product')}`;
            
            // Enhanced title and description extraction
            const title = item.name || item.title || item.product_name || item.display_name || 'Product';
            const description = item.description || 
                              item.sale_story || 
                              item.product_description ||
                              item.details ||
                              '';
            
            return {
              id: `${storeId}-item-${itemIndex}-${Date.now()}`,
              store: storeName,
              storeLogo: enhancedStoreLogo,
              title: title,
              price: salePrice,
              originalPrice: originalPrice,
              discountPercent: discount,
              imageUrl: imageUrl,
              validUntil: item.valid_to || item.end_date || new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
              category: item.category?.name || 
                       item.category_name || 
                       item.product_category ||
                       'General',
              description: description
            };
          })
          .sort((a, b) => b.discountPercent - a.discountPercent) // Sort by highest discount first
          .slice(0, 20) // Limit to 20 best items per store to avoid overcrowding
        };
      })
    );
    
    console.log('Enhanced flyers conversion completed:', flyers.length, 'flyers created');
    return flyers;
  };

  // Enhanced mock data with better images and detailed product information
  const mockFlyers: Flyer[] = [
    {
      id: 'walmart-001',
      storeName: 'Walmart',
      storeId: 'walmart',
      storeLogo: 'https://logo.clearbit.com/walmart.ca',
      validFrom: '2025-09-02',
      validUntil: '2025-09-08',
      pageCount: 12,
      previewImage: 'https://flipp.com/shopper_assets/banner_images/1000010983.png',
      items: [
        {
          id: 'walmart-item-1',
          store: 'Walmart',
          storeLogo: 'https://logo.clearbit.com/walmart.ca',
          title: 'Great Value Peanut Butter 1kg',
          price: 4.97,
          originalPrice: 6.97,
          discountPercent: 29,
          imageUrl: 'https://picsum.photos/200/200?random=10',
          validUntil: '2025-09-08',
          category: 'Grocery',
          description: 'Smooth peanut butter, 1kg jar - Great for families'
        },
        {
          id: 'walmart-item-2',
          store: 'Walmart',
          storeLogo: 'https://logo.clearbit.com/walmart.ca',
          title: 'Samsung 65" 4K Smart TV',
          price: 699.99,
          originalPrice: 899.99,
          discountPercent: 22,
          imageUrl: 'https://picsum.photos/200/200?random=11',
          validUntil: '2025-09-08',
          category: 'Electronics',
          description: 'Crystal UHD 4K Smart TV with built-in streaming apps'
        },
        {
          id: 'walmart-item-3',
          store: 'Walmart',
          storeLogo: 'https://logo.clearbit.com/walmart.ca',
          title: 'Instant Pot Duo 7-in-1',
          price: 89.99,
          originalPrice: 129.99,
          discountPercent: 31,
          imageUrl: 'https://picsum.photos/200/200?random=12',
          validUntil: '2025-09-08',
          category: 'Home & Kitchen',
          description: '6-quart electric pressure cooker with 7 functions'
        }
      ]
    },
    {
      id: 'nofrills-001',
      storeName: 'No Frills',
      storeId: 'nofrills',
      storeLogo: 'https://logo.clearbit.com/nofrills.ca',
      validFrom: '2025-09-02',
      validUntil: '2025-09-08',
      pageCount: 8,
      previewImage: 'https://cdn.flyerquicksearch.com/no-frills-weekly-flyer/no-frills-weekly-flyer-cover.jpg',
      items: [
        {
          id: 'nofrills-item-1',
          store: 'No Frills',
          storeLogo: 'https://logo.clearbit.com/nofrills.ca',
          title: 'Bananas - Premium Quality',
          price: 1.48,
          originalPrice: 1.98,
          discountPercent: 25,
          imageUrl: 'https://picsum.photos/200/200?random=20',
          validUntil: '2025-09-08',
          category: 'Produce',
          description: 'Fresh bananas per lb - Perfect for snacking'
        },
        {
          id: 'nofrills-item-2',
          store: 'No Frills',
          storeLogo: 'https://logo.clearbit.com/nofrills.ca',
          title: 'Ground Beef Lean',
          price: 5.99,
          originalPrice: 7.99,
          discountPercent: 25,
          imageUrl: 'https://picsum.photos/200/200?random=21',
          validUntil: '2025-09-08',
          category: 'Meat',
          description: 'Extra lean ground beef, 1lb package'
        }
      ]
    },
    {
      id: 'canadiantire-001',
      storeName: 'Canadian Tire',
      storeId: 'canadiantire',
      storeLogo: 'https://logo.clearbit.com/canadiantire.ca',
      validFrom: '2025-09-02',
      validUntil: '2025-09-15',
      pageCount: 16,
      previewImage: 'https://cdn.flyerquicksearch.com/canadian-tire-weekly-flyer/canadian-tire-weekly-flyer.png',
      items: [
        {
          id: 'ct-item-1',
          store: 'Canadian Tire',
          storeLogo: 'https://logo.clearbit.com/canadiantire.ca',
          title: 'Craftsman 20V Drill Set',
          price: 129.99,
          originalPrice: 199.99,
          discountPercent: 35,
          imageUrl: 'https://picsum.photos/200/200?random=30',
          validUntil: '2025-09-15',
          category: 'Tools',
          description: 'Cordless drill with battery, charger, and carrying case'
        },
        {
          id: 'ct-item-2',
          store: 'Canadian Tire',
          storeLogo: 'https://logo.clearbit.com/canadiantire.ca',
          title: 'Winter Tires Set of 4',
          price: 599.99,
          originalPrice: 799.99,
          discountPercent: 25,
          imageUrl: 'https://picsum.photos/200/200?random=31',
          validUntil: '2025-09-15',
          category: 'Automotive',
          description: 'All-season winter tires, installation included'
        }
      ]
    },
    {
      id: 'loblaws-001',
      storeName: 'Loblaws',
      storeId: 'loblaws',
      storeLogo: 'https://logo.clearbit.com/loblaws.ca',
      validFrom: '2025-09-02',
      validUntil: '2025-09-08',
      pageCount: 10,
      previewImage: 'https://via.placeholder.com/300x400/ff6b35/ffffff?text=Loblaws+Weekly+Specials',
      items: [
        {
          id: 'loblaws-item-1',
          store: 'Loblaws',
          storeLogo: 'https://logo.clearbit.com/loblaws.ca',
          title: 'Presidents Choice Cookies',
          price: 2.99,
          originalPrice: 4.49,
          discountPercent: 33,
          imageUrl: 'https://picsum.photos/200/200?random=40',
          validUntil: '2025-09-08',
          category: 'Bakery',
          description: 'Chocolate chip cookies, family size package'
        },
        {
          id: 'loblaws-item-2',
          store: 'Loblaws',
          storeLogo: 'https://logo.clearbit.com/loblaws.ca',
          title: 'Atlantic Salmon Fillets',
          price: 12.99,
          originalPrice: 16.99,
          discountPercent: 24,
          imageUrl: 'https://picsum.photos/200/200?random=41',
          validUntil: '2025-09-08',
          category: 'Seafood',
          description: 'Fresh Atlantic salmon fillets, per lb'
        }
      ]
    }
  ];

  useEffect(() => {
    const fetchFlyers = async () => {
      setLoading(true);
      
      try {
        console.log('Attempting enhanced fetch from Flipp API...');
        
        // Try multiple search queries to get diverse products
        const queries = ['groceries', 'electronics', 'clothing', 'home'];
        let allItems: any[] = [];
        
        for (const query of queries) {
          console.log(`Fetching ${query} deals...`);
          const items = await fetchFlippData('M5V3A8', query, 25); // 25 items per category
          if (items && items.length > 0) {
            allItems = [...allItems, ...items];
            console.log(`Found ${items.length} ${query} items`);
          }
        }
        
        console.log(`Total items fetched: ${allItems.length}`);
        
        if (allItems && allItems.length > 0) {
          const convertedFlyers = await convertFlippDataToFlyers(allItems);
          console.log('Enhanced converted flyers:', convertedFlyers);
          
          if (convertedFlyers.length > 0) {
            setFlyers(convertedFlyers);
          } else {
            console.log('No flyers after conversion, using enhanced mock data');
            setFlyers(mockFlyers);
          }
        } else {
          console.log('No items from enhanced Flipp API, using mock data');
          setFlyers(mockFlyers);
        }
      } catch (error) {
        console.error('Enhanced fetch failed:', error);
        // If CORS is still an issue, log it clearly and use mock data
        if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
          console.log('CORS issue detected - using enhanced mock data as fallback');
        }
        setFlyers(mockFlyers);
      }
      
      setLoading(false);
    };

    fetchFlyers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Keyboard escape handler for modal
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && selectedFlyer) {
        setSelectedFlyer(null);
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [selectedFlyer]);

  const stores = ['all', ...Array.from(new Set(flyers.map(f => f.storeId)))];
  const filteredFlyers = selectedStore === 'all' 
    ? flyers 
    : flyers.filter(f => f.storeId === selectedStore);

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-CA', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="max-w-container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-penguin-charcoal mb-8">Weekly Flyers</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="bg-white rounded-lg shadow-md animate-pulse">
              <div className="h-48 bg-gray-300 rounded-t-lg"></div>
              <div className="p-4">
                <div className="h-4 bg-gray-300 rounded mb-2"></div>
                <div className="h-3 bg-gray-300 rounded mb-4"></div>
                <div className="h-3 bg-gray-300 rounded w-1/2"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
        <h1 className="text-3xl font-bold text-penguin-charcoal mb-4 md:mb-0">
          Weekly Flyers
        </h1>
        
        <div className="flex items-center space-x-4">
          <label htmlFor="store-filter" className="text-sm font-medium text-penguin-charcoal">
            Filter by Store:
          </label>
          <select
            id="store-filter"
            value={selectedStore}
            onChange={(e) => setSelectedStore(e.target.value)}
            className="border border-penguin-light-gray rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-penguin-ice-blue"
          >
            <option value="all">All Stores</option>
            {stores.filter(s => s !== 'all').map(store => (
              <option key={store} value={store}>
                {flyers.find(f => f.storeId === store)?.storeName || store}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {filteredFlyers.map(flyer => (
          <div key={flyer.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer"
               onClick={() => setSelectedFlyer(flyer)}>
            <div className="relative">
              <img
                src={flyer.previewImage}
                alt={`${flyer.storeName} flyer`}
                className="w-full h-48 object-cover rounded-t-lg"
              />
              <div className="absolute top-2 left-2 bg-white rounded-full p-1">
                <img
                  src={flyer.storeLogo}
                  alt={flyer.storeName}
                  className="w-8 h-8 object-contain"
                />
              </div>
            </div>
            
            <div className="p-4">
              <h3 className="font-bold text-lg text-penguin-charcoal mb-2">
                {flyer.storeName}
              </h3>
              <p className="text-sm text-gray-600 mb-2">
                Valid: {formatDate(flyer.validFrom)} - {formatDate(flyer.validUntil)}
              </p>
              <p className="text-sm text-gray-500">
                {flyer.pageCount} pages • {flyer.items.length} featured items
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Flyer Detail Modal */}
      {selectedFlyer && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          onClick={(e) => {
            if (e.target === e.currentTarget) {
              setSelectedFlyer(null);
            }
          }}
        >
          <div className="bg-white rounded-lg max-w-4xl max-h-[90vh] overflow-y-auto"
               onClick={(e) => e.stopPropagation()}>
            <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <img
                  src={selectedFlyer.storeLogo}
                  alt={selectedFlyer.storeName}
                  className="w-10 h-10 object-contain"
                />
                <div>
                  <h2 className="text-xl font-bold text-penguin-charcoal">
                    {selectedFlyer.storeName} Weekly Flyer
                  </h2>
                  <p className="text-sm text-gray-600">
                    Valid: {formatDate(selectedFlyer.validFrom)} - {formatDate(selectedFlyer.validUntil)}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setSelectedFlyer(null)}
                className="p-2 hover:bg-gray-100 rounded-full"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="p-6">
              {/* Featured Items */}
              <div className="mb-8">
                <h3 className="text-lg font-semibold mb-4">🌟 Featured Deals</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                  {selectedFlyer.items.map(item => (
                    <div key={item.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow bg-white">
                      <img
                        src={item.imageUrl}
                        alt={item.title}
                        className="w-full h-32 object-contain mb-3"
                        onError={(e) => {
                          (e.target as HTMLImageElement).src = `https://via.placeholder.com/200x200/f8f8f8/666?text=${encodeURIComponent(item.title || 'Product')}`;
                        }}
                      />
                      <h4 className="font-semibold text-sm mb-2 text-penguin-charcoal">
                        {item.title}
                      </h4>
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <span className="text-lg font-bold text-green-600">
                            ${item.price.toFixed(2)}
                          </span>
                          {item.originalPrice && item.originalPrice > item.price && (
                            <span className="text-sm text-gray-500 line-through">
                              ${item.originalPrice.toFixed(2)}
                            </span>
                          )}
                        </div>
                        {item.discountPercent && item.discountPercent > 0 && (
                          <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded-full">
                            {item.discountPercent}% OFF
                          </span>
                        )}
                      </div>
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span className="bg-gray-100 px-2 py-1 rounded">{item.category}</span>
                        <span>Valid until {formatDate(item.validUntil)}</span>
                      </div>
                      {item.description && (
                        <p className="text-xs text-gray-600 mt-2">{item.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Scrollable Flyer Pages */}
              <div className="mb-8">
                <h3 className="text-lg font-semibold mb-4">
                  📄 Complete {selectedFlyer.storeName} Flyer ({selectedFlyer.pageCount} pages)
                </h3>
                
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="max-h-[70vh] overflow-y-auto border-2 border-gray-200 rounded-lg bg-white">
                    <div className="space-y-4 p-4">
                      {/* Generate mock flyer pages */}
                      {Array.from({ length: selectedFlyer.pageCount }, (_, pageIndex) => (
                        <div key={pageIndex} className="relative">
                          <div className="bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg p-6 min-h-[400px] shadow-sm">
                            <div className="text-center">
                              <div className="text-xs text-gray-500 mb-4">Page {pageIndex + 1} of {selectedFlyer.pageCount}</div>
                              
                              {pageIndex === 0 && (
                                /* Cover Page */
                                <div>
                                  <div className="flex items-center justify-center mb-6">
                                    <img
                                      src={selectedFlyer.storeLogo}
                                      alt={selectedFlyer.storeName}
                                      className="w-16 h-16 object-contain mr-4"
                                    />
                                    <div>
                                      <h4 className="text-2xl font-bold text-gray-800">{selectedFlyer.storeName}</h4>
                                      <p className="text-gray-600">Weekly Specials</p>
                                    </div>
                                  </div>
                                  
                                  <div className="bg-red-500 text-white py-3 px-6 rounded-lg mb-4 inline-block">
                                    <div className="text-lg font-bold">SALE</div>
                                    <div className="text-sm">Valid {formatDate(selectedFlyer.validFrom)} - {formatDate(selectedFlyer.validUntil)}</div>
                                  </div>
                                  
                                  <img
                                    src={selectedFlyer.previewImage}
                                    alt="Cover"
                                    className="w-full max-w-sm mx-auto rounded-lg shadow-md"
                                    onError={(e) => {
                                      // Fallback to generic flyer image if store-specific fails
                                      (e.target as HTMLImageElement).src = `https://via.placeholder.com/400x600/f8f8f8/666?text=${selectedFlyer.storeName}+Weekly+Flyer`;
                                    }}
                                  />
                                </div>
                              )}
                              
                              {pageIndex > 0 && (
                                /* Inner Pages with Items */
                                <div className="grid grid-cols-2 gap-4">
                                  {selectedFlyer.items
                                    .slice((pageIndex - 1) * 4, pageIndex * 4)
                                    .map((item, itemIndex) => (
                                      <div key={itemIndex} className="bg-white rounded-lg p-4 shadow-sm">
                                        <img
                                          src={item.imageUrl}
                                          alt={item.title}
                                          className="w-full h-24 object-contain mb-2"
                                        />
                                        <h5 className="text-sm font-semibold text-gray-800 mb-1">{item.title}</h5>
                                        <div className="flex items-center justify-between">
                                          <span className="text-green-600 font-bold">${item.price.toFixed(2)}</span>
                                          {item.discountPercent && (
                                            <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded">
                                              {item.discountPercent}% OFF
                                            </span>
                                          )}
                                        </div>
                                      </div>
                                    ))}
                                  
                                  {/* Fill empty slots with placeholder deals */}
                                  {Array.from({ 
                                    length: Math.max(0, 4 - selectedFlyer.items.slice((pageIndex - 1) * 4, pageIndex * 4).length) 
                                  }, (_, emptyIndex) => (
                                    <div key={`empty-${emptyIndex}`} className="bg-white rounded-lg p-4 shadow-sm opacity-50">
                                      <div className="w-full h-24 bg-gray-200 rounded mb-2 flex items-center justify-center">
                                        <span className="text-gray-400 text-xs">Product</span>
                                      </div>
                                      <div className="text-sm text-gray-400 mb-1">More deals inside!</div>
                                      <div className="text-green-500 font-bold">$XX.XX</div>
                                    </div>
                                  ))}
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="text-center mt-4">
                    <p className="text-sm text-gray-600">
                      📱 Scroll up and down to browse all {selectedFlyer.pageCount} pages
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      Prices and availability may vary by location
                    </p>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Flyers;