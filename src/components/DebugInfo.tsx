import React from 'react';
import { getPriceVisibility } from '../utils/priceVisibility';

const DebugInfo: React.FC = () => {
  const testDeals = [
    { id: "1", title: "Deal 1" },
    { id: "2", title: "Deal 2" },
    { id: "3", title: "Deal 3" },
    { id: "4", title: "Deal 4" },
    { id: "5", title: "Deal 5" },
    { id: "6", title: "Deal 6" },
    { id: "7", title: "Deal 7" },
    { id: "8", title: "Deal 8" },
    { id: "9", title: "Deal 9" },
    { id: "10", title: "Deal 10" }
  ];

  const showingPriceCount = testDeals.filter(deal => getPriceVisibility(deal.id).showPrice).length;

  return (
    <div className="bg-yellow-100 border border-yellow-400 rounded p-4 mb-4">
      <h3 className="font-bold mb-2">🐛 Debug: Price Visibility Test</h3>
      <p className="text-sm mb-2">Expected: ~10% show prices, ~90% show "Check Price"</p>
      <p className="text-sm font-bold mb-2">Result: {showingPriceCount}/10 deals showing prices ({showingPriceCount * 10}%)</p>
      
      <div className="grid grid-cols-2 gap-2 text-xs">
        {testDeals.map(deal => {
          const visibility = getPriceVisibility(deal.id);
          return (
            <div key={deal.id} className={`p-2 rounded ${visibility.showPrice ? 'bg-green-200' : 'bg-red-200'}`}>
              ID: {deal.id} - {visibility.showPrice ? '💰 SHOW PRICE' : '❓ CHECK PRICE'}
              {!visibility.showPrice && (
                <div className="text-xs opacity-75">{visibility.checkPriceMessage}</div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DebugInfo;