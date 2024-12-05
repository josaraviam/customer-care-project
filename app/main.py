from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Asegúrate de importar desde fastapi.middleware.cors
from app.db.mysql_connector import get_mysql_connection, initialize_database
from app.db.mongodb_connector import mongo_db
from app.routes import casos_router, comentarios_router, backup_router
from app.routes.auth_router import router as auth_router

# Crear la instancia de FastAPI
app = FastAPI(title="Customer Care API")

# Configuración del middleware de CORS
app.add_middleware(
    CORSMiddleware,  # Usa directamente la clase CORSMiddleware aquí
    allow_origins=["https://witty-pond-032d33e0f.4.azurestaticapps.net/index.html"],  # Permitir solicitudes desde el front-end
    allow_credentials=True,  # Permitir envío de credenciales (como cookies o tokens)
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


@app.on_event("startup")
def validate_db_connections():
    """
    Verifica las conexiones con MySQL y MongoDB al iniciar la aplicación.
    """
    # Validación de conexión con MySQL
    try:
        connection = get_mysql_connection()
        print("Conexión exitosa con Amazon RDS.")
        connection.close()
    except Exception as e:
        print(f"Error al conectar a MySQL: {e}")

    # Validación de conexión con MongoDB
    try:
        # Intentar listar colecciones para verificar la conexión
        mongo_db.list_collection_names()
        print("Conexión exitosa con MongoDB Atlas.")
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")


# Inicializar la base de datos de MySQL
initialize_database()

# Registrar rutas
app.include_router(casos_router.router, prefix="/api/casos", tags=["Casos"])
app.include_router(comentarios_router.router, prefix="/api/comentarios", tags=["Comentarios"])
app.include_router(backup_router.router, prefix="/api/backup", tags=["BackUp"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


@app.get("/")
def root():
    """
    Ruta raíz para verificar el estado del API.
    """
    return {"message": "API de Customer Care operativa"}
