import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAINDROP_TOKEN = os.getenv("RAINDROP_TOKEN")
RAINDROP_API_BASE = "https://api.raindrop.io/rest/v1"

def list_all_titles():
    headers = {"Authorization": f"Bearer {RAINDROP_TOKEN}"}
    response = requests.get(f"{RAINDROP_API_BASE}/collections", headers=headers)
    response.raise_for_status()
    items = response.json().get("items", [])
    
    print(f"Found {len(items)} collections:")
    for item in items:
        parent_id = item.get("parent", {}).get("$id") if item.get("parent") else "None"
        print(f"- {item['title']} (ID: {item['_id']}, Parent: {parent_id})")

if __name__ == "__main__":
    list_all_titles()
