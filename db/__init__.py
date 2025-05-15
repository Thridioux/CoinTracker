from pymongo import MongoClient
from datetime import datetime

class DatabaseManager:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="cointracker"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["prices"]

    def store_data(self, data):
        self.collection.insert_many(data)

    def get_data(self):
        return list(self.collection.find())

    def insert_price(self, token_id, price):
        document = {
            "token_id": token_id,
            "price": price,
            "timestamp": datetime.utcnow()
        }
        self.collection.insert_one(document)

    def get_price_history(self, token_id):
        return list(self.collection.find({"token_id": token_id}).sort("timestamp"))