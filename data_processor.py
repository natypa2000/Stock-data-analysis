import sys
import pandas as pd

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