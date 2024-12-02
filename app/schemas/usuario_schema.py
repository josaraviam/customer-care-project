from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class Usuario(BaseModel):
    id_usuario: str
    nombre: str
    email: EmailStr
    is_admin: bool
    fecha_creacion: datetime
