from fastapi import APIRouter, HTTPException
from utils.backup import backup_mysql, backup_mongodb

router = APIRouter()


# Ruta para realizar el respaldo de MySQL
@router.post("/mysql")
def backup_mysql_route():
    try:
        backup_mysql()
        return {"message": "Respaldo de MySQL completado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al respaldar MySQL: {e}")


# Ruta para realizar el respaldo de MongoDB
@router.post("/mongodb")
def backup_mongodb_route():
    try:
        backup_mongodb()
        return {"message": "Respaldo de MongoDB completado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al respaldar MongoDB: {e}")
