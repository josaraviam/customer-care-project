from pydantic import BaseModel, EmailStr
from datetime import datetime

class Usuario(BaseModel):
    id_usuario: str
    email: EmailStr
    nombre: str
    is_admin: bool  # Agregar campo para identificar si el usuario es administrador
    fecha_creacion: datetime

    class Config:
        orm_mode = True  # Permite convertir automáticamente desde objetos ORM o similares
