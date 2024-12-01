from pydantic import BaseModel, EmailStr
from datetime import datetime

class Usuario(BaseModel):
    id_usuario: str
    email: EmailStr
    hashed_password: str
    nombre: str
    fecha_creacion: datetime
