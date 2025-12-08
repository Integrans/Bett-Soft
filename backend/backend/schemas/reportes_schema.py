from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReporteCreate(BaseModel):
    tipo_problema: str      
    edificio: str          
    nivel: int             
    sexo: str               
    taza_o_orinal: str     
    pasillo: str            
    numero_cuenta: Optional[str] = None
    es_anonimo: bool = False

    # 👇 NUEVOS CAMPOS
    tipo_reporte: str | None = None
    edificio: str | None = None


class ReporteResponse(BaseModel):
    mensaje: str
    folio: str
    
    class Config:
        from_attributes = True

class ReporteAdmin(BaseModel):
    """
    Esquema usado para:
    - GET /admin/reportes
    - GET /admin/reportes/{folio}

    Incluye datos del reporte más información calculada
    de otras tablas (categoría y baño).
    """

    # Campos de la tabla reportes
    id_reporte: int
    folio: str
    numero_cuenta: Optional[str] = None
    id_bano: int
    id_categoria: int
    fecha_creacion: datetime
    id_estado: int
    prioridad_asignada: str

    # Campos extra que calculamos
    tipo_reporte: Optional[str] = None   # nombre de CategoriaIncidente
    edificio: Optional[str] = None       # edificio del baño
    sexo: Optional[str] = None           # sexo del baño

    class Config:
        from_attributes = True