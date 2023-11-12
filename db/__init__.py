# from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# mongodb+srv://<credentials>@cluster0.tjmjpcd.mongodb.net/

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:8000/my")
DATABASE_NAME = "my"

# client = AsyncIOMotorClient(MONGO_URI)
# db = client[DATABASE_NAME]

conn = MongoClient('MONGO_URI')
db = conn['DATABASE_NAME']