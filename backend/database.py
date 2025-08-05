
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
load_dotenv(override=True)
import os

uri = os.getenv("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(uri)


db = client["chat_database"]

