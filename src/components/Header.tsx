import React, { useState } from 'react';

interface HeaderProps {
  onSearch?: (query: string) => void;
}

const Header: React.FC<HeaderProps> = ({ onSearch }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    if (onSearch) {
      onSearch(query);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(searchQuery);
    }
  };

  return (
    <header>
      <div className="bg-primary-green">
        <div className="max-w-container mx-auto px-4 py-4 md:py-6">
          <div className="flex items-center">
            <h1 className="text-2xl md:text-4xl font-bold text-white">
              <a href="/" className="flex items-center">
                <span className="bg-white text-primary-green px-3 py-1 rounded">SavingsGuru</span>
              </a>
            </h1>
            <p className="ml-4 text-white text-sm md:text-base hidden md:block">
              Helping you save money!
            </p>
          </div>
        </div>
      </div>
      
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-container mx-auto px-4">
          <div className="flex items-center justify-between h-14">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2"
              aria-label="Toggle menu"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            
            <div className="hidden md:flex items-center space-x-6">
              <a href="/" className="text-text-dark hover:text-primary-green font-medium">HOME</a>
              <a href="/deals" className="text-text-dark hover:text-primary-green">ONLINE DEALS</a>
              <a href="/coupons" className="text-text-dark hover:text-primary-green">COUPONS</a>
              <a href="/amazon" className="text-text-dark hover:text-primary-green">AMAZON</a>
              <a href="/about" className="text-text-dark hover:text-primary-green">ABOUT US</a>
            </div>
            
            <form onSubmit={handleSearchSubmit} className="flex items-center">
              <input
                type="search"
                placeholder="Search deals..."
                value={searchQuery}
                onChange={handleSearchChange}
                className="border border-gray-300 rounded px-3 py-1.5 text-sm w-32 md:w-48 focus:outline-none focus:border-primary-green"
              />
              <button type="submit" className="ml-2 p-1.5">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </form>
          </div>
          
          {mobileMenuOpen && (
            <div className="md:hidden py-3 border-t">
              <a href="/" className="block py-2 text-text-dark hover:text-primary-green font-medium">HOME</a>
              <a href="/deals" className="block py-2 text-text-dark hover:text-primary-green">ONLINE DEALS</a>
              <a href="/coupons" className="block py-2 text-text-dark hover:text-primary-green">COUPONS</a>
              <a href="/amazon" className="block py-2 text-text-dark hover:text-primary-green">AMAZON</a>
              <a href="/about" className="block py-2 text-text-dark hover:text-primary-green">ABOUT US</a>
            </div>
          )}
        </div>
      </nav>
    </header>
  );
};

export default Header;