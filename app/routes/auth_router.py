from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.usuario_schema import UsuarioCreate, UsuarioLogin, Usuario
from app.db.mongodb_connector import usuarios_collection
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_utils import is_admin
from app.utils.helpers import generar_id_usuario
from jose import jwt
from datetime import datetime
from app.config import JWT_SECRET_KEY

router = APIRouter()

@router.post("/register", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def register_user(user: UsuarioCreate, is_admin_user: bool = Depends(is_admin)):
    """
    Registra un nuevo usuario. Solo permitido para administradores.
    """
    if not is_admin_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo los administradores pueden crear usuarios.")

    if not user.email or not user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Los campos email y password son obligatorios.")

    # Verificar que el correo no esté duplicado
    if usuarios_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está registrado.")

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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno al registrar el usuario.") from e

    return Usuario(**nuevo_usuario)


@router.post("/register-admin", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def register_admin(user: UsuarioCreate):
    """
    Registra el primer usuario administrador. Este endpoint debe ser usado solo una vez.
    """
    if not user.email or not user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Los campos email y password son obligatorios.")

    # Verificar si ya existe un administrador en la base de datos
    if usuarios_collection.find_one({"is_admin": True}):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ya existe un administrador registrado.")

    # Generar un ID único para el usuario
    id_usuario = generar_id_usuario()

    # Crear el usuario con los datos requeridos
    hashed_password = hash_password(user.password)
    nuevo_usuario = {
        "id_usuario": id_usuario,
        "nombre": user.nombre,
        "email": user.email,
        "hashed_password": hashed_password,
        "is_admin": True,  # El primer usuario es administrador
        "fecha_creacion": datetime.utcnow(),
    }

    try:
        usuarios_collection.insert_one(nuevo_usuario)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno al registrar el administrador.") from e

    return Usuario(**nuevo_usuario)


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Inicia sesión usando id_usuario o email y retorna un token JWT si las credenciales son válidas.
    """
    username = form_data.username
    password = form_data.password

    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Los campos username y password son obligatorios.")

    # Buscar al usuario por id_usuario o email
    user = usuarios_collection.find_one({"$or": [{"id_usuario": username}, {"email": username}]})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas.")

    # Generar el token JWT con el ID de usuario y el rol de administrador
    try:
        token = jwt.encode({
            "id_usuario": user["id_usuario"],
            "is_admin": user.get("is_admin", False)
        }, JWT_SECRET_KEY, algorithm="HS256")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al generar el token de autenticación.") from e

    return {"access_token": token, "token_type": "bearer"}
