from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class ComentarioModel(BaseModel):
    id_comentario: str = Field(..., alias="_id")
    pnr: str
    fecha_creacion: datetime
    usuario: str
    tags: List[str]
    canal_contacto: str
    estado: str
    texto: str
    fecha_edicion: Optional[datetime]
