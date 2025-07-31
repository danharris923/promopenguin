// Test with actual deal IDs from deals.json
const dealIds = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1];

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
  const hash = hashString(String(dealId));
  return hash % 5 === 0; // 20% instead of 10%
}

const messages = [
  "Check Price on Amazon",
  "See Price at Amazon", 
  "View Amazon Price",
  "Get Best Price",
  "Check Current Price",
  "See Deal Price",
  "Amazon Price Check",
  "View Special Price"
];

function getRandomCheckPriceMessage(dealId) {
  const hash = hashString(String(dealId));
  return messages[hash % messages.length];
}

console.log("🎯 Actual Deal ID Test:\n");

let showingPrice = 0;
dealIds.forEach(dealId => {
  const show = shouldShowPrice(dealId);
  const message = show ? 'SHOWS PRICE' : getRandomCheckPriceMessage(dealId);
  if (show) showingPrice++;
  console.log(`${show ? '💰' : '❓'} Deal ID: ${dealId} - ${show ? 'SHOWS PRICE' : message}`);
});

console.log(`\n📊 Result: ${showingPrice}/${dealIds.length} deals showing prices (${showingPrice/dealIds.length*100}%)`);