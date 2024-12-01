from pydantic import BaseModel, Field
from typing import List, Optional


class Caso(BaseModel):
    id_caso: Optional[int] = Field(None, description="ID único del caso, generado automáticamente.")
    fecha_contacto: str = Field(..., description="Fecha en que se generó el contacto.")
    canal_contacto: str = Field(..., description="Canal por el que se generó el contacto (FB, TW, IG, WA).")
    pnr: str = Field(..., min_length=6, max_length=6, description="PNR único asociado al caso.")
    tipo_caso: str = Field(..., description="Tipo de caso (Reclamo, Consulta, etc.).")
    comentarios: List[Comentario] = Field([], description="Lista de comentarios asociados al caso.")

    class Config:
        schema_extra = {
            "example": {
                "id_caso": 1,
                "fecha_contacto": "2024-11-20",
                "canal_contacto": "Facebook",
                "pnr": "ABC123",
                "tipo_caso": "Reclamo",
                "comentarios": [
                    {
                        "_id": "64b2c2f70ad94e001c2c8b85",
                        "pnr": "ABC123",
                        "tags": ["Reclamo", "Urgente"],
                        "canal_contacto": "Facebook",
                        "estado": "Pendiente",
                        "texto": "Cliente solicita reembolso.",
                        "fecha_creacion": "2024-11-20T15:32:00",
                        "usuario": "admin@example.com"
                    }
                ]
            }
        }
