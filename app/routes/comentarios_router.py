from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from bson import ObjectId
from app.schemas.comentario_schema import ComentarioCreate, Comentario
from app.db.mongodb_connector import mongo_db
from app.utils.jwt_utils import get_current_user, is_admin

router = APIRouter()


@router.post("/", response_model=Comentario)
def create_comentario(comentario: ComentarioCreate, current_user: str = Depends(get_current_user)):
    """
    Crea un nuevo comentario asociado al usuario autenticado en MongoDB.
    """
    try:
        nuevo_comentario = {
            "pnr": comentario.pnr,
            "fecha_creacion": datetime.utcnow(),
            "fecha_edicion": None,  # Sin edición inicial
            "usuario": current_user,
            "tags": comentario.tags,
            "canal_contacto": comentario.canal_contacto,
            "estado": comentario.estado,
        }

        result = mongo_db["comentarios"].insert_one(nuevo_comentario)
        nuevo_comentario["_id"] = str(result.inserted_id)  # Convertir ObjectId a string
        return nuevo_comentario
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el comentario: {e}")


@router.get("/mis-comentarios", response_model=List[Comentario])
def get_mis_comentarios(current_user: str = Depends(get_current_user)):
    """
    Recupera los comentarios asociados al usuario autenticado desde MongoDB.
    """
    try:
        comentarios = list(mongo_db["comentarios"].find({"usuario": current_user}))
        if not comentarios:
            raise HTTPException(status_code=404, detail="No se encontraron comentarios para este usuario.")

        # Convertir ObjectId a string
        for comentario in comentarios:
            comentario["_id"] = str(comentario["_id"])

        return comentarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recuperar tus comentarios: {e}")


@router.get("/pnr/{pnr}", response_model=List[Comentario])
def get_comentarios_by_pnr(pnr: str):
    """
    Busca todos los comentarios asociados a un PNR en MongoDB.
    """
    try:
        comentarios = list(mongo_db["comentarios"].find({"pnr": pnr}))
        if not comentarios:
            raise HTTPException(status_code=404, detail="No se encontraron comentarios para este PNR.")

        # Convertir ObjectId a string
        for comentario in comentarios:
            comentario["_id"] = str(comentario["_id"])

        return comentarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar comentarios por PNR: {e}")


@router.put("/{comentario_id}", response_model=Comentario)
def update_comentario(comentario_id: str, comentario: ComentarioCreate, current_user: str = Depends(get_current_user)):
    """
    Actualiza un comentario existente en MongoDB.
    """
    try:
        # Verificar si el comentario pertenece al usuario autenticado
        comentario_existente = mongo_db["comentarios"].find_one({"_id": ObjectId(comentario_id), "usuario": current_user})
        if not comentario_existente:
            raise HTTPException(status_code=403, detail="No tienes permiso para editar este comentario.")

        # Actualizar el comentario
        actualizacion = {
            "$set": {
                "tags": comentario.tags,
                "canal_contacto": comentario.canal_contacto,
                "estado": comentario.estado,
                "fecha_edicion": datetime.utcnow(),
            }
        }
        mongo_db["comentarios"].update_one({"_id": ObjectId(comentario_id)}, actualizacion)

        # Retornar el comentario actualizado
        comentario_existente.update(actualizacion["$set"])
        comentario_existente["_id"] = str(comentario_existente["_id"])  # Convertir ObjectId a string
        return comentario_existente
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el comentario: {e}")


@router.delete("/{comentario_id}")
def delete_comentario(comentario_id: str, is_admin_user: bool = Depends(is_admin)):
    """
    Elimina un comentario por su ID único en MongoDB (solo permitido para administradores).
    """
    if not is_admin_user:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar comentarios.")

    try:
        result = mongo_db["comentarios"].delete_one({"_id": ObjectId(comentario_id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Comentario no encontrado.")
        return {"detail": "Comentario eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el comentario: {e}")
