#!/usr/bin/env python3
"""
Fix all affiliate tags in deals.json to use the correct savingsgurucc-20 tag
"""

import json
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def fix_affiliate_tag(url, correct_tag="savingsgurucc-20"):
    """Fix the affiliate tag in an Amazon URL"""
    parsed = urlparse(url)
    
    # If it's not an Amazon URL, return as-is
    if 'amazon' not in parsed.netloc.lower():
        return url
    
    # Parse query parameters
    params = parse_qs(parsed.query)
    
    # Update the tag parameter
    params['tag'] = [correct_tag]
    
    # Rebuild URL with correct tag
    new_query = urlencode(params, doseq=True)
    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    return new_url

def main():
    # Load existing deals.json
    with open('../public/deals.json', 'r') as f:
        deals = json.load(f)
    
    print(f"Fixing affiliate tags for {len(deals)} deals...")
    
    updated_count = 0
    
    # Update each deal's affiliate URL
    for deal in deals:
        old_url = deal['affiliateUrl']
        new_url = fix_affiliate_tag(old_url)
        
        if old_url != new_url:
            deal['affiliateUrl'] = new_url
            updated_count += 1
            print(f"Updated {deal['title'][:30]}...")
    
    # Save updated deals.json
    with open('../public/deals.json', 'w') as f:
        json.dump(deals, f, indent=2)
    
    print(f"\nSuccessfully updated {updated_count} affiliate links to use savingsgurucc-20!")

if __name__ == "__main__":
    main()