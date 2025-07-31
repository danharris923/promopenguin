// Test the smart pricing logic
import { getSmartDealLabel } from './dealUtils';

const testDeals = [
  { original: 149.99, current: 89.99, title: "VASAGLE Bakers Rack" },
  { original: 5.49, current: 3.99, title: "Snack Factory Pretzel Crisps" },
  { original: 199.99, current: 119.99, title: "TEEHO Door Lock" },
  { original: 39.99, current: 24.99, title: "CTHH 4 Pack Leggings" },
  { original: 52.99, current: 32.99, title: "PRETTYGARDEN Cardigan" }
];

console.log("🧠 Smart Pricing Psychology Test\n");

testDeals.forEach(deal => {
  const savings = deal.original - deal.current;
  const percent = Math.round((savings / deal.original) * 100);
  const result = getSmartDealLabel(deal.original, deal.current);
  
  console.log(`📦 ${deal.title}`);
  console.log(`   Price: $${deal.current} (was $${deal.original})`);
  console.log(`   Savings: $${savings.toFixed(2)} (${percent}%)`);
  console.log(`   Display: ${result.primary}${result.secondary ? ` + "${result.secondary}"` : ''}`);
  console.log(`   Logic: ${result.showPercent ? 'Show % OFF' : 'Show $ OFF'}`);
  console.log('');
});

// Quick test in browser console:
// Run this to see the output