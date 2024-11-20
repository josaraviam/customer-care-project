from pydantic import BaseModel
from typing import List

class Comentario(BaseModel):
    id_caso: int
    comentarios: str
    tags: List[str]
