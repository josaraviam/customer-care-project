from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Configuración de MySQL
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")

# Configuración de MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
