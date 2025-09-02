import React from 'react';

const CouponsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-penguin-black">
      {/* Coming Soon Hero */}
      <div className="bg-gradient-to-r from-penguin-charcoal to-penguin-ice-blue-dark text-white">
        <div className="max-w-container mx-auto px-4 py-20">
          <div className="text-center">
            <div className="text-6xl mb-6">🎫</div>
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Exclusive Coupons Coming Soon!
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100">
              We're building something amazing for Canadian coupon lovers
            </p>
            <div className="bg-penguin-ice-blue/20 backdrop-blur-sm rounded-2xl p-6 max-w-2xl mx-auto border border-penguin-ice-blue/30">
              <h2 className="text-2xl font-bold mb-4">Get Ready For:</h2>
              <div className="grid md:grid-cols-2 gap-4 text-left">
                <ul className="space-y-2">
                  <li className="flex items-center">
                    <span className="text-yellow-300 mr-3">⭐</span>
                    <span>Exclusive Canadian store coupons</span>
                  </li>
                  <li className="flex items-center">
                    <span className="text-yellow-300 mr-3">⭐</span>
                    <span>Printable grocery coupons</span>
                  </li>
                  <li className="flex items-center">
                    <span className="text-yellow-300 mr-3">⭐</span>
                    <span>Digital promo codes</span>
                  </li>
                </ul>
                <ul className="space-y-2">
                  <li className="flex items-center">
                    <span className="text-yellow-300 mr-3">⭐</span>
                    <span>Restaurant & food deals</span>
                  </li>
                  <li className="flex items-center">
                    <span className="text-yellow-300 mr-3">⭐</span>
                    <span>Travel & entertainment</span>
                  </li>
                  <li className="flex items-center">
                    <span className="text-yellow-300 mr-3">⭐</span>
                    <span>Local business offers</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 py-16">
        
        {/* What's Coming */}
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-penguin-white mb-8">
            🚀 The Ultimate Canadian Coupon Experience
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-penguin-charcoal p-8 rounded-2xl border border-penguin-ice-blue/20">
              <div className="text-4xl mb-4">💳</div>
              <h3 className="text-xl font-bold mb-4 text-penguin-white">Smart Coupon Matching</h3>
              <p className="text-gray-300">
                Our AI will automatically match the best coupons to your shopping list, 
                so you never miss a saving opportunity.
              </p>
            </div>
            
            <div className="bg-penguin-charcoal p-8 rounded-2xl border border-penguin-ice-blue/20">
              <div className="text-4xl mb-4">📱</div>
              <h3 className="text-xl font-bold mb-4 text-penguin-white">Mobile Wallet Integration</h3>
              <p className="text-gray-300">
                Add coupons directly to your phone's wallet for easy access at checkout. 
                No more forgotten paper coupons!
              </p>
            </div>
            
            <div className="bg-penguin-charcoal p-8 rounded-2xl border border-penguin-ice-blue/20">
              <div className="text-4xl mb-4">🏪</div>
              <h3 className="text-xl font-bold mb-4 text-penguin-white">Local Store Partners</h3>
              <p className="text-gray-300">
                Exclusive partnerships with Canadian retailers for members-only 
                coupons you can't find anywhere else.
              </p>
            </div>
          </div>
        </div>

        {/* Notify Me Section */}
        <div className="bg-gradient-to-r from-penguin-ice-blue-dark to-penguin-ice-blue text-penguin-black p-8 rounded-2xl text-center mb-16">
          <h2 className="text-3xl font-bold mb-4">Be The First To Know!</h2>
          <p className="text-xl mb-6 text-blue-800">
            Get notified the moment our coupon site launches with exclusive early-bird offers
          </p>
          <div className="max-w-md mx-auto">
            <div className="flex flex-col sm:flex-row gap-4">
              <input 
                type="email" 
                placeholder="Enter your email..." 
                className="flex-1 px-4 py-3 rounded-full text-gray-900 focus:outline-none focus:ring-2 focus:ring-penguin-charcoal"
              />
              <button className="bg-penguin-charcoal text-penguin-white px-6 py-3 rounded-full font-bold hover:bg-penguin-black transition-all">
                Notify Me! 🔔
              </button>
            </div>
          </div>
        </div>

        {/* Browse Current Deals */}
        <div className="text-center">
          <h2 className="text-2xl font-bold text-penguin-white mb-4">
            While You Wait, Check Out Our Hot Deals!
          </h2>
          <p className="text-gray-300 mb-8">
            Don't miss out on amazing savings happening right now
          </p>
          <a 
            href="/" 
            className="inline-flex items-center bg-penguin-ice-blue text-penguin-black px-8 py-4 rounded-full font-bold text-lg hover:bg-blue-400 transition-all shadow-lg"
          >
            🔥 Browse Current Deals
            <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </a>
        </div>
      </div>
    </div>
  );
};

export default CouponsPage;