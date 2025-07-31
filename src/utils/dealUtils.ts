export interface DealLabelResult {
  primary: string;
  secondary?: string;
  showPercent: boolean;
}

export function getSmartDealLabel(originalPrice: number, currentPrice: number, realDiscountPercent?: number): DealLabelResult {
  // Use real Amazon discount percentage if available, otherwise calculate from prices
  const percent = realDiscountPercent && realDiscountPercent > 0 ? realDiscountPercent : Math.round(((originalPrice - currentPrice) / originalPrice) * 100);
  
  // Only show red percentage tags for deals over 20% off
  if (percent >= 20) {
    return {
      primary: `${percent}% OFF`,
      secondary: undefined, // Remove savings calculations
      showPercent: true
    };
  } else {
    // Don't show any badge for deals under 20% off
    return {
      primary: "",
      secondary: undefined,
      showPercent: false
    };
  }
}

export function getPriceDisplay(originalPrice: number, currentPrice: number, realDiscountPercent?: number) {
  const savings = originalPrice - currentPrice;
  
  if (savings <= 0) {
    return {
      current: `$${currentPrice.toFixed(2)}`,
      original: null,
      badge: null
    };
  }
  
  const dealLabel = getSmartDealLabel(originalPrice, currentPrice, realDiscountPercent);
  
  return {
    current: `$${currentPrice.toFixed(2)}`,
    original: `$${originalPrice.toFixed(2)}`,
    badge: dealLabel
  };
}