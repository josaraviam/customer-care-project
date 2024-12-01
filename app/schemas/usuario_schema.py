from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str
