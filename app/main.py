from fastapi import FastAPI
from app.routes import casos_router, comentarios_router
from app.db.mysql_connector import initialize_database
from app.routes import backup_router

# Crear una instancia de la aplicación FastAPI
app = FastAPI(title="Customer Care Project API")

# Inicializar la estructura de la base de datos al iniciar el servidor
initialize_database()


# Registrar las rutas de casos y comentarios
app.include_router(casos_router.router, prefix="/api/casos", tags=["Casos"])
app.include_router(comentarios_router.router, prefix="/api/comentarios", tags=["Comentarios"])
app.include_router(backup_router.router, prefix="/api/backup", tags=["Backup"])



# Definir un endpoint de inicio para verificar que la aplicación funciona
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Customer Care"}


