from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class Comentario(BaseModel):
    id_comentario: str = Field(..., alias="_id")  # Mapear _id de MongoDB a id_comentario
    pnr: str
    fecha_creacion: datetime
    id_usuario: str
    tags: List[str]
    canal_contacto: str
    estado: str
