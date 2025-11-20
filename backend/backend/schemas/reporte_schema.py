from pydantic import BaseModel
from typing import Optional

class ReporteCreate(BaseModel):
    id_bano: int
    id_categoria: int
    descripcion: str
    imagen_url: Optional[str] = None
