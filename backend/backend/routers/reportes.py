from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from utils.folio_generator import generar_folio
from database.models import Reporte, CategoriaIncidente
from schemas.reporte_schema import ReporteCreate

router = APIRouter(prefix="/reportes", tags=["Reportes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def crear_reporte(data: ReporteCreate, db: Session = Depends(get_db)):

    # Generar folio único
    nuevo_folio = generar_folio(db)

    # Obtener prioridad por defecto desde la categoría
    categoria = db.query(CategoriaIncidente).filter(
        CategoriaIncidente.id_categoria == data.id_categoria
    ).first()

    if not categoria:
        return {"error": "La categoría no existe"}

    prioridad_auto = categoria.prioridad_default

    # Crear reporte
    reporte = Reporte(
        folio=nuevo_folio,
        id_bano=data.id_bano,
        id_categoria=data.id_categoria,
        descripcion=data.descripcion,
        id_estado=1,  # en_proceso por defecto
        prioridad_asignada=prioridad_auto,
        imagen_url=data.imagen_url
    )

    db.add(reporte)
    db.commit()
    db.refresh(reporte)

    return {
        "mensaje": "Reporte creado",
        "folio": reporte.folio,
        "prioridad_asignada": prioridad_auto
    }

