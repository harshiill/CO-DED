from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "HackByte"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
