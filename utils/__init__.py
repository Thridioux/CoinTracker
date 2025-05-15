from price_fetcher import PriceFetcher
from db import DatabaseManager
from gui.graph_view import show_price_graph
from utils.utils import Utils

def main():
    fetcher = PriceFetcher()
    db = DatabaseManager()

    for token in Utils.TOKEN_LIST:
        price = fetcher.fetch_price(token)
        if price is not None:
            db.insert_price(token, price)
            print(f"{token.capitalize()} fiyatı kaydedildi: ${price}")
        else:
            print(f"{token.capitalize()} fiyatı alınamadı.")

    for token in Utils.TOKEN_LIST:
        show_price_graph(token)

if __name__ == "__main__":
    main()
