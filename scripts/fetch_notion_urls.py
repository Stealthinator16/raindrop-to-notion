import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_BASE = "https://api.notion.com/v1"

def get_all_notion_urls():
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28"
    }
    
    urls = set()
    has_more = True
    next_cursor = None
    
    while has_more:
        payload = {}
        if next_cursor:
            payload["start_cursor"] = next_cursor
            
        response = requests.post(f"{NOTION_API_BASE}/databases/{NOTION_DATABASE_ID}/query", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        for result in data.get("results", []):
            url_prop = result["properties"].get("URL", {}).get("url")
            if url_prop:
                urls.add(url_prop.rstrip("/"))
        
        has_more = data.get("has_more")
        next_cursor = data.get("next_cursor")
        
    return list(urls)

if __name__ == "__main__":
    urls = get_all_notion_urls()
    print(json.dumps(urls))
