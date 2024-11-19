from pydantic import BaseModel
from typing import List

class Comentario(BaseModel):
    id_caso: str
    comentarios: str
    tags: List[str]
