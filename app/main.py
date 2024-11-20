from fastapi import FastAPI
from app.db.mysql_connector import get_mysql_connection, initialize_database
from app.routes import casos_router, comentarios_router, backup_router

app = FastAPI(title="Customer Care API")

@app.on_event("startup")
def validate_db_connection():
    """
    Verifica la conexión con la base de datos al iniciar la aplicación.
    """
    try:
        connection = get_mysql_connection()
        print("Conexión exitosa con Amazon RDS.")
        connection.close()
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")


# Inicializar la base de datos
initialize_database()

# Registrar rutas
app.include_router(casos_router.router, prefix="/api/casos", tags=["Casos"])
app.include_router(comentarios_router.router, prefix="/api/comentarios", tags=["Comentarios"])
app.include_router(backup_router.router, prefix="/api/backup", tags=["BackUp"])


@app.get("/")
def root():
    return {"message": "API de Customer Care operativa"}
