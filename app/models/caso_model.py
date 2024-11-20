from pydantic import BaseModel
from typing import List, Optional


class Caso(BaseModel):
    id_caso: int
    fecha_contacto: str
    canal_contacto: str
    pnr: str
    tipo_caso: str
    comentarios: str


