import requests
from datetime import datetime, timedelta, timezone
import pytz
from typing import Dict, List, Optional, Any, Union

class PriceFetcher:
    def __init__(self, token_symbol: str = "BTC"):
        """Initialize price fetcher with given token symbol"""
        self.token_symbol = token_symbol
        self.api_key = "762ac19e170c8dcab5c7e48331d0ab2c3dacf24e5ddfb2c6779cc524bbe2746e"
        self.base_url = "https://min-api.cryptocompare.com/data"
        self.utc = pytz.UTC

    def fetch_current_price(self) -> Optional[float]:
        """Fetch current price for the token"""
        url = f"{self.base_url}/price"
        params = {
            "fsym": self.token_symbol,
            "tsyms": "USD",
            "api_key": self.api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"API response for {self.token_symbol}: {data}")
            if "USD" not in data:
                print(f"Price data not found in response: {data}")
                return None
            return data.get("USD")
        except Exception as e:
            print(f"API error for {self.token_symbol} ({type(e).__name__}): {str(e)}")
            return None

    def fetch_hourly_data(self, hours: int = 24) -> Dict[str, List[Any]]:
        """Fetch hourly historical data"""
        url = f"{self.base_url}/v2/histohour"
        params = {
            "fsym": self.token_symbol,
            "tsym": "USD",
            "limit": hours,
            "api_key": self.api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return self._process_historical_data(data)
        except Exception as e:
            print(f"API error fetching hourly data: {e}")
            return {"prices": [], "timestamps": [], "volumes": []}

    def fetch_daily_data(self, days: int = 30) -> Dict[str, List[Any]]:
        """Fetch daily historical data"""
        url = f"{self.base_url}/v2/histoday"
        params = {
            "fsym": self.token_symbol,
            "tsym": "USD",
            "limit": days,
            "api_key": self.api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return self._process_historical_data(data)
        except Exception as e:
            print(f"API error fetching daily data: {e}")
            return {"prices": [], "timestamps": [], "volumes": []}

    def fetch_historical_data(self, time_range):
        """Belirli bir zaman aralığı için geçmiş fiyat verilerini getir"""
        try:
            # Zaman aralığına göre timestamp hesapla
            now = datetime.now()
            if time_range == "1h":
                start_time = now - timedelta(hours=1)
                interval = "1m"  # 1 dakikalık veri
            elif time_range == "24h":
                start_time = now - timedelta(days=1)
                interval = "5m"  # 5 dakikalık veri
            elif time_range == "1m":
                start_time = now - timedelta(days=30)
                interval = "1h"  # 1 saatlik veri
            elif time_range == "3m":
                start_time = now - timedelta(days=90)
                interval = "4h"  # 4 saatlik veri
            elif time_range == "6m":
                start_time = now - timedelta(days=180)
                interval = "6h"  # 6 saatlik veri
            elif time_range == "1y":
                start_time = now - timedelta(days=365)
                interval = "1d"  # Günlük veri
            else:
                start_time = now - timedelta(days=1)
                interval = "5m"

            # Unix timestamp'e çevir
            start_timestamp = int(start_time.timestamp() * 1000)
            end_timestamp = int(now.timestamp() * 1000)

            # API isteği yap
            url = f"https://api.binance.com/api/v3/klines"
            params = {
                "symbol": f"{self.token_symbol}USDT",
                "interval": interval,
                "startTime": start_timestamp,
                "endTime": end_timestamp
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Veriyi düzenle
            timestamps = []
            prices = []
            volumes = []

            for item in data:
                ts = datetime.fromtimestamp(item[0] / 1000, tz=timezone.utc)
                price = float(item[4])  # Closing price
                volume = float(item[5])

                timestamps.append(ts)
                prices.append(price)
                volumes.append(volume)

            return {
                "timestamps": timestamps,
                "prices": prices,
                "volumes": volumes
            }

        except Exception as e:
            print(f"Veri alınırken hata oluştu: {str(e)}")
            return None

    def _process_historical_data(self, response_data: Dict[str, Any]) -> Dict[str, List[Any]]:
        """Process historical data from API response"""
        if not response_data or "Data" not in response_data or "Data" not in response_data["Data"]:
            print(f"Invalid response data format: {response_data}")
            return {"prices": [], "timestamps": [], "volumes": []}

        data = response_data["Data"]["Data"]
        processed_data = {
            "prices": [],
            "timestamps": [],
            "volumes": []
        }

        for entry in data:
            # Convert Unix timestamp to UTC datetime
            dt = datetime.fromtimestamp(entry["time"], tz=self.utc)
            processed_data["timestamps"].append(dt)
            processed_data["prices"].append(entry["close"])
            processed_data["volumes"].append(entry.get("volumeto", 0))

        return processed_data
