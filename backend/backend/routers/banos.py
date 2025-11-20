from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import Bano
from schemas.bano_schema import BanoCreate, BanoUpdate, BanoResponse

router = APIRouter(prefix="/banos", tags=["Baños"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Crear baño
# -------------------------
@router.post("/", response_model=BanoResponse)
def crear_bano(data: BanoCreate, db: Session = Depends(get_db)):

    nuevo_bano = Bano(
        edificio=data.edificio,
        nivel=data.nivel,
        numero=data.numero,
        sexo=data.sexo
    )

    db.add(nuevo_bano)
    db.commit()
    db.refresh(nuevo_bano)

    return nuevo_bano


# -------------------------
# Listar baños
# -------------------------
@router.get("/", response_model=list[BanoResponse])
def obtener_banos(db: Session = Depends(get_db)):
    return db.query(Bano).all()


# -------------------------
# Obtener baño por ID
# -------------------------
@router.get("/{id_bano}", response_model=BanoResponse)
def obtener_bano(id_bano: int, db: Session = Depends(get_db)):

    bano = db.query(Bano).filter(Bano.id_bano == id_bano).first()

    if not bano:
        return {"error": "El baño no existe"}

    return bano


# -------------------------
# Actualizar baño
# -------------------------
@router.put("/{id_bano}", response_model=BanoResponse)
def actualizar_bano(id_bano: int, data: BanoUpdate, db: Session = Depends(get_db)):

    bano = db.query(Bano).filter(Bano.id_bano == id_bano).first()

    if not bano:
        return {"error": "El baño no existe"}

    bano.edificio = data.edificio
    bano.nivel = data.nivel
    bano.numero = data.numero
    bano.sexo = data.sexo

    db.commit()
    db.refresh(bano)

    return bano


# -------------------------
# Eliminar baño
# -------------------------
@router.delete("/{id_bano}")
def eliminar_bano(id_bano: int, db: Session = Depends(get_db)):

    bano = db.query(Bano).filter(Bano.id_bano == id_bano).first()

    if not bano:
        return {"error": "El baño no existe"}

    db.delete(bano)
    db.commit()

    return {"mensaje": "Baño eliminado correctamente"}
