from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime
from bson import ObjectId
from app.schemas.comentario_schema import (ComentarioResponseSchema as Comentario,
                                           ComentarioCreateSchema as ComentarioCreate)
from app.db.mongodb_connector import mongo_db
from app.utils.jwt_utils import get_current_user, is_admin
from app.utils.helpers import validar_object_id, procesar_comentarios, convertir_objectid

router = APIRouter()


@router.post("/", response_model=Comentario, status_code=status.HTTP_201_CREATED)
def create_comentario(comentario: ComentarioCreate, current_user: str = Depends(get_current_user)):
    """
    Crea un nuevo comentario asociado al usuario autenticado en MongoDB.
    """
    nuevo_comentario = {
        "pnr": comentario.pnr,
        "fecha_creacion": datetime.utcnow(),
        "fecha_edicion": None,
        "usuario": current_user,
        "tags": comentario.tags,
        "canal_contacto": comentario.canal_contacto,
        "estado": comentario.estado,
        "texto": comentario.texto,
    }

    try:
        result = mongo_db["comentarios"].insert_one(nuevo_comentario)
        nuevo_comentario["_id"] = result.inserted_id
        return convertir_objectid(nuevo_comentario)  # Convertir antes de devolver
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al crear el comentario: {str(e)}"
        )


@router.get("/mis-comentarios", response_model=List[Comentario], status_code=status.HTTP_200_OK)
def get_mis_comentarios(current_user: str = Depends(get_current_user)):
    """
    Recupera los comentarios asociados al usuario autenticado desde MongoDB.
    """
    try:
        comentarios = list(mongo_db["comentarios"].find({"usuario": current_user}))
        if not comentarios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron comentarios para este usuario."
            )
        return convertir_objectid(comentarios)  # Convertir antes de devolver
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al recuperar los comentarios: {str(e)}"
        )


@router.get("/pnr/{pnr}", response_model=List[Comentario], status_code=status.HTTP_200_OK)
def get_comentarios_by_pnr(pnr: str):
    """
    Busca todos los comentarios asociados a un PNR en MongoDB.
    """
    try:
        comentarios = list(mongo_db["comentarios"].find({"pnr": pnr}))
        if not comentarios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron comentarios para este PNR."
            )
        return convertir_objectid(comentarios)  # Convertir antes de devolver
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al buscar comentarios por PNR: {str(e)}"
        )


@router.put("/{comentario_id}", response_model=Comentario, status_code=status.HTTP_200_OK)
def update_comentario(comentario_id: str, comentario: ComentarioCreate, current_user: str = Depends(get_current_user)):
    """
    Actualiza un comentario existente en MongoDB y registra el historial de ediciones.
    """
    comentario_id = validar_object_id(comentario_id)

    try:
        comentario_existente = mongo_db["comentarios"].find_one({"_id": comentario_id, "usuario": current_user})
        if not comentario_existente:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para editar este comentario."
            )

        actualizacion = {
            "$set": {
                "tags": comentario.tags,
                "canal_contacto": comentario.canal_contacto,
                "estado": comentario.estado,
                "texto": comentario.texto,
                "fecha_edicion": datetime.utcnow().isoformat(),
            }
        }
        mongo_db["comentarios"].update_one({"_id": comentario_id}, actualizacion)

        mongo_db["historial_ediciones"].insert_one({
            "comentario_id": str(comentario_id),
            "usuario": current_user,
            "cambios": actualizacion["$set"],
            "fecha_edicion": datetime.utcnow().isoformat(),
        })

        comentario_existente.update(actualizacion["$set"])
        comentario_existente["_id"] = comentario_id
        return convertir_objectid(comentario_existente)  # Convertir antes de devolver
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al actualizar el comentario: {str(e)}"
        )


@router.delete("/{comentario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comentario(comentario_id: str, is_admin_user: bool = Depends(is_admin)):
    """
    Elimina un comentario por su ID único en MongoDB. Solo permitido para administradores.
    """
    comentario_id = validar_object_id(comentario_id)

    try:
        result = mongo_db["comentarios"].delete_one({"_id": comentario_id})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comentario no encontrado."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al eliminar el comentario: {str(e)}"
        )


@router.get("/all", response_model=List[Comentario], status_code=status.HTTP_200_OK)
def get_all_comentarios():
    """
    Recupera todos los comentarios de la base de datos.
    Esta ruta no requiere autenticación y es útil para pruebas.
    """
    try:
        comentarios = list(mongo_db["comentarios"].find())
        if not comentarios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron comentarios en la base de datos."
            )
        return convertir_objectid(comentarios)  # Convertir antes de devolver
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al recuperar todos los comentarios: {str(e)}"
        )
