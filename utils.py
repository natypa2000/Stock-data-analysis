import os
import tkinter as tk
from tkinter import simpledialog

def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_company_names():
    root = tk.Tk()
    root.withdraw()
    company_names = simpledialog.askstring("Input", "Enter company names separated by commas:")
    if company_names:
        return [name.strip() for name in company_names.split(',')]
    return None