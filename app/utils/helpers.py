from datetime import datetime
from typing import List, Union
from bson import ObjectId
from fastapi import HTTPException
from app.db.mongodb_connector import usuarios_collection


def validate_date_format(date_input: Union[datetime, str], date_format: str) -> bool:
    """
    Valida si la entrada es una fecha válida en un formato específico.
    Puede recibir un objeto `datetime` o una cadena.
    """
    if isinstance(date_input, datetime):
        # Si ya es un objeto datetime, validamos su formato convirtiéndolo a string
        date_input = date_input.strftime(date_format)
    try:
        datetime.strptime(date_input, date_format)
        return True
    except ValueError:
        return False


def format_api_response(data, message="Operación exitosa") -> dict:
    """
    Formatea la respuesta estándar para las APIs.
    """
    return {"data": data, "message": message}


def handle_api_error(error: Exception) -> dict:
    """
    Maneja errores y devuelve un formato estándar para respuestas de error.
    """
    return {"error": str(error)}


def generar_id_usuario() -> str:
    """
    Genera un ID único para los usuarios en formato 'JXXXX'.
    """
    last_user = usuarios_collection.find_one(sort=[("id_usuario", -1)])
    if not last_user:
        return "J0001"
    last_id = int(last_user["id_usuario"][1:])
    return f"J{last_id + 1:04d}"


def validar_object_id(id_: str) -> ObjectId:
    """
    Valida y convierte un ID en formato string a ObjectId.
    """
    try:
        return ObjectId(id_)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido.")


def procesar_comentarios(comentarios: List[dict]) -> List[dict]:
    """
    Convierte '_id' a 'id_comentario' y las fechas a formato ISO en una lista de comentarios.
    """
    for comentario in comentarios:
        comentario["id_comentario"] = str(comentario.pop("_id"))
        comentario["fecha_creacion"] = comentario["fecha_creacion"].isoformat() if comentario.get(
            "fecha_creacion") else None
        comentario["fecha_edicion"] = comentario["fecha_edicion"].isoformat() if comentario.get(
            "fecha_edicion") else None
    return comentarios


def convertir_objectid(documento: Union[dict, List[dict]]) -> Union[dict, List[dict]]:
    """
    Convierte los ObjectId a string y las fechas a formato ISO en un documento o lista de documentos.
    """
    if isinstance(documento, list):  # Si es una lista, procesa cada documento
        return [convertir_objectid(doc) for doc in documento]
    if isinstance(documento, dict):
        if "_id" in documento:  # Convertir el ObjectId
            documento["id_comentario"] = str(documento["_id"])
            del documento["_id"]
        for clave, valor in documento.items():  # Convertir fechas
            if isinstance(valor, datetime):
                documento[clave] = valor.isoformat()
    return documento
