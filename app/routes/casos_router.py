from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.schemas.caso_schema import Caso
from app.db.mysql_connector import mysql_connection
from app.db.mongodb_connector import mongo_db

router = APIRouter()


@router.post("/", response_model=Caso)
def create_caso(caso: Caso):
    """
    Crea un nuevo caso en la base de datos MySQL.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                # Insertar el nuevo caso
                query = """
                    INSERT INTO casos (fecha_contacto, canal_contacto, pnr, tipo_caso)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (
                    caso.fecha_contacto,
                    caso.canal_contacto,
                    caso.pnr,
                    caso.tipo_caso,
                ))
                connection.commit()
                caso.id_caso = cursor.lastrowid  # Obtener el ID generado automáticamente
        return caso
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el caso: {e}")


@router.get("/", response_model=List[Dict])
def list_casos():
    """
    Devuelve una lista de todos los casos almacenados en MySQL, incluyendo sus comentarios.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT id_caso, fecha_contacto, canal_contacto, pnr, tipo_caso
                    FROM casos
                """
                cursor.execute(query)
                rows = cursor.fetchall()

        # Recuperar los comentarios asociados a cada PNR
        casos = []
        for row in rows:
            pnr = row[3]
            comentarios = list(mongo_db["comentarios"].find({"pnr": pnr}, {"_id": 0}))  # Recuperar comentarios por PNR
            casos.append({
                "id_caso": row[0],
                "fecha_contacto": row[1].strftime("%Y-%m-%d") if row[1] else None,
                "canal_contacto": row[2],
                "pnr": row[3],
                "tipo_caso": row[4],
                "comentarios": comentarios
            })

        return casos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los casos: {e}")


@router.get("/pnr/{pnr}", response_model=Dict)
def get_caso_by_pnr(pnr: str):
    """
    Busca un caso por el PNR en MySQL e incluye sus comentarios desde MongoDB.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT id_caso, fecha_contacto, canal_contacto, pnr, tipo_caso
                    FROM casos
                    WHERE pnr = %s
                """
                cursor.execute(query, (pnr,))
                row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="No se encontró un caso con el PNR proporcionado.")

        # Recuperar comentarios asociados al PNR
        comentarios = list(mongo_db["comentarios"].find({"pnr": pnr}, {"_id": 0}))

        return {
            "id_caso": row[0],
            "fecha_contacto": row[1].strftime("%Y-%m-%d") if row[1] else None,
            "canal_contacto": row[2],
            "pnr": row[3],
            "tipo_caso": row[4],
            "comentarios": comentarios
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar el caso por PNR: {e}")


@router.put("/{caso_id}", response_model=Caso)
def update_caso(caso_id: int, caso: Caso):
    """
    Actualiza un caso existente en MySQL.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    UPDATE casos
                    SET fecha_contacto = %s, canal_contacto = %s, pnr = %s, tipo_caso = %s
                    WHERE id_caso = %s
                """
                cursor.execute(query, (
                    caso.fecha_contacto,
                    caso.canal_contacto,
                    caso.pnr,
                    caso.tipo_caso,
                    caso_id
                ))
                connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Caso no encontrado.")
        return caso
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el caso: {e}")


@router.delete("/{caso_id}")
def delete_caso(caso_id: int):
    """
    Elimina un caso por su ID único en MySQL.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM casos WHERE id_caso = %s", (caso_id,))
                connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Caso no encontrado.")
        return {"detail": "Caso eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el caso: {e}")
