// Quick test to see which deals show prices vs "Check Price"
const deals = [
  { id: "1", title: "VASAGLE Bakers Rack" },
  { id: "2", title: "Snack Factory Pretzel Crisps" },
  { id: "3", title: "OREO Cakesters" },
  { id: "4", title: "OREO Cakesters (duplicate)" },
  { id: "5", title: "TEEHO Door Lock" },
  { id: "6", title: "CTHH Leggings" },
  { id: "7", title: "Vtopmart Container Set" },
  { id: "8", title: "PRETTYGARDEN Cardigan" },
  { id: "9", title: "Crayan Mattress" },
  { id: "10", title: "Howdy Rodeo Shirt" }
];

// Simple hash function
function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash);
}

function shouldShowPrice(dealId) {
  const hash = hashString(dealId);
  return hash % 10 === 0;
}

console.log("🎯 Price Visibility Test (10% should show prices):\n");

let showingPrice = 0;
deals.forEach(deal => {
  const show = shouldShowPrice(deal.id);
  if (show) showingPrice++;
  console.log(`${show ? '💰' : '❓'} ID: ${deal.id} - ${deal.title} - ${show ? 'SHOWS PRICE' : 'CHECK PRICE BUTTON'}`);
});

console.log(`\n📊 Result: ${showingPrice}/${deals.length} deals showing prices (${showingPrice/deals.length*100}%)`);

// You can run this in browser console to test