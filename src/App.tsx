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
      <div className="min-h-screen bg-gray-50">
        <Header onSearch={handleSearch} />
        
        <Routes>
          <Route path="/" element={<HomePage searchQuery={searchQuery} />} />
          <Route path="/deals" element={<HomePage searchQuery={searchQuery} />} />
          <Route path="/about" element={<HomePage searchQuery={searchQuery} />} />
          <Route path="/coupons" element={<HomePage searchQuery={searchQuery} />} />
          <Route path="/amazon" element={<HomePage searchQuery={searchQuery} />} />
        </Routes>
        
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
    </Router>
  );
}

export default App;
// Force rebuild: 2025-07-31 17:50