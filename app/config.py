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


# Variables de configuración de MongoDB
MONGO_URI = os.getenv("MONGO_URI")

# JWT
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# Validaciones
missing_env_vars = []

if not MYSQL_USER:
    missing_env_vars.append("MYSQL_USER")
if not MYSQL_PASSWORD:
    missing_env_vars.append("MYSQL_PASSWORD")
if not MYSQL_HOST:
    missing_env_vars.append("MYSQL_HOST")
if not MYSQL_DB:
    missing_env_vars.append("MYSQL_DB")
if not MONGO_URI:
    missing_env_vars.append("MONGO_URI")
if not JWT_SECRET_KEY:
    missing_env_vars.append("JWT_SECRET_KEY")

# Si falta alguna variable, se lanza una excepción
if missing_env_vars:
    raise ValueError(f"Faltan las siguientes configuraciones en el entorno: {', '.join(missing_env_vars)}. Verifica tu archivo .env.")
