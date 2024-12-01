from fastapi import APIRouter, HTTPException
from typing import List
import json
from app.schemas.caso_schema import Caso, Comentario
from app.db.mysql_connector import mysql_connection

router = APIRouter()


@router.post("/", response_model=Caso)
def create_caso(caso: Caso):
    """
    Crea un nuevo caso en la base de datos.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO casos (fecha_contacto, canal_contacto, pnr, tipo_caso, comentarios_historial)
                    VALUES (%s, %s, %s, %s, %s)
                """
                comentarios_json = json.dumps(
                    [coment.dict() for coment in caso.comentarios_historial]) if caso.comentarios_historial else None
                cursor.execute(query, (
                    caso.fecha_contacto,
                    caso.canal_contacto,
                    caso.pnr,
                    caso.tipo_caso,
                    comentarios_json
                ))
                connection.commit()
                caso.id_caso = cursor.lastrowid  # Recuperar el ID generado
        return caso
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el caso: {e}")


@router.get("/", response_model=List[Caso])
def list_casos():
    """
    Devuelve una lista de todos los casos almacenados.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT id_caso, fecha_contacto, canal_contacto, pnr, tipo_caso, comentarios_historial
                    FROM casos
                """
                cursor.execute(query)
                rows = cursor.fetchall()
        return [
            Caso(
                id_caso=row[0],
                fecha_contacto=row[1].strftime("%Y-%m-%d") if row[1] else None,
                canal_contacto=row[2],
                pnr=row[3],
                tipo_caso=row[4],
                comentarios_historial=json.loads(row[5]) if row[5] else None
            ) for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los casos: {e}")


@router.get("/pnr/{pnr}", response_model=List[Caso])
def get_caso_by_pnr(pnr: str):
    """
    Busca casos por el PNR asociado.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT id_caso, fecha_contacto, canal_contacto, pnr, tipo_caso, comentarios_historial
                    FROM casos
                    WHERE pnr = %s
                """
                cursor.execute(query, (pnr,))
                rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="No se encontraron casos para el PNR proporcionado.")

        return [
            Caso(
                id_caso=row[0],
                fecha_contacto=row[1].strftime("%Y-%m-%d") if row[1] else None,
                canal_contacto=row[2],
                pnr=row[3],
                tipo_caso=row[4],
                comentarios_historial=json.loads(row[5]) if row[5] else None
            ) for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar los casos por PNR: {e}")


@router.put("/{caso_id}", response_model=Caso)
def update_caso(caso_id: int, caso: Caso):
    """
    Actualiza un caso existente.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    UPDATE casos
                    SET fecha_contacto = %s, canal_contacto = %s, pnr = %s, tipo_caso = %s, comentarios_historial = %s
                    WHERE id_caso = %s
                """
                comentarios_json = json.dumps(
                    [coment.dict() for coment in caso.comentarios_historial]) if caso.comentarios_historial else None
                cursor.execute(query, (
                    caso.fecha_contacto,
                    caso.canal_contacto,
                    caso.pnr,
                    caso.tipo_caso,
                    comentarios_json,
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
    Elimina un caso por su ID único.
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
