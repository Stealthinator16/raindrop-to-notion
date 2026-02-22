# Raindrop to Notion

Sync bookmarks from Raindrop.io collections to a Notion database. Fetches bookmarks by collection, deduplicates against existing Notion entries, and creates rich Notion pages with metadata, ratings, summaries, and highlights.

## Features

- **Bookmark fetching** -- Pull bookmarks from specific Raindrop.io collections (Read, Fitness, Mental Fitness, etc.)
- **Deduplication** -- Fetch existing Notion URLs to avoid creating duplicate entries
- **Collection mapping** -- Map Raindrop collections to Notion tags (e.g., Fitness, Mental Fitness)
- **Rich page creation** -- Each synced bookmark gets a Notion page with title, URL, type, rating, notes, summary, and highlights
- **Verification scripts** -- Validate sync results by checking tag counts and page contents

## Prerequisites

- Python 3
- A [Notion integration](https://www.notion.so/my-integrations) token with access to your target database
- A [Raindrop.io](https://developer.raindrop.io/) API test token
- `requests` and `python-dotenv` packages

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/<your-username>/raindrop-to-notion.git
   cd raindrop-to-notion
   ```

2. Install dependencies:
   ```
   pip install requests python-dotenv
   ```

3. Copy the example environment file and fill in your tokens:
   ```
   cp .env.example scripts/.env
   ```

4. Edit `scripts/.env` with your actual Notion integration token, Notion database ID, and Raindrop API token.

## Usage

All scripts live in the `scripts/` directory and should be run from there (they load `.env` via `python-dotenv`).

### Core sync

- **`raindrop_to_notion.py`** -- Main sync script. Fetches bookmarks from the "Read" collection in Raindrop and outputs them as JSON for processing into Notion pages.
- **`sync_fitness.py`** -- Syncs Fitness collection bookmarks to Notion with pre-analyzed ratings, notes, and summaries.
- **`sync_mental_fitness.py`** -- Syncs Mental Fitness collection bookmarks to Notion with pre-analyzed metadata.

### Collection discovery

- **`list_collections.py`** -- List all Raindrop collections with IDs and parent info.
- **`find_read_folder.py`** -- Locate the "Read" collection nested under "To Read".
- **`find_all_collections.py`** -- Dump all collection data for debugging.
- **`get_collection_names.py`** -- Resolve collection IDs to names.

### Fetching and inspection

- **`fetch_fitness.py`** -- Fetch and format bookmarks from the Fitness collection.
- **`fetch_mental_fitness.py`** -- Fetch and format bookmarks from the Mental Fitness collection.
- **`fetch_notion_urls.py`** -- Retrieve all existing URLs from the Notion database (used for deduplication).
- **`list_all_titles.py`** -- List all collection titles with parent relationships.
- **`check_tags.py`** -- Show available tag options in the Notion database.
- **`debug_collections.py`** -- Raw JSON dump of Raindrop collections.

### Verification

- **`verify_sync.py`** -- Count synced items by tag and spot-check highlights in random pages.
- **`verify_final_counts.py`** -- Count items by "toread" and "read" tags.
- **`verify_new_collections.py`** -- Count items by "Fitness" and "Mental Fitness" tags.
