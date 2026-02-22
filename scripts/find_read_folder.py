import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAINDROP_TOKEN = os.getenv("RAINDROP_TOKEN")
RAINDROP_API_BASE = "https://api.raindrop.io/rest/v1"

def find_read_collection():
    headers = {"Authorization": f"Bearer {RAINDROP_TOKEN}"}
    # To find nested ones, we can just get all collections and filter by parent
    response = requests.get(f"{RAINDROP_API_BASE}/collections", headers=headers)
    response.raise_for_status()
    items = response.json().get("items", [])
    
    to_read_id = None
    for item in items:
        if item["title"].lower() == "to read":
            to_read_id = item["_id"]
            break
            
    if not to_read_id:
        print("To Read collection not found.")
        return

    print(f"To Read ID: {to_read_id}")
    
    # Check if any item has this parent
    for item in items:
        parent = item.get("parent")
        if parent and isinstance(parent, dict) and parent.get("$id") == to_read_id:
            print(f"Found nested collection: {item['title']}, ID: {item['_id']}")
            if item["title"].lower() == "read":
                print(f"SUCCESS: 'read' collection ID is {item['_id']}")

if __name__ == "__main__":
    find_read_collection()
