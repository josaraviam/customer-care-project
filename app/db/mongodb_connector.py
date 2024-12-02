from pymongo import MongoClient
from app.config import MONGO_URI

# Conexión al cliente MongoDB
mongo_client = MongoClient(MONGO_URI)

# Selección de la base de datos
mongo_db = mongo_client["customerCareComments"]

# Definición de colecciones
usuarios_collection = mongo_db["usuarios"]
comentarios_collection = mongo_db["comentarios"]
historial_ediciones_collection = mongo_db["historial_ediciones"]  # Nueva colección
