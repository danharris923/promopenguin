import React, { useState, useEffect } from 'react';

interface AmazonCategory {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  color: string;
  icon: string;
  badge?: string;
  link: string; // Will be populated with Amazon affiliate links
}

interface AdditionalDeal {
  id: string;
  title: string;
  affiliateUrl: string;
  dateAdded: string;
  description?: string;
  price?: number;
  originalPrice?: number;
  discountPercent?: number;
  imageUrl?: string;
}

const AmazonPage: React.FC = () => {
  const [additionalDeals, setAdditionalDeals] = useState<AdditionalDeal[]>([]);
  const [loading, setLoading] = useState(true);

  // Fetch additional deals from local file
  useEffect(() => {
    const fetchAdditionalDeals = async () => {
      try {
        const response = await fetch('/additional_deals.json');
        if (response.ok) {
          const deals = await response.json();
          setAdditionalDeals(deals.slice(0, 6)); // Show first 6 deals
        }
      } catch (error) {
        console.log('No additional deals file found');
      } finally {
        setLoading(false);
      }
    };

    fetchAdditionalDeals();
  }, []);
  const categories: AmazonCategory[] = [
    {
      id: 'todays-deals',
      title: "Today's Deals",
      subtitle: 'BEST SAVINGS',
      description: 'Lightning deals and limited-time offers updated daily',
      color: 'bg-gradient-to-br from-orange-400 to-orange-600',
      icon: '⚡',
      badge: 'BEST SAVINGS',
      link: 'https://www.amazon.ca/deals?ie=UTF8&bubble-id=deals-collection-coupons&linkCode=ll2&tag=promopenguin-20&linkId=b343da55fa2b2182e69724988afc8f7c&language=en_CA&ref_=as_li_ss_tl'
    },
    {
      id: 'outlet-deals',
      title: 'Outlet Deals',
      subtitle: '',
      description: 'Deep discounts on overstock and clearance items',
      color: 'bg-gradient-to-br from-purple-500 to-purple-700',
      icon: '🏷️',
      link: 'https://www.amazon.ca/b?ie=UTF8&node=9833876011&linkCode=ll2&tag=promopenguin-20&linkId=011b4d47495f204c50045ed064d72cd2&language=en_CA&ref_=as_li_ss_tl'
    },
    {
      id: 'amazon-resale',
      title: 'Amazon Resale',
      subtitle: '',
      description: 'Quality pre-owned items at discounted prices',
      color: 'bg-gradient-to-br from-green-500 to-green-700',
      icon: '♻️',
      link: 'https://www.amazon.ca/b?ie=UTF8&node=8929975011&linkCode=ll2&tag=promopenguin-20&linkId=6b7cd5d6bf68fbc0813f8aca9d1082a3&language=en_CA&ref_=as_li_ss_tl'
    },
    {
      id: 'coupons',
      title: 'Coupons',
      subtitle: 'EXTRA SAVINGS',
      description: 'Clip and save with exclusive Amazon coupons',
      color: 'bg-gradient-to-br from-blue-500 to-blue-700',
      icon: '✂️',
      badge: 'EXTRA SAVINGS',
      link: 'https://www.amazon.ca/deals?ie=UTF8&bubble-id=deals-collection-coupons&linkCode=ll2&tag=promopenguin-20&linkId=254cd138770c1811465cd911440ea141&language=en_CA&ref_=as_li_ss_tl'
    },
    {
      id: 'subscribe-save',
      title: 'Subscribe & Save',
      subtitle: '',
      description: 'Save up to 15% on recurring deliveries',
      color: 'bg-gradient-to-br from-teal-500 to-teal-700',
      icon: '📦',
      link: 'https://www.amazon.ca/Subscribe/b?ie=UTF8&node=6583741011&linkCode=ll2&tag=promopenguin-20&linkId=cab34b61baa6f9ade6229bc48931e06e&language=en_CA&ref_=as_li_ss_tl'
    },
    {
      id: 'prime-exclusive',
      title: 'Prime Exclusive',
      subtitle: 'PRIME ONLY',
      description: 'Special deals for Prime members only',
      color: 'bg-gradient-to-br from-indigo-500 to-indigo-700',
      icon: '👑',
      badge: 'PRIME ONLY',
      link: 'https://www.amazon.ca/amazonprime?&linkCode=ll2&tag=promopenguin-20&linkId=82f6fdbfe7140a91188e200c047cfb61&language=en_CA&ref_=as_li_ss_tl'
    }
  ];

  const benefits = [
    {
      icon: '🚚',
      title: 'Fast Shipping',
      description: 'Prime members get free 2-day shipping on millions of items'
    },
    {
      icon: '↩️',
      title: 'Easy Returns',
      description: 'Hassle-free returns within 30 days on most items'
    },
    {
      icon: '✅',
      title: 'Verified Reviews',
      description: 'Make informed decisions with millions of customer reviews'
    }
  ];

  return (
    <div className="min-h-screen bg-penguin-black">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-penguin-charcoal to-penguin-ice-blue-dark">
        <div className="max-w-container mx-auto px-4 py-12 text-center">
          <div className="flex justify-center items-center mb-6">
            <img 
              src="https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg" 
              alt="Amazon" 
              className="h-12 mr-4 bg-white px-3 py-2 rounded-lg"
            />
            <span className="text-4xl">🐧</span>
          </div>
          
          <h1 className="text-4xl md:text-5xl font-bold text-penguin-white mb-4">
            Amazon Deal Categories
          </h1>
          
          <p className="text-lg text-blue-100 mb-6">
            Discover the best savings across Amazon's special deal sections
          </p>
          
          <div className="inline-flex items-center bg-penguin-ice-blue text-penguin-black px-4 py-2 rounded-full text-sm font-medium">
            <span className="mr-2">👆</span>
            Click any card to explore deals
            <span className="ml-2">👆</span>
          </div>
        </div>
      </div>

      {/* Categories Grid */}
      <div className="max-w-container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {categories.map(category => (
            <div
              key={category.id}
              className={`${category.color} rounded-2xl p-8 text-white shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 cursor-pointer relative overflow-hidden`}
              onClick={() => window.open(category.link, '_blank')}
            >
              {/* Badge */}
              {category.badge && (
                <div className="absolute top-4 right-4 bg-white text-gray-800 text-xs font-bold px-3 py-1 rounded-full">
                  {category.badge}
                </div>
              )}
              
              {/* Icon */}
              <div className="text-4xl mb-4">
                {category.icon}
              </div>
              
              {/* Content */}
              <h3 className="text-2xl font-bold mb-3">
                {category.title}
              </h3>
              
              <p className="text-white/90 mb-6 leading-relaxed">
                {category.description}
              </p>
              
              {/* Button */}
              <button className="bg-white/20 hover:bg-white/30 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 backdrop-blur-sm border border-white/30">
                BROWSE DEALS →
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* SavingsGuru Deals Section */}
      <div className="bg-penguin-black">
        <div className="max-w-container mx-auto px-4 py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-penguin-white mb-4">
              🔥 Latest Additional Deals
            </h2>
            <p className="text-gray-300 mb-6">
              Fresh deals and savings opportunities from additional sources
            </p>
          </div>
          
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-penguin-charcoal rounded-lg p-6 animate-pulse">
                  <div className="h-4 bg-penguin-dark-gray rounded mb-3"></div>
                  <div className="h-3 bg-penguin-dark-gray rounded mb-2"></div>
                  <div className="h-3 bg-penguin-dark-gray rounded w-1/2"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {additionalDeals.map((deal) => (
                <div
                  key={deal.id}
                  className="bg-penguin-charcoal rounded-lg p-6 border border-penguin-ice-blue/20 hover:border-penguin-ice-blue/40 transition-colors cursor-pointer"
                  onClick={() => window.open(deal.affiliateUrl, '_blank')}
                >
                  {deal.imageUrl && (
                    <div className="w-full h-32 bg-penguin-dark-gray rounded-lg mb-4 overflow-hidden">
                      <img 
                        src={deal.imageUrl} 
                        alt={deal.title}
                        className="w-full h-full object-contain p-2"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none';
                        }}
                      />
                    </div>
                  )}
                  <h3 className="text-lg font-semibold text-penguin-white mb-3 line-clamp-2">
                    {deal.title}
                  </h3>
                  {deal.price && (
                    <div className="flex items-baseline gap-2 mb-3">
                      <span className="text-penguin-ice-blue font-bold text-lg">${deal.price}</span>
                      {deal.originalPrice && (
                        <span className="text-gray-400 line-through text-sm">${deal.originalPrice}</span>
                      )}
                      {deal.discountPercent && (
                        <span className="bg-red-500 text-white text-xs px-2 py-1 rounded">
                          {deal.discountPercent}% OFF
                        </span>
                      )}
                    </div>
                  )}
                  <p className="text-sm text-gray-400 mb-4">
                    {new Date(deal.dateAdded).toLocaleDateString()}
                  </p>
                  <button className="text-penguin-ice-blue hover:text-penguin-ice-blue-dark font-medium text-sm transition-colors">
                    View Deal →
                  </button>
                </div>
              ))}
            </div>
          )}
          
          <div className="text-center mt-8">
            <button 
              onClick={() => window.location.href = '/'}
              className="bg-gradient-to-r from-penguin-ice-blue-dark to-penguin-ice-blue text-penguin-black font-bold py-3 px-6 rounded-lg hover:from-penguin-ice-blue hover:to-penguin-ice-blue-dark transition-all"
            >
              View All Deals →
            </button>
          </div>
        </div>
      </div>

      {/* Why Shop Amazon Deals Section */}
      <div className="bg-penguin-charcoal">
        <div className="max-w-container mx-auto px-4 py-16">
          <h2 className="text-3xl font-bold text-center text-penguin-white mb-12">
            Why Shop Amazon Deals?
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {benefits.map((benefit, index) => (
              <div key={index} className="text-center p-6 rounded-lg bg-penguin-dark-gray border border-penguin-ice-blue/20 hover:border-penguin-ice-blue/40 transition-colors">
                <div className="text-4xl mb-4">
                  {benefit.icon}
                </div>
                <h3 className="text-xl font-semibold text-penguin-white mb-3">
                  {benefit.title}
                </h3>
                <p className="text-gray-300">
                  {benefit.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Affiliate Disclosure */}
      <div className="bg-penguin-black border-t border-penguin-dark-gray">
        <div className="max-w-container mx-auto px-4 py-8">
          <div className="text-center text-sm text-gray-400 bg-penguin-charcoal rounded-lg p-6 border border-penguin-ice-blue/20">
            <p className="mb-2">
              As an Amazon Associate, we earn from qualifying purchases. 
              <span className="font-medium text-penguin-white"> This helps support our site at no extra cost to you!</span>
            </p>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="bg-penguin-charcoal">
        <div className="max-w-container mx-auto px-4 py-12 text-center">
          <h2 className="text-2xl font-bold text-white mb-4">
            New deals are added daily!
          </h2>
          <p className="text-penguin-ice-blue mb-8">
            Bookmark this page and check back regularly for the latest Amazon savings.
          </p>
          <button 
            onClick={() => window.open('https://amazon.ca/?tag=promopenguin-20', '_blank')}
            className="bg-gradient-to-r from-penguin-ice-blue-dark to-penguin-ice-blue hover:from-penguin-ice-blue hover:to-penguin-ice-blue-dark text-penguin-black font-bold py-4 px-8 rounded-lg text-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            🐧 Start Saving on Amazon →
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-penguin-black">
        <div className="max-w-container mx-auto px-4 py-8 text-center">
          <h3 className="text-xl font-bold text-white mb-2">
            PromoPenguin
          </h3>
          <p className="text-gray-400 text-sm">
            PromoPenguin helps you waddle to the best savings by finding you coupons, deals, and the lowest prices EVER!
          </p>
        </div>
      </div>
    </div>
  );
};

export default AmazonPage;