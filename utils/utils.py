import pandas as pd
import matplotlib.pyplot as plt

class Utils:
    TOKEN_LIST = [
        {"symbol": "BTC", "name": "Bitcoin"},
        {"symbol": "ETH", "name": "Ethereum"},
        {"symbol": "SOL", "name": "Solana"},
        {"symbol": "XRP", "name": "Ripple"},
        {"symbol": "DOGE", "name": "Dogecoin"},
        {"symbol": "ADA", "name": "Cardano"},
        {"symbol": "AVAX", "name": "Avalanche"},
        {"symbol": "DOT", "name": "Polkadot"},
        {"symbol": "LINK", "name": "Chainlink"},
        {"symbol": "MATIC", "name": "Polygon"},
        {"symbol": "SHIB", "name": "Shiba Inu"},
        {"symbol": "UNI", "name": "Uniswap"},
        {"symbol": "LTC", "name": "Litecoin"},
        {"symbol": "ATOM", "name": "Cosmos"},
        {"symbol": "TRX", "name": "TRON"},
        {"symbol": "BNB", "name": "Binance Coin"},
        {"symbol": "USDT", "name": "Tether"},
        {"symbol": "USDC", "name": "USD Coin"},
        {"symbol": "BUSD", "name": "Binance USD"},
        {"symbol": "AAVE", "name": "Aave"}
    ]

    @staticmethod
    def clean_data(data):
        """Clean and preprocess the data."""
        df = pd.DataFrame(data)
        df.dropna(inplace=True)
        return df

    @staticmethod
    def visualize_data(df):
        """Visualize the data using matplotlib."""
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['value'])
        plt.title("Cryptocurrency Price History")
        plt.xlabel("Time")
        plt.ylabel("Price (USD)")
        plt.grid(True)
        plt.show()
