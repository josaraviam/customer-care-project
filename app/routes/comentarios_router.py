from fastapi import APIRouter, HTTPException
from app.models.comentario_model import Comentario
from app.db.mongodb_connector import mongo_db
from bson.objectid import ObjectId
from utils.helpers import format_api_response, handle_api_error

router = APIRouter()

# Crear un comentario
@router.post("/")
def create_comentario(comentario: Comentario):
    try:
        result = mongo_db["comentarios"].insert_one(comentario.dict())
        return format_api_response("success", "Comentario registrado exitosamente.", {"id": str(result.inserted_id)})
    except Exception as e:
        return handle_api_error(e)

# Obtener todos los comentarios
@router.get("/")
def get_comentarios():
    try:
        comentarios = list(mongo_db["comentarios"].find())
        for comentario in comentarios:
            comentario["_id"] = str(comentario["_id"])
        return format_api_response("success", "Comentarios obtenidos exitosamente.", comentarios)
    except Exception as e:
        return handle_api_error(e)

# Obtener un comentario por ID
@router.get("/{comentario_id}")
def get_comentario(comentario_id: str):
    try:
        comentario = mongo_db["comentarios"].find_one({"_id": ObjectId(comentario_id)})
        if not comentario:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        comentario["_id"] = str(comentario["_id"])
        return format_api_response("success", "Comentario obtenido exitosamente.", comentario)
    except Exception as e:
        return handle_api_error(e)

# Actualizar un comentario
@router.put("/{comentario_id}")
def update_comentario(comentario_id: str, comentario: Comentario):
    try:
        result = mongo_db["comentarios"].update_one(
            {"_id": ObjectId(comentario_id)}, {"$set": comentario.dict()}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        return format_api_response("success", "Comentario actualizado exitosamente.")
    except Exception as e:
        return handle_api_error(e)

# Eliminar un comentario
@router.delete("/{comentario_id}")
def delete_comentario(comentario_id: str):
    try:
        result = mongo_db["comentarios"].delete_one({"_id": ObjectId(comentario_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        return format_api_response("success", "Comentario eliminado exitosamente.")
    except Exception as e:
        return handle_api_error(e)
