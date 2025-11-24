from pydantic import BaseModel


class CategoriaResponse(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: str
    prioridad_default: str  # "alta", "media", "baja"

    class Config:
        from_attributes = True
