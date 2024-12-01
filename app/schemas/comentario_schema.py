from pydantic import BaseModel
from typing import List


class ComentarioCreate(BaseModel):
    pnr: str
    tags: List[str]
    canal_contacto: str
    estado: str
    texto: str


class Comentario(ComentarioCreate):
    _id: str
    fecha_creacion: str
    usuario: str
