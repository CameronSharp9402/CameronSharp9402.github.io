""" CRUD_Python_Module.py Reusable MongoDB CRUD class originally developed for CS-340 Project Two. Enhanced for CS-499 to improve structure, documentation, and error handling. """

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Dict, List


class AnimalShelter:
    """ Provides a clean abstraction layer for MongoDB CRUD operations. Separates persistence logic from application logic. """

    def __init__(self, username, password, host, port, database, collection):
            """Initialize and validate MongoDB connection."""
            try:
                self.client = MongoClient(
                    f"mongodb://{username}:{password}@{host}:{port}"
                )
                self.database = self.client[database]
                self.collection = self.database[collection]
            except PyMongoError as e:
                raise ConnectionError(f"MongoDB connection failed: {e}")

    def create(self, data: Dict) -> bool:
        """Insert a single document into the collection."""
        if not data:
            raise ValueError("Insert failed: no data provided")

        try:
            return self.collection.insert_one(data).acknowledged
        except PyMongoError as e:
            print(f"Create operation failed: {e}")
            return False

    def read(self, query: Dict) -> List[Dict]:
        """Retrieve documents matching a query."""
        try:
            return list(self.collection.find(query))
        except PyMongoError as e:
            print(f"Read operation failed: {e}")
            return []

    def update(self, query: Dict, update_data: Dict) -> int:
        """Update documents matching a query."""
        if not update_data:
            raise ValueError("Update failed: no update data provided")

        try:
            result = self.collection.update_many(query, {"$set": update_data})
            return result.modified_count
        except PyMongoError as e:
            print(f"Update operation failed: {e}")
            return 0

    def delete(self, query: Dict) -> int:
        """Delete documents matching a query."""
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as e:
            print(f"Delete operation failed: {e}")
            return 0