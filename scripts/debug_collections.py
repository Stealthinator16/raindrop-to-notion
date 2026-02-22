import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAINDROP_TOKEN = os.getenv("RAINDROP_TOKEN")
RAINDROP_API_BASE = "https://api.raindrop.io/rest/v1"

def debug_collections():
    headers = {"Authorization": f"Bearer {RAINDROP_TOKEN}"}
    response = requests.get(f"{RAINDROP_API_BASE}/collections", headers=headers)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    debug_collections()
