from pydantic import BaseModel
from typing import Optional

class ReporteCreate(BaseModel):
    tipo_problema: str      
    edificio: str          
    nivel: int             
    sexo: str               
<<<<<<< HEAD
    taza_o_orinal: str     
=======
    taza_or_orinal: str     
>>>>>>> origin/dev
    pasillo: str            
    numero_cuenta: Optional[str] = None
    es_anonimo: bool = False


class ReporteResponse(BaseModel):
    mensaje: str
    folio: str
    
    class Config:
        from_attributes = True