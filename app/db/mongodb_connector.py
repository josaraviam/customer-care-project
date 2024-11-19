from pymongo import MongoClient
from app.config import MONGO_URI

# Crear una conexión a MongoDB Atlas
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["customerCareComments"]
