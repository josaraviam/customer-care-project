from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.caso_schema import Caso
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
                cursor.execute("""
                    INSERT INTO casos (fecha_contacto, canal_contacto, pnr, tipo_caso, comentarios)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    caso.fecha_contacto,
                    caso.canal_contacto,
                    caso.pnr,
                    caso.tipo_caso,
                    caso.comentarios,
                ))
                connection.commit()
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
                cursor.execute("""
                    SELECT id_caso, fecha_contacto, canal_contacto, pnr, tipo_caso, comentarios 
                    FROM casos
                """)
                rows = cursor.fetchall()

        casos = [
            Caso(
                id_caso=row[0],
                fecha_contacto=row[1].strftime("%Y-%m-%d") if row[1] else None,
                canal_contacto=row[2],
                pnr=row[3],
                tipo_caso=row[4],
                comentarios=row[5],
            )
            for row in rows
        ]
        return casos
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
                cursor.execute("""
                    SELECT id_caso, fecha_contacto, canal_contacto, pnr, tipo_caso, comentarios
                    FROM casos
                    WHERE pnr = %s
                """, (pnr,))
                rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="No se encontraron casos para el PNR proporcionado.")

        casos = [
            Caso(
                id_caso=row[0],
                fecha_contacto=row[1].strftime("%Y-%m-%d") if row[1] else None,
                canal_contacto=row[2],
                pnr=row[3],
                tipo_caso=row[4],
                comentarios=row[5],
            )
            for row in rows
        ]
        return casos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar los casos por PNR: {e}")

@router.get("/{caso_id}", response_model=Caso)
def get_caso(caso_id: int):
    """
    Busca un caso por su ID único.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_caso, fecha_contacto, canal_contacto, pnr, tipo_caso, comentarios
                    FROM casos
                    WHERE id_caso = %s
                """, (caso_id,))
                row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Caso no encontrado.")

        return Caso(
            id_caso=row[0],
            fecha_contacto=row[1].strftime("%Y-%m-%d") if row[1] else None,
            canal_contacto=row[2],
            pnr=row[3],
            tipo_caso=row[4],
            comentarios=row[5],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar el caso: {e}")

@router.put("/{caso_id}", response_model=Caso)
def update_caso(caso_id: int, caso: Caso):
    """
    Actualiza un caso existente.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE casos
                    SET fecha_contacto = %s, canal_contacto = %s, pnr = %s, tipo_caso = %s, comentarios = %s
                    WHERE id_caso = %s
                """, (
                    caso.fecha_contacto,
                    caso.canal_contacto,
                    caso.pnr,
                    caso.tipo_caso,
                    caso.comentarios,
                    caso_id,
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
