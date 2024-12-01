from fastapi import APIRouter, HTTPException
from app.schemas.usuario_schema import UsuarioCreate, UsuarioLogin
from app.db.mongodb_connector import usuarios_collection
from app.utils.hashing import hash_password, verify_password
from app.utils.helpers import generar_id_usuario
from jose import jwt
from app.config import JWT_SECRET_KEY

router = APIRouter()


@router.post("/register")
def register_user(user: UsuarioCreate):
    if usuarios_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    nuevo_id = generar_id_usuario()
    hashed_password = hash_password(user.password)
    usuario = {
        "id_usuario": nuevo_id,
        "email": user.email,
        "hashed_password": hashed_password,
        "nombre": user.nombre,
        "fecha_creacion": datetime.utcnow(),
    }
    usuarios_collection.insert_one(usuario)
    return {"id_usuario": nuevo_id, "detail": "Usuario registrado exitosamente."}


@router.post("/login")
def login_user(credentials: UsuarioLogin):
    user = usuarios_collection.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    token = jwt.encode({"id_usuario": user["id_usuario"]}, JWT_SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
