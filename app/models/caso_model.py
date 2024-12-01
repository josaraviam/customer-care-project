from pydantic import BaseModel
from typing import List, Dict, Optional


class Comentario(BaseModel):
    texto: str
    fecha: str
    usuario: str


class Caso(BaseModel):
    id_caso: int
    fecha_contacto: str
    canal_contacto: str
    pnr: str
    tipo_caso: str
    comentarios_historial: Optional[List[Comentario]] = None
