import os
import requests
import json
import random
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_BASE = "https://api.notion.com/v1"

def verify_sync():
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28"
    }
    
    # 1. Count items with tag "read"
    print("Verifying item count...")
    count = 0
    has_more = True
    next_cursor = None
    page_ids = []
    
    while has_more:
        payload = {
            "filter": {
                "property": "Tags",
                "multi_select": {
                    "contains": "read"
                }
            }
        }
        if next_cursor:
            payload["start_cursor"] = next_cursor
            
        response = requests.post(f"{NOTION_API_BASE}/databases/{NOTION_DATABASE_ID}/query", headers=headers, json=payload)
        data = response.json()
        results = data.get("results", [])
        count += len(results)
        page_ids.extend([p["id"] for p in results])
        
        has_more = data.get("has_more")
        next_cursor = data.get("next_cursor")
        
    print(f"Total items tagged 'read': {count}")
    
    # 2. Check highlights in random sample
    print("\nVerifying highlights in 3 random pages...")
    sample_ids = random.sample(page_ids, min(len(page_ids), 3))
    
    for page_id in sample_ids:
        # Get page title
        page_resp = requests.get(f"{NOTION_API_BASE}/pages/{page_id}", headers=headers).json()
        title_prop = page_resp["properties"].get("Name", {}).get("title", [])
        title = title_prop[0]["text"]["content"] if title_prop else "Untitled"
        print(f"\nChecking: {title}")
        
        # Get blocks
        blocks_resp = requests.get(f"{NOTION_API_BASE}/blocks/{page_id}/children", headers=headers).json()
        
        found_highlights_header = False
        highlight_count = 0
        
        for block in blocks_resp.get("results", []):
            if block["type"] == "heading_2":
                text = block["heading_2"]["rich_text"][0]["text"]["content"]
                if "Highlights" in text:
                    found_highlights_header = True
            elif block["type"] == "bulleted_list_item" and found_highlights_header:
                highlight_count += 1
                
        if found_highlights_header:
            print(f"  [PASS] Found 'Highlights' section with {highlight_count} bullets.")
        else:
            print(f"  [INFO] No 'Highlights' section found (item might not have highlights).")

if __name__ == "__main__":
    verify_sync()
