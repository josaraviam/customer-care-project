from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UsuarioCreate(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico único del usuario.")
    password: str = Field(..., min_length=8, description="Contraseña del usuario.")
    nombre: str = Field(..., description="Nombre completo del usuario.")


class UsuarioLogin(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario.")
    password: str = Field(..., description="Contraseña del usuario.")


class Usuario(BaseModel):
    nombre: str
    email: EmailStr
    fecha_creacion: datetime
