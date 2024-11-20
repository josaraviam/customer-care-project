from pydantic import BaseModel, Field
from typing import Optional

class Caso(BaseModel):
    id_caso: int
    fecha_contacto: str
    canal_contacto: str
    pnr: str
    tipo_caso: str
    comentarios: str

    class Config:
        json_schema_extra = {
            "example": {
                "id_caso": 1,
                "fecha_contacto": "2024-11-20",
                "canal_contacto": "Facebook",
                "pnr": "ABC123",
                "tipo_caso": "Reclamo",
                "comentarios": "Cliente solicita reembolso."
            }
        }
