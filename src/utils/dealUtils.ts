export interface DealLabelResult {
  primary: string;
  secondary?: string;
  showPercent: boolean;
}

export function getSmartDealLabel(originalPrice: number, currentPrice: number): DealLabelResult {
  const savings = originalPrice - currentPrice;
  const percent = Math.round((savings / originalPrice) * 100);
  
  // Smart psychological logic for better CTR
  const shouldShowPercent = (
    // Show % when savings >= 20%
    percent >= 20 ||
    // Show % when original price is high (>$40) and decent discount
    (originalPrice > 40 && percent >= 15) ||
    // Show % when it's a nice round number
    (percent % 10 === 0 && percent >= 20)
  );
  
  if (shouldShowPercent) {
    return {
      primary: `${percent}% OFF`,
      secondary: originalPrice > currentPrice ? `Save $${savings.toFixed(2)}` : undefined,
      showPercent: true
    };
  } else {
    // Show money savings for smaller discounts or low-priced items
    return {
      primary: `Save $${savings.toFixed(2)}`,
      secondary: percent > 5 ? `${percent}% off` : undefined,
      showPercent: false
    };
  }
}

export function getPriceDisplay(originalPrice: number, currentPrice: number) {
  const savings = originalPrice - currentPrice;
  
  if (savings <= 0) {
    return {
      current: `$${currentPrice.toFixed(2)}`,
      original: null,
      badge: null
    };
  }
  
  const dealLabel = getSmartDealLabel(originalPrice, currentPrice);
  
  return {
    current: `$${currentPrice.toFixed(2)}`,
    original: `$${originalPrice.toFixed(2)}`,
    badge: dealLabel
  };
}