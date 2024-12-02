from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.config import JWT_SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        id_usuario = payload.get("id_usuario")
        if not id_usuario:
            raise HTTPException(status_code=401, detail="Token inválido.")
        return id_usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido.")


# app/utils/jwt_utils.py

def is_admin(user: str) -> bool:
    """
    Verifica si el usuario tiene permisos de administrador.
    """
    # Supón que el usuario es un string que contiene los roles o similar.
    # Este es solo un ejemplo, puedes ajustarlo según la lógica de tu sistema.
    return "admin" in user

