from fastapi import APIRouter, HTTPException
from app.models.caso_model import Caso
from app.db.mysql_connector import mysql_connection
from utils.helpers import format_api_response, handle_api_error, validate_date_format

router = APIRouter()

# Crear un caso
@router.post("/")
def create_caso(caso: Caso):
    if not validate_date_format(caso.fecha_contacto, "%Y-%m-%d"):
        raise HTTPException(status_code=400, detail="El formato de la fecha es inválido. Use 'YYYY-MM-DD'.")
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO casos (fecha_contacto, canal_contacto, PNR, tipo_caso, comentarios_agente) 
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (caso.fecha_contacto, caso.canal_contacto, caso.PNR, caso.tipo_caso, caso.comentarios_agente))
                connection.commit()
        return format_api_response("success", "Caso registrado exitosamente.")
    except Exception as e:
        return handle_api_error(e)

# Obtener todos los casos
@router.get("/")
def get_casos():
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM casos")
                casos = cursor.fetchall()
        return format_api_response("success", "Casos obtenidos exitosamente.", casos)
    except Exception as e:
        return handle_api_error(e)

# Obtener un caso por ID
@router.get("/{caso_id}")
def get_caso(caso_id: int):
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM casos WHERE id_caso = %s", (caso_id,))
                caso = cursor.fetchone()
        if not caso:
            raise HTTPException(status_code=404, detail="Caso no encontrado")
        return format_api_response("success", "Caso obtenido exitosamente.", caso)
    except Exception as e:
        return handle_api_error(e)

# Actualizar un caso
@router.put("/{caso_id}")
def update_caso(caso_id: int, caso: Caso):
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                sql = """
                UPDATE casos 
                SET fecha_contacto = %s, canal_contacto = %s, PNR = %s, tipo_caso = %s, comentarios_agente = %s
                WHERE id_caso = %s
                """
                cursor.execute(sql, (caso.fecha_contacto, caso.canal_contacto, caso.PNR, caso.tipo_caso, caso.comentarios_agente, caso_id))
                connection.commit()
        return format_api_response("success", "Caso actualizado exitosamente.")
    except Exception as e:
        return handle_api_error(e)

# Eliminar un caso
@router.delete("/{caso_id}")
def delete_caso(caso_id: int):
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM casos WHERE id_caso = %s", (caso_id,))
                connection.commit()
        return format_api_response("success", "Caso eliminado exitosamente.")
    except Exception as e:
        return handle_api_error(e)
