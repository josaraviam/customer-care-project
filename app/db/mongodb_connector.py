
from pymongo import MongoClient
from app.config import MONGO_URI

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["customerCareDB"]

usuarios_collection = mongo_db["usuarios"]
comentarios_collection = mongo_db["comentarios"]
