from pydantic import BaseModel

class BanoCreate(BaseModel):
    edificio: str
    nivel: str
    numero: int
    sexo: str  # "H", "M", "Mixto"


class BanoUpdate(BaseModel):
    edificio: str
    nivel: str
    numero: int
    sexo: str


class BanoResponse(BaseModel):
    id_bano: int
    edificio: str
    nivel: str
    numero: int
    sexo: str

    class Config:
        orm_mode = True
