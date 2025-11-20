from pydantic import BaseModel

class EstadoCreate(BaseModel):
    nombre: str   # "en_proceso" | "resuelto" | "descartado"


class EstadoUpdate(BaseModel):
    nombre: str


class EstadoResponse(BaseModel):
    id_estado: int
    nombre: str

    class Config:
        orm_mode = True
