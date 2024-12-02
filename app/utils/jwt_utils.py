from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.config import JWT_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Obtiene el usuario actual a partir del token JWT.
    """
    try:
        payload = decode_token(token)
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
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token


def is_admin(token: str = Depends(oauth2_scheme)) -> bool:
    """
    Verifica si el usuario autenticado tiene permisos de administrador.
    """
    try:
        payload = decode_token(token)
        is_admin = payload.get("is_admin")
        if not is_admin:
            raise HTTPException(status_code=403, detail="No tienes permisos de administrador.")
        return True
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado.")


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Genera un token de acceso JWT con un tiempo de expiración.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Genera un token de actualización JWT con un tiempo de expiración más largo.
    """
    if expires_delta is None:
        expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decodifica un token JWT y verifica su validez.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Token inválido o expirado.") from e


def renew_access_token(refresh_token: str) -> str:
    """
    Renueva el token de acceso utilizando un refresh token válido.
    """
    payload = decode_token(refresh_token)
    id_usuario = payload.get("id_usuario")
    if not id_usuario:
        raise HTTPException(status_code=401, detail="Refresh token inválido.")
    # Generar un nuevo token de acceso
    new_access_token = create_access_token(data={"id_usuario": id_usuario})
    return new_access_token


def decode_refresh_token(refresh_token: str) -> dict:
    """
    Decodifica un refresh token JWT y verifica su validez.
    """
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Refresh token inválido o expirado."
        ) from e
