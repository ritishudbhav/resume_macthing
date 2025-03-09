import pymongo
from config import MONGO_URI, DATABASE_NAME

client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

jobs_collection = db["jobs"]
students_collection = db["students"]
