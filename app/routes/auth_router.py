from fastapi import APIRouter, HTTPException
from app.db.mongodb_connector import usuarios_collection
from app.utils.hashing import hash_password, verify_password
from app.schemas.usuario_schema import UsuarioCreate
from jose import jwt
from app.config import JWT_SECRET_KEY

router = APIRouter()


@router.post("/register")
def register_user(usuario: UsuarioCreate):
    if usuarios_collection.find_one({"email": usuario.email}):
        raise HTTPException(status_code=400, detail="El usuario ya existe.")

    hashed_password = hash_password(usuario.password)
    usuarios_collection.insert_one({
        "email": usuario.email,
        "hashed_password": hashed_password,
        "nombre": usuario.nombre
    })
    return {"detail": "Usuario registrado exitosamente."}


@router.post("/login")
def login(email: str, password: str):
    user = usuarios_collection.find_one({"email": email})
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    token = jwt.encode({"sub": email}, JWT_SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
