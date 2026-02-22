import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAINDROP_TOKEN = os.getenv("RAINDROP_TOKEN")
RAINDROP_API_BASE = "https://api.raindrop.io/rest/v1"

def list_collections():
    headers = {"Authorization": f"Bearer {RAINDROP_TOKEN}"}
    response = requests.get(f"{RAINDROP_API_BASE}/collections", headers=headers)
    response.raise_for_status()
    collections = response.json().get("items", [])
    
    print(f"Found {len(collections)} collections.")
    for col in collections:
        parent_info = f" (Parent: {col['parent']['$id']})" if "parent" in col and col["parent"] else ""
        print(f"Title: {col['title']}, ID: {col['_id']}{parent_info}")

if __name__ == "__main__":
    if not RAINDROP_TOKEN:
        print("Error: Missing RAINDROP_TOKEN in .env file.")
    else:
        list_collections()
