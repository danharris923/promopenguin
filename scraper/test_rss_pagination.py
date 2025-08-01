#!/usr/bin/env python3
"""
Test different RSS URLs and pagination to access all 2000 posts
"""

import feedparser
import requests
from urllib.parse import urljoin

def test_rss_urls():
    """Test various RSS feed URLs to find one with more posts"""
    
    base_urls = [
        "https://www.savingsguru.ca/feed/",
        "https://www.savingsguru.ca/feed/?posts_per_page=100",
        "https://www.savingsguru.ca/feed/?posts_per_rss=100", 
        "https://www.savingsguru.ca/feed/?showposts=100",
        "https://www.savingsguru.ca/feed/?paged=1",
        "https://www.savingsguru.ca/?feed=rss2&posts_per_page=100",
        "https://www.savingsguru.ca/?feed=rss2&showposts=100",
        "https://www.savingsguru.ca/wp-json/wp/v2/posts?per_page=100",  # WordPress REST API
    ]
    
    print("Testing different RSS feed URLs...\n")
    
    for url in base_urls:
        try:
            print(f"Testing: {url}")
            
            if 'wp-json' in url:
                # This is REST API, handle differently
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    print(f"  REST API - Found {len(data)} posts")
                    if len(data) > 0:
                        print(f"     First post: {data[0].get('title', {}).get('rendered', 'No title')}")
                else:
                    print(f"  REST API failed: {response.status_code}")
            else:
                # Regular RSS feed
                feed = feedparser.parse(url)
                if hasattr(feed, 'status') and feed.status == 200:
                    print(f"  Found {len(feed.entries)} posts")
                    if len(feed.entries) > 0:
                        print(f"     First post: {feed.entries[0].title}")
                else:
                    print(f"  Failed or no entries")
                    
        except Exception as e:
            print(f"  Error: {e}")
        
        print()

def test_pagination():
    """Test if RSS feed supports pagination"""
    print("Testing RSS pagination...\n")
    
    total_posts = []
    seen_titles = set()
    
    for page in range(1, 6):  # Test first 5 pages
        url = f"https://www.savingsguru.ca/feed/?paged={page}"
        print(f"Testing page {page}: {url}")
        
        try:
            feed = feedparser.parse(url)
            
            if len(feed.entries) == 0:
                print(f"  No posts found on page {page}")
                break
                
            new_posts = 0
            for entry in feed.entries:
                if entry.title not in seen_titles:
                    seen_titles.add(entry.title)
                    total_posts.append(entry.title)
                    new_posts += 1
            
            print(f"  Found {len(feed.entries)} posts ({new_posts} new)")
            
            if new_posts == 0:
                print(f"  No new posts on page {page}, stopping")
                break
                
        except Exception as e:
            print(f"  Error on page {page}: {e}")
            break
    
    print(f"\nTotal unique posts found across all pages: {len(total_posts)}")
    return total_posts

def test_rest_api_pagination():
    """Test WordPress REST API with pagination"""
    print("Testing WordPress REST API pagination...\n")
    
    all_posts = []
    page = 1
    per_page = 100
    
    while len(all_posts) < 500 and page <= 20:  # Safety limit
        url = f"https://www.savingsguru.ca/wp-json/wp/v2/posts?per_page={per_page}&page={page}"
        print(f"Testing REST API page {page}: posts {(page-1)*per_page + 1}-{page*per_page}")
        
        try:
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                posts = response.json()
                if len(posts) == 0:
                    print(f"  No posts on page {page}")
                    break
                
                all_posts.extend(posts)
                print(f"  Found {len(posts)} posts (total: {len(all_posts)})")
                
                # Check if there are more pages
                if len(posts) < per_page:
                    print(f"  Last page reached (got {len(posts)} < {per_page})")
                    break
                    
            elif response.status_code == 400:
                print(f"  Page {page} not found (400) - probably reached the end")
                break
            else:
                print(f"  HTTP {response.status_code}")
                break
                
        except Exception as e:
            print(f"  Error on page {page}: {e}")
            break
            
        page += 1
    
    print(f"\nTotal posts found via REST API: {len(all_posts)}")
    
    if len(all_posts) > 0:
        print(f"Sample titles:")
        for i, post in enumerate(all_posts[:5]):
            print(f"  {i+1}. {post['title']['rendered']}")
    
    return all_posts

if __name__ == "__main__":
    print("Investigating SavingsGuru RSS feeds to find all 2000 posts...\n")
    
    # Test different RSS URLs
    test_rss_urls()
    
    print("="*60)
    
    # Test RSS pagination
    rss_posts = test_pagination()
    
    print("="*60)
    
    # Test REST API pagination  
    api_posts = test_rest_api_pagination()
    
    print("="*60)
    print("SUMMARY:")
    print(f"RSS pagination found: {len(rss_posts)} posts")
    print(f"REST API found: {len(api_posts)} posts")
    
    if len(api_posts) > len(rss_posts):
        print("REST API seems to be the best option for getting more posts!")
    elif len(rss_posts) > 10:
        print("RSS pagination works!")
    else:
        print("Still limited posts found. May need different approach.")