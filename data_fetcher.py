import sys

import requests
import json
from datetime import datetime, timedelta
import os
from utils import ensure_dir_exists

API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key
CACHE_DIR = 'stock_data_cache'

def get_cache_file_path(symbol):
    return os.path.join(CACHE_DIR, f"{symbol}_data.json")

def load_cached_data(symbol):
    cache_file = get_cache_file_path(symbol)
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cached_data = json.load(f)
        last_updated = datetime.fromisoformat(cached_data['last_updated'])
        if datetime.now() - last_updated < timedelta(days=1):
            return cached_data['data']
    return None

def save_to_cache(symbol, data):
    ensure_dir_exists(CACHE_DIR)
    cache_file = get_cache_file_path(symbol)
    with open(cache_file, 'w') as f:
        json.dump({'last_updated': datetime.now().isoformat(), 'data': data}, f)

def fetch_stock_symbol(company_name):
    base_url = 'https://www.alphavantage.co/query'
    function = 'SYMBOL_SEARCH'

    params = {
        'function': function,
        'keywords': company_name,
        'apikey': API_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "bestMatches" not in data or len(data["bestMatches"]) == 0:
            raise ValueError(f"No symbol found for company: {company_name}")

        return data["bestMatches"][0]["1. symbol"]
    except requests.RequestException as e:
        print(f"Error fetching symbol: {e}")
        sys.exit(1)
    except (ValueError, KeyError) as e:
        print(f"Error processing symbol search response: {e}")
        sys.exit(1)

def fetch_stock_data(symbol):
    cached_data = load_cached_data(symbol)
    if cached_data:
        return cached_data

    base_url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'

    params = {
        'function': function,
        'symbol': symbol,
        'apikey': API_KEY,
        'outputsize': 'full'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "Error Message" in data:
            raise ValueError(f"API Error: {data['Error Message']}")

        if "Time Series (Daily)" not in data:
            raise KeyError("Unexpected API response format")

        save_to_cache(symbol, data['Time Series (Daily)'])
        return data['Time Series (Daily)']
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)
    except (ValueError, KeyError) as e:
        print(f"Error processing API response: {e}")
        sys.exit(1)