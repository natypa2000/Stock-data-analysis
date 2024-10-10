import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import argparse
import sys
import mplfinance as mpf
import os
import json
import tkinter as tk
from tkinter import simpledialog


API_KEY = 'YOUR_API_KEY'
CACHE_DIR = 'stock_data_cache'
EXPORT_DIR = 'stock_data_exports'


def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


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


def process_data(raw_data):
    try:
        df = pd.DataFrame(raw_data).T
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        df = df.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })
        df = df.sort_index()
        return df
    except (ValueError, TypeError) as e:
        print(f"Error processing data: {e}")
        sys.exit(1)


def add_moving_averages(df):
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    return df


def plot_stock_data(df, symbol):
    try:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        ax1.plot(df.index, df['Close'], label='Close Price')
        ax1.plot(df.index, df['MA20'], label='20-day MA')
        ax1.plot(df.index, df['MA50'], label='50-day MA')
        ax1.set_title(f'{symbol} Stock Price and Moving Averages')
        ax1.set_ylabel('Price (USD)')
        ax1.legend()
        ax1.grid(True)

        ax2.bar(df.index, df['Volume'])
        ax2.set_title(f'{symbol} Trading Volume')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Volume')
        ax2.grid(True)

        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error plotting data: {e}")
        sys.exit(1)


def plot_candlestick(df, symbol):
    try:
        mpf.plot(df, type='candle', style='yahoo', title=f'{symbol} Candlestick Chart',
                 ylabel='Price (USD)', volume=True, figsize=(12, 8))
    except Exception as e:
        print(f"Error plotting candlestick chart: {e}")
        sys.exit(1)


def compare_stocks(symbols):
    try:
        plt.figure(figsize=(12, 6))
        for symbol in symbols:
            raw_data = fetch_stock_data(symbol)
            df = process_data(raw_data)
            df['Normalized'] = df['Close'] / df['Close'].iloc[0]
            plt.plot(df.index, df['Normalized'], label=symbol)

        plt.title('Stock Price Comparison (Normalized)')
        plt.xlabel('Date')
        plt.ylabel('Normalized Price')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error comparing stocks: {e}")
        sys.exit(1)


def export_data(df, symbol, format):
    ensure_dir_exists(EXPORT_DIR)
    if format == 'csv':
        filename = os.path.join(EXPORT_DIR, f"{symbol}_data.csv")
        df.to_csv(filename)
    elif format == 'excel':
        filename = os.path.join(EXPORT_DIR, f"{symbol}_data.xlsx")
        df.to_excel(filename)
    print(f"Data exported to {filename}")


def get_company_names():
    root = tk.Tk()
    root.withdraw()
    company_names = simpledialog.askstring("Input", "Enter company names separated by commas:")
    if company_names:
        return [name.strip() for name in company_names.split(',')]
    return None


def main(company_names=None, export_format=None):
    if company_names is None or len(company_names) == 0:
        company_names = get_company_names()
        if not company_names:
            print("No company names provided. Exiting.")
            sys.exit(1)

    symbols = [fetch_stock_symbol(name) for name in company_names]


    if len(symbols) == 1:
        symbol = symbols[0]
        raw_data = fetch_stock_data(symbol)
        df = process_data(raw_data)
        df = add_moving_averages(df)
        plot_stock_data(df, symbol)
        plot_candlestick(df, symbol)

        if export_format:
            export_data(df, symbol, export_format)
    else:
        compare_stocks(symbols)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Fetch and visualize stock data")
    parser.add_argument("companies", nargs='*',
                        help="Company names (e.g., 'Apple Inc' 'Google LLC' 'Microsoft Corporation')")
    parser.add_argument("--export", choices=['csv', 'excel'], help="Export data to CSV or Excel")
    args = parser.parse_args()

    main(args.companies, args.export)