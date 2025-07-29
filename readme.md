# Smithery scraper

## Installation

```bash
pip install -r requirements.txt
```

## Setup .env

### Setup API key
```env
SMITHERY_API_KEY=...

```

### Setup update frequency in hours
```env
SMITHERY_UPDATE_FREQ=72
```
### Setup GoogleConsole Service account key file and bucket settings
```env
STORAGE_SERVICE_ACCOUNT_KEY=key.json
STORAGE_BACKET_NAME=...
STORAGE_BACKET_FOLDER=...
```

## Usage
### Run:
```
python main.py
```

Results will be saved to GoogleCloudStorage and to ``result.json`` file as map