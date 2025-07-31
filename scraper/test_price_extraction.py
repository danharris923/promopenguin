#!/usr/bin/env python3
"""
Test price extraction from RSS descriptions
"""

import re

def extract_price_info(description):
    """Extract price information from description"""
    # Try multiple price patterns
    price_patterns = [
        r'\$([\\d,]+(?:\\.\\d{2})?)',  # $12.99 or $1,299.99
        r'CDN\$ ([\\d,]+(?:\\.\\d{2})?)',  # CDN$ 12.99
        r'Price: \$([\\d,]+(?:\\.\\d{2})?)',  # Price: $12.99
        r'Now: \$([\\d,]+(?:\\.\\d{2})?)',  # Now: $12.99
    ]
    
    prices = []
    for pattern in price_patterns:
        matches = re.findall(pattern, description)
        prices.extend(matches)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_prices = []
    for price in prices:
        if price not in seen:
            seen.add(price)
            unique_prices.append(float(price.replace(',', '')))
    
    if len(unique_prices) >= 2:
        current_price = unique_prices[0]
        original_price = unique_prices[1]
    elif len(unique_prices) == 1:
        current_price = unique_prices[0]
        # Estimate original price with 30% markup
        original_price = current_price * 1.3
    else:
        # Try to find percentage discount
        discount_match = re.search(r'(\d+)%\s*[Oo]ff', description)
        if discount_match:
            discount = int(discount_match.group(1))
            # If we have any price and a discount percentage
            if len(unique_prices) == 1:
                current_price = unique_prices[0]
                original_price = current_price / (1 - discount/100)
            else:
                # Default prices if nothing found
                current_price = 29.99
                original_price = 39.99
        else:
            current_price = 29.99
            original_price = 39.99
    
    if original_price > 0:
        discount = int(((original_price - current_price) / original_price) * 100)
    else:
        discount = 0
        
    return current_price, original_price, discount

# Test with sample descriptions
test_descriptions = [
    "SereneLife Hanging Lounge Swing Chair sells on Amazon. I think the price is very good.",
    "Product is now $12.99, was $19.99!",
    "Great deal at CDN$ 45.99 (regularly CDN$ 89.99)",
    "Save 40% off the regular price!",
    "Price: $29.99 - You save: $10.00 (25%)"
]

print("Testing price extraction:")
for desc in test_descriptions:
    current, original, discount = extract_price_info(desc)
    print(f"\nDescription: {desc[:50]}...")
    print(f"Current: ${current:.2f}, Original: ${original:.2f}, Discount: {discount}%")