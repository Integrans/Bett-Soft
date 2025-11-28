# backend/routers/reportes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database.connection import SessionLocal
from database import models
from schemas.reportes_schema import ReporteCreate, ReporteResponse
from utils.folio_generator import generar_folio  # ya lo usas en el proyecto

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

# Dependencia de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ReporteResponse, status_code=201)
def crear_reporte(datos: ReporteCreate, db: Session = Depends(get_db)):
    """
    Crea un reporte desde el formulario público.
    """

    # 1. Buscar el baño por edificio / nivel / sexo
    bano = (
        db.query(models.Bano)
        .filter(
            models.Bano.edificio == datos.edificio,
            models.Bano.nivel == datos.nivel,
            models.Bano.sexo == datos.sexo,
        )
        .first()
    )
    if not bano:
        raise HTTPException(status_code=400, detail="Baño no válido")

    # 2. Buscar la categoría por tipo_problema (nombre en categorias_incidente)
    categoria = (
        db.query(models.Categoria)
        .filter(models.Categoria.nombre == datos.tipo_problema)
        .first()
    )
    if not categoria:
        raise HTTPException(status_code=400, detail="Tipo de problema no válido")

    # 3. Número de cuenta (anónimo)
    if datos.es_anonimo or not datos.numero_cuenta:
        numero_cuenta = "ANONIMO"
    else:
        numero_cuenta = datos.numero_cuenta

    # 4. Generar folio
    folio = generar_folio(db)

    # 5. Crear objeto Reporte
    nuevo_reporte = models.Reporte(
        folio=folio,
        numero_cuenta=numero_cuenta,
        id_bano=bano.id_bano,
        id_categoria=categoria.id_categoria,
        id_estado=1,  # pendiente / en_proceso dependiendo de tu Enum
        fecha_creacion=datetime.utcnow(),
        prioridad_asignada=categoria.prioridad_default,
        imagen_url=None,  # por ahora
        taza_o_orinal=datos.taza_o_orinal,
        pasillo=datos.pasillo,
        tipo_reporte=models.TipoReporteEnum(datos.tipo_problema),
        edificio=datos.edificio,
        sexo=datos.sexo,
    )
        

    db.add(nuevo_reporte)
    db.commit()
    db.refresh(nuevo_reporte)

    return ReporteResponse(
        folio=nuevo_reporte.folio,
        mensaje="Reporte creado correctamente"
    )

    # 6. Devolver el objeto usando el schema de respuesta
    return ReporteResponse.from_orm(nuevo_reporte)
