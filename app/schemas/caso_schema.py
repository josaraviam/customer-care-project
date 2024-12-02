from pydantic import BaseModel, Field, constr
from typing import List, Optional
from app.schemas.comentario_schema import ComentarioResponseSchema  # Esquema, no modelo


class CasoSchema(BaseModel):
    id_caso: Optional[int] = Field(None, description="ID único del caso en la base de datos.")
    fecha_contacto: str = Field(..., description="Fecha del contacto en formato ISO.")
    canal_contacto: str = Field(..., description="Canal del contacto.")
    pnr: constr(min_length=6, max_length=6) = Field(..., description="PNR único.")
    tipo_caso: str = Field(..., description="Tipo de caso.")
    comentarios: List[ComentarioResponseSchema] = Field(default=[], description="Comentarios asociados.")


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
                        "id_comentario": "64b37bc7d2f5f8e5e3b76c39",
                        "pnr": "ABC123",
                        "tags": ["urgente", "reembolso"],
                        "canal_contacto": "Facebook",
                        "estado": "pendiente",
                        "texto": "El cliente solicita reembolso.",
                        "fecha_creacion": "2024-11-20T14:30:00Z",
                        "usuario": "admin@example.com",
                        "fecha_edicion": None,
                    }
                ],
            }
        }
