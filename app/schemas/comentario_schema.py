from pydantic import BaseModel, Field
from typing import List, Optional


class ComentarioCreate(BaseModel):
    pnr: str = Field(..., min_length=6, max_length=6, description="PNR asociado al comentario.")
    tags: List[str] = Field(..., description="Etiquetas asociadas al comentario.")
    canal_contacto: str = Field(..., description="Canal de contacto donde se originó el comentario.")
    estado: str = Field(..., description="Estado actual del comentario.")
    texto: str = Field(..., description="Texto del comentario.")


class Comentario(ComentarioCreate):
    _id: str = Field(..., description="ID único del comentario en MongoDB.")
    fecha_creacion: str = Field(..., description="Fecha y hora de creación del comentario.")
    usuario: str = Field(..., description="Usuario que creó el comentario.")
    fecha_edicion: Optional[str] = Field(None, description="Fecha y hora de la última edición del comentario.")
