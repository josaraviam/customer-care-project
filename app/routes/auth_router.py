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
    if not is_admin_user:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden crear usuarios.")

    # Verificar que el correo no esté duplicado
    if usuarios_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

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

    # Generar el token JWT con el ID de usuario y el rol de administrador
    token = jwt.encode({
        "id_usuario": user["id_usuario"],  # Usar el ID único generado
        "is_admin": user.get("is_admin", False)  # Incluir rol en el token
    }, JWT_SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "token_type": "bearer"}


@router.post("/register-admin", response_model=Usuario)
def register_admin(user: UsuarioCreate):
    """
    Registra el primer usuario administrador. Este endpoint debe ser usado solo una vez.
    """
    try:
        # Verificar si ya existe un administrador en la base de datos
        if usuarios_collection.find_one({"is_admin": True}):
            raise HTTPException(status_code=403, detail="Ya existe un administrador registrado.")

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
        usuarios_collection.insert_one(nuevo_usuario)

        return Usuario(**nuevo_usuario)

    except Exception as e:
        print(f"Error interno: {e}")  # Log detallado
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
