import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import DealCard from './components/DealCard';
import DealModal from './components/DealModal';
import Sidebar from './components/Sidebar';
import { Deal } from './types/Deal';

function App() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);

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

  const topDeals = deals
    .filter(deal => deal.featured)
    .sort((a, b) => b.discountPercent - a.discountPercent)
    .slice(0, 5);

  const mainDeals = deals.sort((a, b) => 
    new Date(b.dateAdded).getTime() - new Date(a.dateAdded).getTime()
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-container mx-auto px-4 py-6">
        <div className="flex flex-col lg:flex-row gap-6">
          <div className="flex-1">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-text-dark mb-1">Latest Deals</h2>
              <p className="text-gray-600">Discover amazing savings on top products</p>
            </div>
            
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-80 bg-gray-200 rounded-lg animate-pulse" />
                ))}
              </div>
            ) : (
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
            )}
          </div>
          
          <Sidebar 
            topDeals={topDeals}
            onDealClick={handleDealClick}
          />
        </div>
      </main>
      
      <DealModal
        deal={selectedDeal}
        isOpen={modalOpen}
        onClose={handleCloseModal}
      />
      
      <footer className="bg-white border-t mt-12">
        <div className="max-w-container mx-auto px-4 py-8">
          <div className="text-center">
            <h3 className="text-xl font-bold text-text-dark mb-2">SavingsGuru</h3>
            <p className="text-gray-600 mb-4">
              The Savings Guru helps you save money by finding you coupons, deals, and the lowest prices EVER!
            </p>
            <p className="text-sm text-gray-500">
              © 2025 SavingsGuru. All deals are legendary deals.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;