import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAINDROP_TOKEN = os.getenv("RAINDROP_TOKEN")
RAINDROP_API_BASE = "https://api.raindrop.io/rest/v1"

def find_all_collections():
    headers = {"Authorization": f"Bearer {RAINDROP_TOKEN}"}
    # Fetch all (including nested)
    response = requests.get(f"{RAINDROP_API_BASE}/collections", headers=headers)
    response.raise_for_status()
    # Wait, let's try /collections/all if it exists or just inspect children
    # Actually, some APIs use /collections and you have to traverse.
    # But let's see if /collections/all works.
    
    response = requests.get(f"{RAINDROP_API_BASE}/collections", headers=headers)
    data = response.json()
    items = data.get("items", [])
    
    print(f"Total root collections: {len(items)}")
    for item in items:
        print(f"Title: {item['title']}, ID: {item['_id']}")
        
    # Now let's try to search specifically for a collection named "read"
    # Or maybe search for raindrops in all collections? No, I need the ID.
    
    # Try /collections children? 
    # Actually, let's just list everything and check for parentage manually again
    # BUT if they aren't in the root list, they might be in childs property?
    
    # Let's try to search by title
    search_response = requests.get(f"{RAINDROP_API_BASE}/collections", headers=headers)
    # If "read" isn't there, maybe it's under a specific parent.
    
    # Wait, I'll try to get ANY collection with title "read"
    # Raindrop doesn't have a direct search-collection-by-title endpoint easily documented
    # usually you just get the list.
    
    # Let's try to find if "To Read" has any children explicitly.
    to_read_id = 49257025
    # There is no /collections/{id}/children endpoint usually.
    # But wait! I can just search for "read" in the name field? 
    # No, I'll just print EVERYTHING and grep carefully.
    
    print("--- FULL DUMP ---")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    find_all_collections()
