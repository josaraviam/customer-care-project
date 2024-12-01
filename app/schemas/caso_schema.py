from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.comentario_schema import Comentario  # Importa el esquema Comentario


class Caso(BaseModel):
    id_caso: Optional[int] = Field(None, description="ID único del caso en la base de datos.")
    fecha_contacto: str = Field(..., description="Fecha del contacto en formato YYYY-MM-DD.")
    canal_contacto: str = Field(..., description="Canal de contacto asociado al caso.")
    pnr: str = Field(..., min_length=6, max_length=6, description="PNR único del caso.")
    tipo_caso: str = Field(..., description="Tipo de caso.")
    comentarios: List[Comentario] = Field([], description="Lista de comentarios asociados al caso.")

    class Config:
        json_schema_extra = {
            "example": {
                "id_caso": 1,
                "fecha_contacto": "2024-11-20",
                "canal_contacto": "Facebook",
                "pnr": "ABC123",
                "tipo_caso": "Reclamo",
                "comentarios": [
                    {
                        "_id": "64b37bc7d2f5f8e5e3b76c39",
                        "pnr": "ABC123",
                        "tags": ["urgente", "reembolso"],
                        "canal_contacto": "Facebook",
                        "estado": "pendiente",
                        "texto": "El cliente solicita reembolso.",
                        "fecha_creacion": "2024-11-20T14:30:00Z",
                        "usuario": "admin@example.com"
                    }
                ]
            }
        }
