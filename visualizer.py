import sys
import matplotlib.pyplot as plt
import mplfinance as mpf
from data_fetcher import fetch_stock_data
from data_processor import process_data

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