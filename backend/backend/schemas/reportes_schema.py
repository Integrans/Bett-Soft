from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enums import SexoEnum, PasilloEnum, TazaOrinalEnum, TipoReporteEnum, PrioridadEnum, EstadoReporteEnum

# ---------------------------------------------------------
# Schema para crear un reporte
# ---------------------------------------------------------
class ReporteCreate(BaseModel):
    tipo_problema: str
    edificio: str
    nivel: int
    sexo: str
    taza_or_orinal: str
    pasillo: str
    numero_cuenta: Optional[str] = None
    es_anonimo: bool = False
    # file_upload se maneja directamente en FastAPI, no aquí

# ---------------------------------------------------------
# Schema de salida (respuesta)
# ---------------------------------------------------------
class ReporteOut(BaseModel):
    id_reporte: int
    folio: str
    numero_cuenta: str
    id_bano: int
    id_categoria: int
    id_estado: int
    fecha_creacion: datetime
    prioridad_asignada: PrioridadEnum
    tipo_reporte: TipoReporteEnum
    taza_or_orinal: TazaOrinalEnum
    pasillo: PasilloEnum
    imagen_url: Optional[str]

    class Config:
        orm_mode = True
