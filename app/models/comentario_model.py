from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class ComentarioCreate(BaseModel):
    """
    Modelo para la creación de comentarios.
    El campo 'usuario' será asignado automáticamente desde el token JWT.
    """
    pnr: str = Field(..., min_length=6, max_length=6, description="PNR asociado al comentario.")
    tags: List[str] = Field(..., description="Etiquetas asociadas al comentario.")
    canal_contacto: str = Field(..., description="Canal de contacto donde se originó el comentario.")
    estado: str = Field(..., description="Estado actual del comentario.")
    texto: str = Field(..., description="Texto del comentario.")


class Comentario(BaseModel):
    """
    Modelo completo de comentario para respuestas y almacenamiento.
    Incluye todos los campos, incluido 'usuario', asignado automáticamente.
    """
    id_comentario: str = Field(..., alias="_id", description="ID único del comentario en MongoDB.")
    pnr: str = Field(..., min_length=6, max_length=6, description="PNR asociado al comentario.")
    fecha_creacion: datetime = Field(..., description="Fecha y hora de creación del comentario.")
    usuario: str = Field(..., description="Usuario que creó el comentario.")
    tags: List[str] = Field(..., description="Etiquetas asociadas al comentario.")
    canal_contacto: str = Field(..., description="Canal de contacto donde se originó el comentario.")
    estado: str = Field(..., description="Estado actual del comentario.")
    texto: str = Field(..., description="Texto del comentario.")
    fecha_edicion: Optional[datetime] = Field(None, description="Fecha y hora de la última edición del comentario.")
