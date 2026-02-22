import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAINDROP_TOKEN = os.getenv("RAINDROP_TOKEN")
COLLECTION_ID = 48193755

def get_raindrop_bookmarks():
    headers = {"Authorization": f"Bearer {RAINDROP_TOKEN}"}
    all_bookmarks = []
    page = 0
    
    while True:
        url = f"https://api.raindrop.io/rest/v1/raindrops/{COLLECTION_ID}?perpage=50&page={page}"
        response = requests.get(url, headers=headers)
        if not response.ok:
            print(f"Error fetching page {page}: {response.text}")
            break
            
        data = response.json()
        items = data.get("items", [])
        if not items:
            break
            
        all_bookmarks.extend(items)
        page += 1
        
    return all_bookmarks

def format_bookmark(item):
    return {
        "title": item["title"],
        "url": item["link"],
        "highlights": [h["text"] for h in item.get("highlights", [])]
    }

if __name__ == "__main__":
    bookmarks = get_raindrop_bookmarks()
    formatted = [format_bookmark(b) for b in bookmarks]
    print(json.dumps(formatted, indent=2))
