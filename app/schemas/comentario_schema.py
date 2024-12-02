from pydantic import BaseModel, Field
from typing import List, Optional

class ComentarioCreateSchema(BaseModel):
    pnr: str = Field(..., min_length=6, max_length=6, description="PNR asociado al comentario.")
    tags: List[str] = Field(..., description="Etiquetas asociadas al comentario.")
    canal_contacto: str = Field(..., description="Canal de contacto donde se originó el comentario.")
    estado: str = Field(..., description="Estado actual del comentario.")
    texto: str = Field(..., min_length=1, description="Texto del comentario.")


class ComentarioResponseSchema(BaseModel):
    id_comentario: str = Field(..., alias="_id", description="ID único del comentario en MongoDB.")
    pnr: str = Field(..., min_length=6, max_length=6, description="PNR asociado al comentario.")
    fecha_creacion: str = Field(..., description="Fecha y hora de creación.")
    usuario: str = Field(..., description="Usuario que creó el comentario.")
    tags: List[str] = Field(..., description="Etiquetas asociadas al comentario.")
    canal_contacto: str = Field(..., description="Canal de contacto.")
    estado: str = Field(..., description="Estado actual.")
    texto: str = Field(..., description="Texto del comentario.")
    fecha_edicion: Optional[str] = Field(None, description="Fecha de última edición.")

    class Config:
        populate_by_name = True
        json_schema_extra = {  # Cambiado por Pydantic v2
            "example": {
                "id_comentario": "64b37bc7d2f5f8e5e3b76c39",
                "pnr": "ABC123",
                "fecha_creacion": "
