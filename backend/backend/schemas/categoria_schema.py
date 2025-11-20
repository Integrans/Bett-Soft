from pydantic import BaseModel

class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: str
    prioridad_default: str   # "alta" | "media" | "baja"


class CategoriaUpdate(BaseModel):
    nombre: str
    descripcion: str
    prioridad_default: str


class CategoriaResponse(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: str
    prioridad_default: str

    class Config:
        orm_mode = True
