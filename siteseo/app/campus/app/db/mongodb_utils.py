from motor.motor_asyncio import AsyncIOMotorClient
# from pymongo import MongoClient


# # MongoDB attributes
# mongodb_uri = 'mongodb://127.0.0.1:27017/campus'
# client = MongoClient(mongodb_uri)
# db = client[campus]

class DataBase:
    client: AsyncIOMotorClient = None

async def get_database() -> AsyncIOMotorClient:
    return await DataBase.client

# def connect_to_mongo(uri):
#     DataBase.client = AsyncIOMotorClient(uri)
#     print("Connected to MongoDB")

# def close_mongo_connection():
#     DataBase.client.close()
#     print("Closed connection with MongoDB")

def get_db():
    client = AsyncIOMotorClient("mongodb://127.0.0.1:27017/campus")
    db = client.campus
    return db