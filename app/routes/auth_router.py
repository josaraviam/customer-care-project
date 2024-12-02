from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.usuario_schema import UsuarioCreate, UsuarioLogin, Usuario
from app.db.mongodb_connector import usuarios_collection
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_utils import create_access_token, create_refresh_token, decode_token, decode_refresh_token, is_admin
from app.utils.helpers import generar_id_usuario
from datetime import datetime

router = APIRouter()


@router.post("/register", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def register_user(user: UsuarioCreate, is_admin_user: bool = Depends(is_admin)):
    """
    Registra un nuevo usuario. Solo permitido para administradores.
    """
    if not is_admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden crear usuarios."
        )

    # Verificar que el correo no esté duplicado
    if usuarios_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado."
        )

    # Generar un ID único para el usuario
    id_usuario = generar_id_usuario()

    # Crear el usuario con los datos requeridos
    hashed_password = hash_password(user.password)
    nuevo_usuario = {
        "id_usuario": id_usuario,
        "nombre": user.nombre,
        "email": user.email,
        "hashed_password": hashed_password,
        "is_admin": False,  # Por defecto no es administrador
        "fecha_creacion": datetime.utcnow(),
    }
    try:
        usuarios_collection.insert_one(nuevo_usuario)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al registrar el usuario: {str(e)}"
        )

    return Usuario(**nuevo_usuario)


@router.post("/register-admin", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def register_admin(user: UsuarioCreate, is_admin_user: bool = Depends(is_admin)):
    """
    Registra un nuevo administrador. Solo permitido para administradores existentes.
    """
    if not is_admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden registrar nuevos administradores."
        )

    # Verificar si ya existe un usuario con el mismo email
    if usuarios_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado."
        )

    # Generar un ID único para el usuario
    id_usuario = generar_id_usuario()

    # Crear el usuario con los datos requeridos
    hashed_password = hash_password(user.password)
    nuevo_usuario = {
        "id_usuario": id_usuario,
        "nombre": user.nombre,
        "email": user.email,
        "hashed_password": hashed_password,
        "is_admin": True,  # Establece al usuario como administrador
        "fecha_creacion": datetime.utcnow(),
    }

    try:
        usuarios_collection.insert_one(nuevo_usuario)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al registrar el administrador: {str(e)}"
        )

    return Usuario(**nuevo_usuario)


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Inicia sesión usando id_usuario o email y retorna access_token y refresh_token.
    """
    username = form_data.username
    password = form_data.password

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los campos username y password son obligatorios."
        )

    # Buscar al usuario por id_usuario o email
    user = usuarios_collection.find_one({"$or": [{"id_usuario": username}, {"email": username}]})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas."
        )

    # Generar los tokens
    try:
        access_token = create_access_token({"id_usuario": user["id_usuario"], "is_admin": user.get("is_admin", False)})
        refresh_token = create_refresh_token({"id_usuario": user["id_usuario"]})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar los tokens de autenticación: {str(e)}"
        )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
def refresh_token(refresh_token: str):
    """
    Renueva el token de acceso utilizando un refresh token válido.
    """
    try:
        payload = decode_refresh_token(refresh_token)
        new_access_token = create_access_token({"id_usuario": payload["id_usuario"]})
        return {"access_token": new_access_token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al renovar el token: {str(e)}"
        )
