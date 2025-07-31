#!/usr/bin/env python3
"""
Fix images by using Unsplash placeholder images based on product categories
"""

import json
import re

def get_category_from_title(title):
    """Get category from product title"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['shirt', 'tank', 'top', 'cardigan', 'sweater', 'leggings']):
        return 'clothing'
    elif any(word in title_lower for word in ['mattress', 'rack', 'storage', 'container']):
        return 'home'
    elif any(word in title_lower for word in ['lock', 'fingerprint', 'door']):
        return 'technology'  
    elif any(word in title_lower for word in ['oreo', 'cakes', 'pretzel', 'crisps', 'snack']):
        return 'food'
    else:
        return 'product'

def get_placeholder_image(title, category):
    """Get a placeholder image URL based on category"""
    # Use Lorem Picsum for reliable placeholder images
    base_url = "https://picsum.photos/400/400"
    
    # Generate a consistent seed from the title for consistent images
    seed = hash(title) % 1000
    
    category_images = {
        'clothing': f"https://picsum.photos/seed/{seed}/400/400",
        'home': f"https://picsum.photos/seed/{seed + 100}/400/400", 
        'technology': f"https://picsum.photos/seed/{seed + 200}/400/400",
        'food': f"https://picsum.photos/seed/{seed + 300}/400/400",
        'product': f"https://picsum.photos/seed/{seed + 400}/400/400"
    }
    
    return category_images.get(category, category_images['product'])

def fix_images():
    """Replace broken Amazon images with working placeholder images"""
    # Read current deals
    with open('../public/deals.json', 'r') as f:
        deals = json.load(f)
    
    print(f"Fixing images for {len(deals)} deals...")
    
    for deal in deals:
        category = get_category_from_title(deal['title'])
        new_image = get_placeholder_image(deal['title'], category)
        
        print(f"Deal: {deal['title'][:50]}...")
        print(f"  Category: {category}")
        print(f"  New image: {new_image}")
        
        deal['imageUrl'] = new_image
    
    # Write back to file
    with open('../public/deals.json', 'w') as f:
        json.dump(deals, f, indent=2)
    
    print("Done! All images replaced with working placeholder images")

if __name__ == "__main__":
    fix_images()