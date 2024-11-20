from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Configuración de MySQL
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)  # Valor por defecto: 3306
MYSQL_DB = os.getenv("MYSQL_DB")

# Variables de configuración
MONGO_URI = os.getenv("MONGO_URI")