from pydantic import BaseModel
from typing import Optional

class ReporteCreate(BaseModel):
    tipo_problema: str      
    edificio: str          
    nivel: int             
    sexo: str               
    taza_o_orinal: str     
    pasillo: str            
    numero_cuenta: Optional[str] = None
    es_anonimo: bool = False


class ReporteResponse(BaseModel):
    mensaje: str
    folio: str
    
    class Config:
        from_attributes = True