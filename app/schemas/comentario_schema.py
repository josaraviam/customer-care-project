from pydantic import BaseModel, Field
from typing import List

class Comentario(BaseModel):
    id_caso: int = Field(..., description="ID del caso al que está asociado el comentario")
    comentarios: str = Field(..., description="Texto del comentario")
    tags: List[str] = Field(..., description="Lista de etiquetas asociadas al comentario")

    class Config:
        json_schema_extra = {
            "example": {
                "id_caso": 123,
                "comentarios": "El cliente solicita más información sobre el caso.",
                "tags": ["urgente", "consulta"]
            }
        }
