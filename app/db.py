import certifi
from motor.motor_asyncio import AsyncIOMotorClient

from app import Config

MONGODB_URI = f"mongodb+srv://{Config().DATABASE_USERNAME}:{Config().DATABASE_PASSWORD}@{Config().DATABASE_PATH}/?retryWrites=true&w=majority"

print("MONGODB_URI", MONGODB_URI)

client = AsyncIOMotorClient(MONGODB_URI, tls=True, tlsCAFile=certifi.where())

db = client["blog-db"]


def get_collection(name):
    return db[name]


# def insert_document(collection_name, document):
#     collection = get_collection(collection_name)
#     result = collection.insert_one(document)
#     return result.inserted_id


# def find_documents(collection_name, query={}, limit=0):
#     collection = get_collection(collection_name)
#     documents = collection.find(query).limit(limit)
#     return list(documents)


# def update_document(collection_name, query, update_data):
#     collection = get_collection(collection_name)
#     result = collection.update_one(query, {"$set": update_data})
#     return result.modified_count


# def delete_document(collection_name, query):
#     collection = get_collection(collection_name)
#     result = collection.delete_one(query)
#     return result.deleted_count


# def count_documents(collection_name, query={}):
#     collection = get_collection(collection_name)
#     count = collection.count_documents(query)
#     return count


# def find_one_document(collection_name, query={}):
#     collection = get_collection(collection_name)
#     document = collection.find_one(query)
#     return document


# def create_index(collection_name, field_name, unique=False):
#     collection = get_collection(collection_name)
#     index_name = collection.create_index([(field_name, 1)], unique=unique)
#     return index_name


# def drop_collection(collection_name):
#     collection = get_collection(collection_name)
#     collection.drop()
