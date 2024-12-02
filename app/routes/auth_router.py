from fastapi import APIRouter, HTTPException, Depends
from app.schemas.usuario_schema import UsuarioCreate, UsuarioLogin, Usuario
from app.db.mongodb_connector import usuarios_collection
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_utils import is_admin
from jose import jwt
from datetime import datetime
from app.config import JWT_SECRET_KEY

router = APIRouter()


@router.post("/register", response_model=Usuario)
def register_user(user: UsuarioCreate, is_admin_user: bool = Depends(is_admin)):
    """
    Registra un nuevo usuario. Solo permitido para administradores.
    """
    # Validar que el usuario actual es administrador
    if not is_admin_user:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden crear usuarios.")

    # Verificar que el correo no esté duplicado
    if usuarios_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    # Crear el usuario con los datos requeridos
    hashed_password = hash_password(user.password)
    nuevo_usuario = {
        "nombre": user.nombre,
        "email": user.email,
        "hashed_password": hashed_password,
        "is_admin": False,  # Por defecto no es administrador
        "fecha_creacion": datetime.utcnow(),
    }
    usuarios_collection.insert_one(nuevo_usuario)

    return Usuario(**nuevo_usuario)


@router.post("/login")
def login_user(credentials: UsuarioLogin):
    """
    Inicia sesión y retorna un token JWT si las credenciales son válidas.
    """
    # Buscar al usuario por email
    user = usuarios_collection.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    # Generar el token JWT con is_admin
    token = jwt.encode({
        "id_usuario": str(user["_id"]),
        "is_admin": user.get("is_admin", False)
    }, JWT_SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "token_type": "bearer"}
