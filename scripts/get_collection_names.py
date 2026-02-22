import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAINDROP_TOKEN = os.getenv("RAINDROP_TOKEN")
IDS = [49294001, 48193755]

def get_collection_name(coll_id):
    headers = {"Authorization": f"Bearer {RAINDROP_TOKEN}"}
    resp = requests.get(f"https://api.raindrop.io/rest/v1/collection/{coll_id}", headers=headers)
    if resp.ok:
        return resp.json()["item"]["title"]
    else:
        return f"Unknown_{coll_id}"

for i in IDS:
    print(f"ID {i}: {get_collection_name(i)}")
