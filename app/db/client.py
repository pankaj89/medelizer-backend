from datetime import datetime
from pymongo import MongoClient

# Connect to MongoDB (default localhost:27017)
client = MongoClient("mongodb://localhost:27017/")
db = client["medical"]
records_table = db["records"]
users_table = db["users"]


def mongo_to_dict(doc):
    """
    Convert a MongoDB document to a dictionary.
    This function handles the conversion of ObjectId to string and datetime fields to ISO format.
    """
    if "_id" in doc.keys():
        doc["id"] = str(doc["_id"])
        del doc["_id"]

    # Convert all datetime fields to ISO format
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()

    return doc
