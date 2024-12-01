from pydantic import BaseModel, EmailStr


class Usuario(BaseModel):
    email: EmailStr
    hashed_password: str
    nombre: str
