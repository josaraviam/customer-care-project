from pydantic import BaseModel, Field
from typing import List


class ComentarioCreateSchema(BaseModel):
    """
    Esquema para la creación de comentarios.
    Este esquema se utiliza para validar los datos enviados al endpoint.
    """
    pnr: str = Field(..., min_length=6, max_length=6, description="PNR asociado al comentario.")
    tags: List[str] = Field(..., description="Etiquetas asociadas al comentario.")
    canal_contacto: str = Field(..., description="Canal de contacto donde se originó el comentario.")
    estado: str = Field(..., description="Estado actual del comentario (por ejemplo, 'pendiente', 'resuelto').")
    texto: str = Field(..., min_length=1, description="Texto del comentario.")


class ComentarioResponseSchema(BaseModel):
    """
    Esquema para la respuesta de comentarios.
    Este esquema se utiliza para estructurar la respuesta enviada al cliente.
    """
    id_comentario: str = Field(..., alias="_id", description="ID único del comentario en MongoDB.")
    pnr: str = Field(..., min_length=6, max_length=6, description="PNR asociado al comentario.")
    fecha_creacion: str = Field(..., description="Fecha y hora de creación del comentario en formato ISO.")
    usuario: str = Field(..., description="Usuario que creó el comentario.")
    tags: List[str] = Field(..., description="Etiquetas asociadas al comentario.")
    canal_contacto: str = Field(..., description="Canal de contacto donde se originó el comentario.")
    estado: str = Field(..., description="Estado actual del comentario.")
    texto: str = Field(..., description="Texto del comentario.")
    fecha_edicion: Optional[str] = Field(None, description="Fecha y hora de la última edición del comentario.")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id_comentario": "64b37bc7d2f5f8e5e3b76c39",
                "pnr": "ABC123",
                "fecha_creacion": "2024-11-20T14:30:00Z",
                "usuario": "admin@example.com",
                "tags": ["urgente", "reembolso"],
                "canal_contacto": "Facebook",
                "estado": "pendiente",
                "texto": "El cliente solicita un reembolso.",
                "fecha_edicion": None
            }
        }
