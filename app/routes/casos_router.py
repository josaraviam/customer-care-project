from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict
from app.schemas.caso_schema import CasoSchema as Caso
from app.db.mysql_connector import mysql_connection
from app.db.mongodb_connector import mongo_db
from app.utils.jwt_utils import is_admin

router = APIRouter()


@router.post("/", response_model=Caso, status_code=status.HTTP_201_CREATED)
def create_caso(caso: Caso):
    """
    Crea un nuevo caso en la base de datos MySQL. Disponible para todos los usuarios.
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al crear el caso: {str(e)}"
        )


@router.put("/{caso_id}", response_model=Caso, status_code=status.HTTP_200_OK)
def update_caso(caso_id: int, caso: Caso):
    """
    Actualiza un caso existente en MySQL. Disponible para todos los usuarios.
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Caso no encontrado para la actualización."
            )

        return caso
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al actualizar el caso: {str(e)}"
        )


@router.delete("/{caso_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_caso(caso_id: int, is_admin_user: bool = Depends(is_admin)):
    """
    Elimina un caso por su ID único en MySQL. Solo permitido para administradores.
    """
    if not is_admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar casos."
        )
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM casos WHERE id_caso = %s", (caso_id,))
                connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Caso no encontrado para eliminar."
            )

        return {"detail": "Caso eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al eliminar el caso: {str(e)}"
        )
