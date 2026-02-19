# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password, host='localhost', port=27017, db='aac', col='animals'): 
        USER = username
        PASS = password
        HOST = host
        PORT = port
        DB = db
        COL = col

        try:
            self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}') 
            self.database = self.client[DB] 
            self.collection = self.database[COL] 
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def create(self, data):
        if data is not None and isinstance(data, dict):
            try:
                result = self.collection.insert_one(data)
                print(f"Document inserted with _id: {result.inserted_id}")
                return True
            except Exception as e:
                print(f"Error inserting document: {e}")
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty or not a dictionary")

    def read(self, query):
        if query is not None and isinstance(query, dict):
            try:
                cursor = self.collection.find(query)
                results = list(cursor)
                print(f"Found {len(results)} document(s) matching the query.")
                return results
            except Exception as e:
                print(f"Error reading documents: {e}")
                return []
        else:
            raise Exception("Query parameter must be a non-empty dictionary")        

    def update(self, query, new_values):
        """
        Update documents in the collection that match the query.
        """
        if query is None or not isinstance(query, dict):
            raise Exception("Query parameter must be a non-empty dictionary")
        if new_values is None or not isinstance(new_values, dict):
            raise Exception("New values must be a non-empty dictionary")

        try:
            result = self.collection.update_many(query, {"$set": new_values})
            print(f"Modified {result.modified_count} document(s)")
            return result.modified_count
        except Exception as e:
            print(f"Error updating documents: {e}")
            return 0

    def delete(self, query):
        """
        Delete documents in the collection that match the query.
        """
        if query is None or not isinstance(query, dict):
            raise Exception("Query parameter must be a non-empty dictionary")

        try:
            result = self.collection.delete_many(query)
            print(f"Deleted {result.deleted_count} document(s)")
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return 0