from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import Reporte
from schemas.reportes_schema import ReporteCreate, ReporteResponse
from utils.folio_generator import generar_folio

router = APIRouter(prefix="/reportes", tags=["Reportes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ReporteResponse)
def crear_reporte(data: ReporteCreate, db: Session = Depends(get_db)):

    # Generar folio
    folio = generar_folio(db)

    nuevo = Reporte(
        folio=folio,
        numero_cuenta=data.numero_cuenta,
        id_categoria=data.id_categoria,
        prioridad_asignada="media",   # DEFAULT temporal hasta definir lógica
        imagen_url=data.imagen_url,
        taza_o_orinal=data.taza_o_orinal,
        pasillo=data.pasillo,
        tipo_reporte=data.tipo_reporte,
        edificio=data.edificio,
        sexo=data.sexo
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "mensaje": "Reporte creado",
        "folio": nuevo.folio,
        "prioridad_asignada": nuevo.prioridad_asignada
    }
