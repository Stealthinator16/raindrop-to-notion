import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_BASE = "https://api.notion.com/v1"

def count_items_by_tag(tag):
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28"
    }
    
    count = 0
    has_more = True
    next_cursor = None
    
    while has_more:
        payload = {
            "filter": {
                "property": "Tags",
                "multi_select": {
                    "contains": tag
                }
            }
        }
        if next_cursor:
            payload["start_cursor"] = next_cursor
            
        response = requests.post(f"{NOTION_API_BASE}/databases/{NOTION_DATABASE_ID}/query", headers=headers, json=payload)
        data = response.json()
        results = data.get("results", [])
        count += len(results)
        
        has_more = data.get("has_more")
        next_cursor = data.get("next_cursor")
    
    return count

if __name__ == "__main__":
    mf_count = count_items_by_tag("Mental Fitness")
    f_count = count_items_by_tag("Fitness")
    
    print(f"Items tagged 'Mental Fitness': {mf_count}")
    print(f"Items tagged 'Fitness': {f_count}")
