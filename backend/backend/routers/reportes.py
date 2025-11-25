from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from database import models
from schemas.reportes_schema import ReporteCreate, ReporteResponse 
import uuid
from datetime import datetime

router = APIRouter(prefix="/reportes", tags=["reportes"])

@router.post("/", response_model=ReporteResponse)
def crear_reporte(datos: ReporteCreate, db: Session = Depends(get_db)):
    
    nuevo_folio = str(uuid.uuid4())[:8].upper()

    cuenta = "ANONIMO"
    if not datos.es_anonimo and datos.numero_cuenta:
        cuenta = datos.numero_cuenta

    bano = db.query(models.Bano).filter(
        models.Bano.edificio == datos.edificio,
        models.Bano.nivel == datos.nivel,
        models.Bano.sexo == datos.sexo 
    ).first()

    id_bano_final = bano.id_bano if bano else 1

    id_categoria_final = 1 

    nuevo_reporte = models.Reporte(
        folio = nuevo_folio,
        numero_cuenta = cuenta,
        id_bano = id_bano_final,
        id_categoria = id_categoria_final, 
        id_estado = 1,
        fecha_creacion = datetime.now(),
        prioridad_asignada = models.PrioridadEnum.media, 
        
        taza_or_orinal = datos.taza_or_orinal,
        pasillo = datos.pasillo,
        tipo_reporte = datos.tipo_problema, 
        imagen_url = None
    )

    try:
        db.add(nuevo_reporte)
        db.commit()
        db.refresh(nuevo_reporte)
        return {"mensaje": "Reporte creado exitosamente", "folio": nuevo_folio}
    except Exception as e:
        db.rollback()
        print("ERROR EN BD:", e)
        raise HTTPException(status_code=500, detail=str(e))