import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './components/HomePage';
import AboutPage from './components/AboutPage';
import CouponsPage from './components/CouponsPage';

function App() {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };
  return (
    <Router>
      <div className="min-h-screen bg-penguin-black">
        <Header onSearch={handleSearch} />
        
        <Routes>
          <Route path="/" element={<HomePage searchQuery={searchQuery} />} />
          <Route path="/deals" element={<HomePage searchQuery={searchQuery} />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/coupons" element={<CouponsPage />} />
          <Route path="/amazon" element={<HomePage searchQuery={searchQuery} />} />
        </Routes>
        
        <footer className="bg-penguin-charcoal border-t border-penguin-dark-gray mt-12">
          <div className="max-w-container mx-auto px-4 py-8">
            <div className="text-center">
              <h3 className="text-xl font-bold text-penguin-white mb-2">PromoPenguin</h3>
              <p className="text-gray-400 mb-4">
                Waddle your way to savings with the coolest deals in Canada! 🐧
              </p>
              <p className="text-sm text-gray-500">
                © 2025 PromoPenguin. All deals are ice-cold fresh.
              </p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
// Force rebuild: 2025-07-31 17:50