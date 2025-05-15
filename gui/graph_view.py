import matplotlib.pyplot as plt
from price_fetcher import PriceFetcher
from db import DatabaseManager

def show_price_graph(token_id):
    fetcher = PriceFetcher()
    data = fetcher.fetch_historical_prices(token_id)

    if not data or "prices" not in data:
        print("Veri alınırken hata oluştu: 'prices'")
        return

    prices = data["prices"]
    timestamps = [p[0] for p in prices]
    values = [p[1] for p in prices]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, values)
    plt.title(f"{token_id} Fiyat Grafiği")
    plt.xlabel("Zaman")
    plt.ylabel("Fiyat")
    plt.show()
