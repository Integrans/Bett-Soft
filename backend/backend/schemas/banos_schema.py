from pydantic import BaseModel


class BanoResponse(BaseModel):
    id_bano: int
    edificio: str
    nivel: int
    sexo: str  # "H", "M", "Mixto"

    class Config:
        from_attributes = True
