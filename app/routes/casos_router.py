from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from app.schemas.caso_schema import Caso
from app.db.mysql_connector import mysql_connection
from app.db.mongodb_connector import mongo_db
from app.utils.jwt_utils import is_admin

router = APIRouter()


@router.post("/", response_model=Caso)
def create_caso(caso: Caso, is_admin_user: bool = Depends(is_admin)):
    """
    Crea un nuevo caso en la base de datos MySQL. Solo permitido para administradores.
    """
    if not is_admin_user:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden crear casos.")
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


@router.put("/{caso_id}", response_model=Caso)
def update_caso(caso_id: int, caso: Caso, is_admin_user: bool = Depends(is_admin)):
    """
    Actualiza un caso existente en MySQL. Solo permitido para administradores.
    """
    if not is_admin_user:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden actualizar casos.")
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
def delete_caso(caso_id: int, is_admin_user: bool = Depends(is_admin)):
    """
    Elimina un caso por su ID único en MySQL. Solo permitido para administradores.
    """
    if not is_admin_user:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden eliminar casos.")
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
