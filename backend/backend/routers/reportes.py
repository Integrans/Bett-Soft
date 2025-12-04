from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database import models
from datetime import datetime
import shutil
import os

router = APIRouter(prefix="/reportes", tags=["Reportes"])

os.makedirs("uploads", exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mapeo de categorías
categoria_map = {
    "fuga": 1,
    "taza_tapada": 2,
    "orinal_tapado": 3,
    "no_papel": 4,
    "no_jabon": 5,
    "suciedad": 6,
    "mal_olor": 7
}

def calcular_prioridad(tipo_problema: str):
    tipo = tipo_problema.lower().strip()

    if tipo in ["fuga", "desbordamiento", "inundacion", "inundación"]:
        return models.PrioridadEnum.alta

    if tipo in ["taza_tapada", "orinal_tapado", "sin_agua"]:
        return models.PrioridadEnum.media

    return models.PrioridadEnum.baja


def generar_folio(db: Session):
    fecha = datetime.now().strftime("%Y%m%d")
    count = db.query(models.Reporte).filter(
        models.Reporte.folio.like(f"INC-{fecha}-%")
    ).count()
    consecutivo = str(count + 1).zfill(4)
    return f"INC-{fecha}-{consecutivo}"


# -------------------------------------------------------
# 🔵 GET /reportes/ — LISTA LIMPIA DE REPORTES (Opción B)
# -------------------------------------------------------
@router.get("/", summary="Obtener lista de reportes")
def obtener_reportes(db: Session = Depends(get_db)):
    reportes = db.query(models.Reporte).all()
    return reportes   # 👈 EXACTAMENTE LO QUE PIDE FASTAPI


# -------------------------------------------------------
# 🟢 POST /reportes/ — CREAR REPORTE
# -------------------------------------------------------
@router.post("/", summary="Crear un nuevo reporte")
def crear_reporte(
    tipo_problema: str = Form(...),
    edificio: str = Form(...),
    nivel: int = Form(...),
    sexo: str = Form(...),
    taza_o_orinal: str = Form(None),
    pasillo: str = Form(None),
    numero_cuenta: str = Form(None),
    es_anonimo: bool = Form(False),
    file_upload: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    folio = generar_folio(db)

    cuenta_final = "ANONIMO" if es_anonimo else numero_cuenta

    edificio_normalizado = (
        edificio.replace("A", "A-", 1)
        if edificio.startswith("A")
        else edificio
    )

    bano = db.query(models.Bano).filter(
        models.Bano.edificio == edificio_normalizado,
        models.Bano.nivel == nivel,
        models.Bano.sexo == sexo
    ).first()

    id_bano_final = bano.id if bano else 1

    id_categoria_final = categoria_map.get(tipo_problema, 1)

    imagen_url = None
    if file_upload:
        ruta = f"uploads/{folio}_{file_upload.filename}"
        with open(ruta, "wb") as buffer:
            shutil.copyfileobj(file_upload.file, buffer)
        imagen_url = ruta

    nuevo_reporte = models.Reporte(
        folio=folio,
        numero_cuenta=cuenta_final,
        id_bano=id_bano_final,
        id_categoria=id_categoria_final,
        id_estado=1,
        prioridad_asignada=models.PrioridadEnum.media,
        fecha_creacion=datetime.now(),
        taza_o_orinal=taza_o_orinal,
        pasillo=pasillo,
        tipo_reporte=tipo_problema,
        imagen_url=imagen_url,
        edificio=edificio_normalizado,
        sexo=sexo
    )

    try:
        db.add(nuevo_reporte)
        db.commit()
        db.refresh(nuevo_reporte)

        return {
            "mensaje": "Reporte creado exitosamente",
            "folio": folio
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))