from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str
