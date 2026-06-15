from datetime import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING
from app.config import settings


class InMemoryTransactionRepository:
    def __init__(self):
        self.transactions: list[dict] = []

    def save(self, transaction: dict) -> None:
        self.transactions.append(transaction)

    def find_by_customer(self, customer_id: str) -> list[dict]:
        return [t for t in self.transactions if t.get("customer_id") == customer_id]

    def find_all(self) -> list[dict]:
        return self.transactions


class MongoTransactionRepository:
    def __init__(self):
        self.client = MongoClient(settings.mongodb_uri)
        self.collection = self.client[settings.mongodb_db]["transactions"]
        self.collection.create_index([("transaction_id", ASCENDING)], unique=True)
        self.collection.create_index([("customer_id", ASCENDING), ("transaction_time", DESCENDING)])
        self.collection.create_index([("risk_score", DESCENDING)])

    def save(self, transaction: dict) -> None:
        self.collection.update_one(
            {"transaction_id": transaction["transaction_id"]},
            {"$set": transaction},
            upsert=True,
        )

    def find_by_customer(self, customer_id: str) -> list[dict]:
        return list(self.collection.find({"customer_id": customer_id}, {"_id": 0}))

    def find_all(self) -> list[dict]:
        return list(self.collection.find({}, {"_id": 0}))


def get_repository():
    if settings.use_in_memory_db:
        return InMemoryTransactionRepository()
    return MongoTransactionRepository()
