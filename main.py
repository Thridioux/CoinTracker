from price_fetcher import PriceFetcher
from db import DatabaseManager
from utils.utils import Utils
from gui.main_gui import CoinTrackerApp
import tkinter as tk

def main():
    db_manager = DatabaseManager()

    # Initialize the GUI
    root = tk.Tk()
    app = CoinTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
