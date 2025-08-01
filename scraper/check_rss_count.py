#!/usr/bin/env python3
"""
Check how many posts are actually available in the RSS feed
"""

import feedparser

def check_rss_feed():
    print("Checking RSS feed at https://www.savingsguru.ca/feed/")
    
    feed = feedparser.parse("https://www.savingsguru.ca/feed/")
    
    print(f"RSS Feed Status: {feed.status if hasattr(feed, 'status') else 'Unknown'}")
    print(f"Total entries found: {len(feed.entries)}")
    
    if len(feed.entries) > 0:
        print(f"\nFirst few entries:")
        for i, entry in enumerate(feed.entries[:10]):
            print(f"{i+1}. {entry.title}")
            
        print(f"\nLast few entries:")
        for i, entry in enumerate(feed.entries[-3:]):
            print(f"{len(feed.entries)-2+i}. {entry.title}")
    
    return len(feed.entries)

if __name__ == "__main__":
    count = check_rss_feed()
    
    if count < 100:
        print(f"\nThe RSS feed only contains {count} posts, not 100.")
        print("This is normal - RSS feeds typically only show the most recent posts.")
        print("To get more historical posts, you might need to:")
        print("1. Check if the site has pagination in their RSS")
        print("2. Use a different RSS URL with more posts")
        print("3. Scrape the site directly instead of relying on RSS")
    else:
        print(f"\nGood news! The RSS feed has {count} posts available.")