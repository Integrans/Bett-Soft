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

# Mapeo de categorías (puedes quitarlo si ya lo tienes en main.py)
categoria_map = {
    "fuga": 1,
    "taza_tapada": 2,
    "orinal_tapado": 3,
    "no_papel": 4,
    "no_jabon": 5,
    "suciedad": 6,
    "mal_olor": 7
}

def generar_folio(db: Session):
    fecha = datetime.now().strftime("%Y%m%d")
    count = db.query(models.Reporte).filter(
        models.Reporte.folio.like(f"INC-{fecha}-%")
    ).count()
    consecutivo = str(count + 1).zfill(4)
    return f"INC-{fecha}-{consecutivo}"


@router.post("/", summary="Crear un nuevo reporte")
def crear_reporte(
    tipo_problema: str = Form(...),
    edificio: str = Form(...),
    nivel: int = Form(...),
    sexo: str = Form(...),
    taza_or_orinal: str = Form(None),
    pasillo: str = Form(None),
    numero_cuenta: str = Form(None),
    es_anonimo: bool = Form(False),
    file_upload: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    folio = generar_folio(db)
    cuenta_final = "ANONIMO" if es_anonimo else numero_cuenta

    # Normalizar edificio (A1 → A-1)
    edificio_normalizado = (
        edificio.replace("A", "A-", 1)
        if edificio.startswith("A")
        else edificio
    )

    # Buscar baño
    bano = db.query(models.Bano).filter(
        models.Bano.edificio == edificio_normalizado,
        models.Bano.nivel == nivel,
        models.Bano.sexo == sexo
    ).first()

    id_bano_final = bano.id if bano else 1
    id_categoria_final = categoria_map.get(tipo_problema, 1)

    # Guardar imagen
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
        id_estado=1,  # Nuevo reporte = estado "pendiente"
        prioridad_asignada=models.PrioridadEnum.media,
        fecha_creacion=datetime.now(),
        taza_or_orinal=taza_or_orinal,
        pasillo=pasillo,
        tipo_reporte=tipo_problema,
        imagen_url=imagen_url
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
