import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
RAINDROP_TOKEN = os.getenv("RAINDROP_TOKEN")
RAINDROP_COLLECTION_ID = 49257121  # "Read" folder ID

RAINDROP_API_BASE = "https://api.raindrop.io/rest/v1"
NOTION_API_BASE = "https://api.notion.com/v1"

# --- Raindrop Helpers ---

def get_raindrop_bookmarks(collection_id):
    headers = {"Authorization": f"Bearer {RAINDROP_TOKEN}"}
    items = []
    page = 0
    while True:
        params = {"perpage": 50, "page": page}
        response = requests.get(f"{RAINDROP_API_BASE}/raindrops/{collection_id}", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        current_items = data.get("items", [])
        if not current_items:
            break
        items.extend(current_items)
        if len(current_items) < 50:
            break
        page += 1
    return items

def get_collection_id(name="to read"):
    headers = {"Authorization": f"Bearer {RAINDROP_TOKEN}"}
    response = requests.get(f"{RAINDROP_API_BASE}/collections", headers=headers)
    response.raise_for_status()
    for col in response.json().get("items", []):
        if col["title"].lower() == name.lower():
            return col["_id"]
    return None

# --- Notion Helpers ---

def create_notion_page(data):
    """
    Creates a page in the Notion database.
    'data' should contain: title, url, tags, notes, rating, summary
    """
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"  # Kept as stable, but noted 2025-09-03 changes
    }
    
    # Note: If using the latest 2025-09-03 version, Notion now distinguishes 
    # between containers (databases) and data sources. For standard database
    # usage, 'database_id' still works in the 'parent' field for most cases.
    
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": data["title"]}}]
            },
            "URL": {
                "url": data["url"]
            },
            "State": {
                "status": {"name": "AI-Read"}
            },
            "Type": {
                "select": {"name": data.get("type", "Article")}
            },
            "Tags": {
                "multi_select": [{"name": tag} for tag in data["tags"]]
            },
            "Notes": {
                "rich_text": [{"text": {"content": data["notes"]}}]
            },
            "Rating": {
                "select": {"name": str(data["rating"])}
            }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Why should I bother reading this article?"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": data["summary"]}}]
                }
            }
        ]
    }

    if data.get("highlights"):
        payload["children"].append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Highlights"}}]
            }
        })
        for highlight in data["highlights"]:
            text = highlight.get("text", "")
            if text:
                payload["children"].append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": text}}]
                    }
                })
    
    response = requests.post(f"{NOTION_API_BASE}/pages", headers=headers, json=payload)
    if not response.ok:
        print(f"Failed to create Notion page: {response.text}")
    else:
        print(f"Successfully created Notion page for: {data['title']}")

# --- Analysis Placeholder ---
# In a real scenario, this would involve sending the content to an LLM.
# Since I am the agent, I will use my analysis capability during the loop.

def analyze_content(title, url, content):
    """
    This is where the actual intelligence happens.
    I'll prompt myself to provide the notes, rating, and summary.
    """
    # This function will be called during the main loop when I run the script.
    # For now, it returns a structure that the main loop will fill.
    return {
        "notes": "", # Key takeaways
        "rating": 0, # LessWrong rating
        "summary": "" # Why read this?
    }

def main():
    if not all([NOTION_TOKEN, NOTION_DATABASE_ID, RAINDROP_TOKEN]):
        print("Error: Missing environment variables. Please check your .env file.")
        return

    bookmarks = get_raindrop_bookmarks(RAINDROP_COLLECTION_ID)
    
    # Output JSON for the agent to process
    output = []
    for item in bookmarks:
        output.append({
            "title": item["title"],
            "url": item["link"],
            "tags": ["read"],
            "highlights": [h["text"] for h in item.get("highlights", []) if "text" in h]
        })
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
