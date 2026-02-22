import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_BASE = "https://api.notion.com/v1"

def check_tags():
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28"
    }
    
    # Get all tags for 'Tags' property
    response = requests.get(f"{NOTION_API_BASE}/databases/{NOTION_DATABASE_ID}", headers=headers)
    data = response.json()
    
    try:
        options = data["properties"]["Tags"]["multi_select"]["options"]
        print("Available tags in database:")
        for opt in options:
            print(f"- {opt['name']}")
    except KeyError:
        print("Could not retrieve tag options.")

if __name__ == "__main__":
    check_tags()
