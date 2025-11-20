from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import EstadoReporte
from schemas.estado_schema import EstadoCreate, EstadoUpdate, EstadoResponse

router = APIRouter(prefix="/estados", tags=["Estados"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Crear Estado
# -------------------------
@router.post("/", response_model=EstadoResponse)
def crear_estado(data: EstadoCreate, db: Session = Depends(get_db)):

    estado = EstadoReporte(nombre=data.nombre)

    db.add(estado)
    db.commit()
    db.refresh(estado)

    return estado


# -------------------------
# Listar todos
# -------------------------
@router.get("/", response_model=list[EstadoResponse])
def obtener_estados(db: Session = Depends(get_db)):
    return db.query(EstadoReporte).all()


# -------------------------
# Obtener uno por ID
# -------------------------
@router.get("/{id_estado}", response_model=EstadoResponse)
def obtener_estado(id_estado: int, db: Session = Depends(get_db)):

    estado = db.query(EstadoReporte).filter(
        EstadoReporte.id_estado == id_estado
    ).first()

    if not estado:
        return {"error": "El estado no existe"}

    return estado


# -------------------------
# Actualizar
# -------------------------
@router.put("/{id_estado}", response_model=EstadoResponse)
def actualizar_estado(id_estado: int, data: EstadoUpdate, db: Session = Depends(get_db)):

    estado = db.query(EstadoReporte).filter(
        EstadoReporte.id_estado == id_estado
    ).first()

    if not estado:
        return {"error": "El estado no existe"}

    estado.nombre = data.nombre
    db.commit()
    db.refresh(estado)

    return estado


# -------------------------
# Eliminar
# -------------------------
@router.delete("/{id_estado}")
def eliminar_estado(id_estado: int, db: Session = Depends(get_db)):

    estado = db.query(EstadoReporte).filter(
        EstadoReporte.id_estado == id_estado
    ).first()

    if not estado:
        return {"error": "El estado no existe"}

    db.delete(estado)
    db.commit()

    return {"mensaje": "Estado eliminado correctamente"}
