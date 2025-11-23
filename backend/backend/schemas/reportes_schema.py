from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReporteCreate(BaseModel):
    numero_cuenta: str
    id_categoria: int
    taza_o_orinal: str  # "taza" | "orinal"
    pasillo: str        # "frente" | "atras"
    tipo_reporte: str   # "fuga" | "taza_tapada" | "orinal_tapado" | "no_papel" | "no_jabon" | "suciedad" | "mal_olor"
    edificio: str
    sexo: str           # "H" | "M" | "Mixto"
    imagen_url: Optional[str] = None


class ReporteResponse(BaseModel):
    mensaje: str
    folio: str
    prioridad_asignada: str

    class Config:
        from_attributes = True
