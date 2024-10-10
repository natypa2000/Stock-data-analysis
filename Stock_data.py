import argparse
import sys
from data_fetcher import fetch_stock_symbol, fetch_stock_data
from data_processor import process_data, add_moving_averages
from visualizer import plot_stock_data, plot_candlestick, compare_stocks
from exporter import export_data
from utils import get_company_names

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