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
      <div className="bg-penguin-charcoal">
        <div className="max-w-container mx-auto px-4 py-4 md:py-6">
          <div className="flex items-center">
            <h1 className="text-2xl md:text-4xl font-bold text-penguin-white">
              <a href="/" className="flex items-center">
                <span className="bg-penguin-ice-blue text-penguin-black px-3 py-1 rounded-lg font-display">PromoPenguin</span>
              </a>
            </h1>
            <p className="ml-4 text-penguin-ice-blue text-sm md:text-base hidden md:block">
              Waddle to the best deals! 🐧
            </p>
          </div>
        </div>
      </div>
      
      <nav className="bg-penguin-black border-b border-penguin-dark-gray">
        <div className="max-w-container mx-auto px-4">
          <div className="flex items-center justify-between h-14">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 text-penguin-white"
              aria-label="Toggle menu"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            
            <div className="hidden md:flex items-center space-x-6">
              <a href="/" className="text-penguin-white hover:text-penguin-ice-blue font-medium transition-colors">HOME</a>
              <a href="/deals" className="text-penguin-white hover:text-penguin-ice-blue transition-colors">DEALS</a>
              <a href="/coupons" className="text-penguin-white hover:text-penguin-ice-blue transition-colors">COUPONS</a>
              <a href="/amazon" className="text-penguin-white hover:text-penguin-ice-blue transition-colors">AMAZON</a>
              <a href="/about" className="text-penguin-white hover:text-penguin-ice-blue transition-colors">ABOUT</a>
            </div>
            
            <form onSubmit={handleSearchSubmit} className="flex items-center">
              <input
                type="search"
                placeholder="Search deals..."
                value={searchQuery}
                onChange={handleSearchChange}
                className="border border-penguin-dark-gray bg-penguin-charcoal text-penguin-white rounded-lg px-3 py-1.5 text-sm w-32 md:w-48 focus:outline-none focus:border-penguin-ice-blue placeholder-gray-400"
              />
              <button type="submit" className="ml-2 p-1.5 text-penguin-white hover:text-penguin-ice-blue transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </form>
          </div>
          
          {mobileMenuOpen && (
            <div className="md:hidden py-3 border-t border-penguin-dark-gray">
              <a href="/" className="block py-2 text-penguin-white hover:text-penguin-ice-blue font-medium transition-colors">HOME</a>
              <a href="/deals" className="block py-2 text-penguin-white hover:text-penguin-ice-blue transition-colors">DEALS</a>
              <a href="/coupons" className="block py-2 text-penguin-white hover:text-penguin-ice-blue transition-colors">COUPONS</a>
              <a href="/amazon" className="block py-2 text-penguin-white hover:text-penguin-ice-blue transition-colors">AMAZON</a>
              <a href="/about" className="block py-2 text-penguin-white hover:text-penguin-ice-blue transition-colors">ABOUT</a>
            </div>
          )}
        </div>
      </nav>
    </header>
  );
};

export default Header;