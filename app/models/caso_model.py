from pydantic import BaseModel
from datetime import datetime

class Caso(BaseModel):
    fecha_contacto: datetime
    canal_contacto: str
    PNR: str
    tipo_caso: str
    comentarios_agente: str
