from pydantic import BaseModel


class AdminCreate(BaseModel):
    nombre: str
    email: str
    password: str


class AdminLogin(BaseModel):
    email: str
    password: str


class AdminResponse(BaseModel):
    mensaje: str

    class Config:
        from_attributes = True