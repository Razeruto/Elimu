import os
import pymongo

# Load environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB", "elimu_mongo")  

def get_mongo_connection():
    """Establish connection to MongoDB."""
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        print("✅ Connected to MongoDB successfully")
        return db
    except Exception as e:
        print(f"❌ MongoDB Connection Error: {e}")
        return None

# Test connection when running this file
if __name__ == "__main__":
    db = get_mongo_connection()
    if db is not None:
        print(f"📂 Available collections: {db.list_collection_names()}")
