from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.config import JWT_SECRET_KEY
from typing import List
from bson import ObjectId  # Asegúrate de importar ObjectId
from fastapi import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Obtiene el usuario actual a partir del token JWT.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        id_usuario = payload.get("id_usuario")
        if not id_usuario:
            raise HTTPException(status_code=401, detail="Token inválido.")
        return id_usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido.")


def generate_token(user: dict) -> str:
    """
    Genera un token JWT para un usuario.
    """
    payload = {
        "id_usuario": str(user["_id"]),
        "is_admin": user.get("is_admin", False),  # Agrega el rol al token
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token


def is_admin(token: str = Depends(oauth2_scheme)) -> bool:
    """
    Verifica si el usuario autenticado tiene permisos de administrador.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        is_admin = payload.get("is_admin")
        if not is_admin:
            raise HTTPException(status_code=403, detail="No tienes permisos de administrador.")
        return True
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado.")
