# Stock Market Analysis Tool

This Python-based tool allows users to fetch, analyze, visualize, and export stock market data. It provides functionalities for analyzing individual stocks as well as comparing multiple stocks.

## Features

- Fetch stock data using company names or stock symbols
- Visualize stock prices and trading volumes
- Generate candlestick charts
- Calculate and display moving averages (20-day and 50-day)
- Compare multiple stocks
- Export data to CSV or Excel formats
- Caching mechanism to reduce API calls

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/natypa2000/stock-data-analysis.git
   cd stock-data-analysis
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Obtain an API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

4. Replace `'YOUR_API_KEY'` in the Stock_data.py script with your actual Alpha Vantage API key.

## Usage

### Command Line Interface

1. Analyze a single stock:
   ```
   python Stock_data.py "Apple Inc"
   ```

2. Compare multiple stocks:
   ```
   python Stock_data.py "Apple Inc" "Microsoft Corporation" "Google LLC"
   ```

3. Export data to CSV:
   ```
   python Stock_data.py "Apple Inc" --export csv
   ```

4. Export data to Excel:
   ```
   python Stock_data.py "Apple Inc" --export excel
   ```

### GUI Interface

If you run the script without any arguments, it will prompt you to enter company names:

```
python Stock_data.py
```

Enter company names separated by commas when prompted.

## Output

The tool will generate:

- A line chart showing stock prices and moving averages
- A bar chart showing trading volumes
- A candlestick chart (for single stock analysis)
- A comparison chart (when analyzing multiple stocks)

If export is specified, it will also generate a CSV or Excel file with the stock data.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- This tool uses the [Alpha Vantage API](https://www.alphavantage.co/) for fetching stock market data.
- Thanks to the developers of pandas, matplotlib, and mplfinance for their excellent data manipulation and visualization libraries.
