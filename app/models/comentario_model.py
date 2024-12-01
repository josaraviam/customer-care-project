from pydantic import BaseModel
from datetime import datetime
from typing import List


class Comentario(BaseModel):
    id_comentario: str
    pnr: str
    fecha_creacion: datetime
    id_usuario: str
    tags: List[str]
    canal_contacto: str
    estado: str
