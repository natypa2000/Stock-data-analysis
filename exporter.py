import os
from utils import ensure_dir_exists

EXPORT_DIR = 'stock_data_exports'

def export_data(df, symbol, format):
    ensure_dir_exists(EXPORT_DIR)
    if format == 'csv':
        filename = os.path.join(EXPORT_DIR, f"{symbol}_data.csv")
        df.to_csv(filename)
    elif format == 'excel':
        filename = os.path.join(EXPORT_DIR, f"{symbol}_data.xlsx")
        df.to_excel(filename)
    print(f"Data exported to {filename}")