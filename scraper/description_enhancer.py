#!/usr/bin/env python3
"""
Description enhancer using free/cheap LLM to improve deal descriptions
"""

import json
import requests
import time
import re
from typing import Dict, Any

class DescriptionEnhancer:
    def __init__(self):
        # Using Together AI (offers free tier with good models)
        self.api_url = "https://api.together.xyz/inference"
        self.api_key = None  # You can set this if you want to use Together AI
        
    def enhance_description_local(self, title: str, original_desc: str, price: float = None, discount: int = None) -> str:
        """
        Enhance description using simple template-based approach (no API needed)
        """
        # Clean up the original description
        clean_desc = re.sub(r'<[^>]+>', '', original_desc)  # Remove HTML tags
        clean_desc = re.sub(r'\*\*.*', '', clean_desc)  # Remove generic ending
        clean_desc = clean_desc.replace('sells on Amazon. I think the price is very good.', '')
        clean_desc = clean_desc.strip()
        
        # Extract key product info from title
        title_lower = title.lower()
        
        # Product category detection with more keywords
        categories = {
            'food': ['oreo', 'cakes', 'pretzel', 'crisps', 'snack', 'chocolate', 'candy', 'cookies', 'chips', 'nuts', 'coffee', 'tea', 'protein bar', 'cereal', 'sauce', 'spice'],
            'tech': ['fingerprint', 'smart lock', 'door lock', 'phone', 'charger', 'cable', 'headphones', 'speaker', 'watch', 'tablet', 'computer', 'mouse', 'keyboard', 'monitor', 'camera'],
            'home': ['storage container', 'rack', 'mattress', 'pillow', 'blanket', 'sheet', 'towel', 'curtain', 'lamp', 'chair', 'table', 'shelf', 'organizer', 'basket', 'bin', 'cabinet', 'mirror'],
            'clothing': ['shirt', 'tank top', 'leggings', 'cardigan', 'sweater', 'dress', 'pants', 'jeans', 'jacket', 'coat', 'hoodie', 'tee', 'blouse', 'skirt', 'shorts', 'underwear', 'bra', 'socks'],
            'beauty': ['cream', 'lotion', 'shampoo', 'conditioner', 'makeup', 'lipstick', 'mascara', 'foundation', 'skincare', 'serum', 'moisturizer', 'cleanser'],
            'kitchen': ['pot', 'pan', 'knife', 'cutting board', 'blender', 'mixer', 'cooker', 'kettle', 'toaster', 'microwave', 'dishes', 'plates', 'cups'],
            'sports': ['fitness', 'yoga', 'workout', 'exercise', 'gym', 'weights', 'athletic'],
            'automotive': ['car', 'auto', 'vehicle', 'tire', 'oil', 'brake', 'engine', 'battery', 'filter']
        }
        
        category = 'product'
        # Check categories in priority order (most specific first)
        category_priority = ['tech', 'food', 'beauty', 'kitchen', 'automotive', 'sports', 'home', 'clothing']
        
        for cat in category_priority:
            if any(keyword in title_lower for keyword in categories[cat]):
                category = cat
                break
        
        # Generate enhanced description based on category
        if category == 'clothing':
            enhanced = f"Discover {title} - perfect for your wardrobe with style and comfort in mind. "
            if discount and discount >= 30:
                enhanced += f"Now available with an incredible {discount}% discount, making it an unbeatable value. "
            enhanced += "Quality materials and thoughtful design make this a must-have addition to your collection."
            
        elif category == 'home':
            enhanced = f"Transform your home with {title}. "
            if 'storage' in title_lower or 'container' in title_lower:
                enhanced += "Keep your space organized and clutter-free with this practical solution. "
            elif 'mattress' in title_lower:
                enhanced += "Experience better sleep and comfort with premium materials and design. "
            else:
                enhanced += "Durable construction meets functional design for everyday use. "
            if discount and discount >= 25:
                enhanced += f"Limited time offer with {discount}% savings!"
                
        elif category == 'tech':
            enhanced = f"Upgrade your tech game with {title}. "
            enhanced += "Advanced technology meets user-friendly design for modern living. "
            if discount:
                enhanced += f"Smart shopping opportunity with {discount}% off regular pricing."
                
        elif category == 'food':
            enhanced = f"Treat yourself to {title}. "
            enhanced += "Delicious taste and quality ingredients make this a perfect snack choice. "
            if discount and discount >= 20:
                enhanced += f"Stock up and save with {discount}% off the regular price!"
                
        elif category == 'beauty':
            enhanced = f"Pamper yourself with {title}. "
            enhanced += "Premium beauty essentials for your daily self-care routine. "
            if discount and discount >= 25:
                enhanced += f"Beauty on a budget with {discount}% off!"
                
        elif category == 'kitchen':
            enhanced = f"Elevate your cooking with {title}. "
            enhanced += "Essential kitchen tools designed for home chefs who demand quality. "
            if discount and discount >= 20:
                enhanced += f"Cook smart and save {discount}%!"
                
        elif category == 'sports':
            enhanced = f"Achieve your fitness goals with {title}. "
            enhanced += "Professional-grade equipment for serious athletes and fitness enthusiasts. "
            if discount and discount >= 30:
                enhanced += f"Get fit for less with {discount}% savings!"
                
        elif category == 'automotive':
            enhanced = f"Keep your vehicle running smoothly with {title}. "
            enhanced += "Reliable automotive solutions for maintenance and performance. "
            if discount:
                enhanced += f"Drive smart and save {discount}%!"
                
        else:
            # Generic enhancement
            enhanced = f"Get {title} with confidence. "
            enhanced += "Quality and value come together in this carefully selected product. "
            if discount and discount >= 20:
                enhanced += f"Don't miss out on {discount}% savings!"
        
        return enhanced
    
    def enhance_deals_json(self, input_file='../public/deals.json', output_file=None):
        """
        Enhance all descriptions in deals.json file
        """
        if output_file is None:
            output_file = input_file
            
        # Read current deals
        with open(input_file, 'r') as f:
            deals = json.load(f)
        
        print(f"Enhancing descriptions for {len(deals)} deals...")
        
        for i, deal in enumerate(deals):
            print(f"Processing deal {i+1}: {deal['title'][:50]}...")
            
            # Enhance description
            enhanced_desc = self.enhance_description_local(
                title=deal['title'],
                original_desc=deal.get('description', ''),
                price=deal.get('price', 0),
                discount=deal.get('discountPercent', 0)
            )
            
            deal['description'] = enhanced_desc
            
            # Small delay to be nice
            time.sleep(0.1)
        
        # Write back to file
        with open(output_file, 'w') as f:
            json.dump(deals, f, indent=2)
            
        print(f"Enhanced descriptions written to {output_file}")
        return deals

if __name__ == "__main__":
    enhancer = DescriptionEnhancer()
    enhancer.enhance_deals_json()