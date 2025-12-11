from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database import models
from datetime import datetime
import shutil
import os
from typing import List, Optional
from utils.excel_generator import generar_excel_reportes

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


def calcular_prioridad(tipo_problema: Optional[str]):
    tipo = (tipo_problema or "").lower().strip()
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


# Si en el frontend envías grupos (A1-A2 etc.) y en tu BD también hay filas
# con esos mismos strings, podemos mapearlos directamente.
# Si en algún momento prefieres mapear "A1-A2" -> ["A-1","A-2"] hazlo aquí.
GRUPOS_A_EDIFICIOS = {
    "A1-A2": ["A1-A2"],
    "A3-A4": ["A3-A4"],
    "A5-A6": ["A5-A6"],
    "A7-A8": ["A7-A8"],
    "A9-A10": ["A9-A10"],
    "A11-A12": ["A11-A12"],
    "Idiomas": ["Idiomas"],
    "A15": ["A15"],
    "CEDETEC": ["CEDETEC"],
    "Posgrado": ["Posgrado"],
    "CEMM": ["CEMM"]
}


@router.get("/", summary="Obtener lista de reportes")
def obtener_reportes(db: Session = Depends(get_db)):
    reportes = db.query(models.Reporte).all()
    return reportes


@router.post("/", summary="Crear un nuevo reporte")
def crear_reporte(
    tipo_problema: str = Form(...),
    edificio: str = Form(...),               # viene del select del frontend (ej. "A3-A4", "Idiomas", "A15", "CEDETEC")
    nivel: int = Form(...),
    sexo: str = Form(...),                   # "H", "M", "Mixto" o "Ambos" desde el frontend
    pasillo: Optional[str] = Form(None),     # "frente" | "atras" | None
    taza_o_orinal: Optional[str] = Form(None),  # "taza" | "orinal" (ahora sí lo recibimos)
    numero_cuenta: Optional[str] = Form(None),
    es_anonimo: bool = Form(False),          # FastAPI parsea "true"/"false"
    file_upload: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # --- folio y cuenta ---
    folio = generar_folio(db)
    cuenta_final = "ANONIMO" if es_anonimo else (numero_cuenta or "")

    # --- normalizar / validar edificio ---
    edificio_input = (edificio or "").strip()
    if not edificio_input:
        raise HTTPException(status_code=400, detail="El campo 'edificio' es obligatorio.")

    edificios_posibles: List[str] = GRUPOS_A_EDIFICIOS.get(edificio_input, [edificio_input])

    # --- normalizar sexo: aceptar "Ambos" como Mixto para la BD ---
    sexo_input = (sexo or "").strip()
    if sexo_input.lower() == "ambos":
        sexo_input = "Mixto"

    try:
        sexo_enum = models.SexoEnum(sexo_input)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Valor de sexo inválido: {sexo_input}")

    # --- buscar baño existente según edificio(s), nivel y sexo ---
    bano = db.query(models.Bano).filter(
        models.Bano.edificio.in_(edificios_posibles),
        models.Bano.nivel == nivel,
        models.Bano.sexo == sexo_enum
    ).first()

    # si no hay con sexo exacto, intentar con Mixto (si usuario pidió H o M)
    if not bano and sexo_enum in (models.SexoEnum.H, models.SexoEnum.M):
        bano_alt = db.query(models.Bano).filter(
            models.Bano.edificio.in_(edificios_posibles),
            models.Bano.nivel == nivel,
            models.Bano.sexo == models.SexoEnum.Mixto
        ).first()
        if bano_alt:
            bano = bano_alt

    if not bano:
        raise HTTPException(
            status_code=404,
            detail=f"No existe baño registrado en {edificio_input}, nivel {nivel}, sexo {sexo_input}"
        )

    # --- Categoria / Tipo de reporte (enum) ---
    try:
        tipo_reporte_enum = models.TipoReporteEnum(tipo_problema)
    except Exception:
        # Intentar normalizar strings comunes (por si el frontend manda "WC tapado" etc.)
        tipo_norm = tipo_problema.strip().lower().replace(" ", "_")
        try:
            tipo_reporte_enum = models.TipoReporteEnum(tipo_norm)
        except Exception:
            raise HTTPException(status_code=400, detail=f"Tipo de problema inválido: {tipo_problema}")

    # --- taza/orinal: preferir lo que venga en el form; si no viene, inferir desde tipo_problema ---
    taza_val = None
    if taza_o_orinal:
        val = taza_o_orinal.strip().lower()
        if val in ("orinal", "mingitorio"):
            taza_val = "orinal"
        elif val in ("taza", "wc", "inodoro"):
            taza_val = "taza"
        else:
            # dejarlo None y continuar (no es fatal)
            taza_val = None
    else:
        # inferir por tipo_problema
        if "orinal" in tipo_problema.lower():
            taza_val = "orinal"
        elif "taza" in tipo_problema.lower() or "wc" in tipo_problema.lower() or "inodoro" in tipo_problema.lower():
            taza_val = "taza"

    # validar que el baño seleccionado tenga el sanitario solicitado
    if taza_val == "orinal" and (bano.tiene_orinal == 0 or bano.tiene_orinal is None):
        raise HTTPException(status_code=400, detail="El baño seleccionado no tiene mingitorios (orinales).")
    if taza_val == "taza" and (bano.tiene_taza == 0 or bano.tiene_taza is None):
        raise HTTPException(status_code=400, detail="El baño seleccionado no tiene WC (tazas).")

    # --- pasillo enum (opcional) ---
    pasillo_enum = None
    if pasillo:
        try:
            pasillo_enum = models.PasilloEnum(pasillo)
        except Exception:
            # aceptar valores comunes en minúscula
            pnorm = pasillo.strip().lower()
            if pnorm in ("frente", "atras", "atrás"):
                pasillo_enum = models.PasilloEnum.frente if pnorm == "frente" else models.PasilloEnum.atras
            else:
                raise HTTPException(status_code=400, detail=f"Valor de pasillo inválido: {pasillo}")

    # --- categoría numerica ---
    id_categoria_final = categoria_map.get(tipo_reporte_enum.value if hasattr(tipo_reporte_enum, "value") else tipo_reporte_enum, 1)

    # --- prioridad ---
    prioridad_final = calcular_prioridad(tipo_problema)

    # --- guardar imagen (sanitizar nombre) ---
    imagen_url = None
    if file_upload:
        filename = os.path.basename(file_upload.filename or "")
        # prevenir nombres vacíos
        if filename:
            ruta = f"uploads/{folio}_{filename}"
            with open(ruta, "wb") as buffer:
                shutil.copyfileobj(file_upload.file, buffer)
            imagen_url = ruta

    # --- crear objeto Reporte ---
    try:
        nuevo_reporte = models.Reporte(
            folio=folio,
            numero_cuenta=cuenta_final,
            id_bano=bano.id_bano,
            id_categoria=id_categoria_final,
            id_estado=1,
            prioridad_asignada=prioridad_final,
            fecha_creacion=datetime.now(),
            taza_o_orinal=(models.TazaOrinalEnum(taza_val) if taza_val else None),
            pasillo=(pasillo_enum if pasillo_enum else None),
            tipo_reporte=tipo_reporte_enum,
            imagen_url=imagen_url,
            edificio=bano.edificio,   # guardamos el valor real de la DB
            sexo=sexo_enum
        )

        db.add(nuevo_reporte)
        db.commit()
        db.refresh(nuevo_reporte)

        return {
            "mensaje": "Reporte creado exitosamente",
            "folio": folio,
            "id_reporte": nuevo_reporte.id_reporte
        }

    except Exception as e:
        db.rollback()
        # Re-lanzar error con detalle (útil en desarrollo)
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------------------------------
# 🔥🔥🔥 ENDPOINT NECESARIO PARA admin.js 🔥🔥🔥
# -----------------------------------------------------------
@router.get("/folio/{folio}", summary="Obtener reporte por folio")
def obtener_reporte_por_folio(folio: str, db: Session = Depends(get_db)):
    reporte = db.query(models.Reporte).filter(models.Reporte.folio == folio).first()

    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    return reporte

# -----------------------------------------------------------
# ENDPOINTS PARA GENERAR EXCEL
# -----------------------------------------------------------

@router.get("/descargar/todos", summary="Descargar todos los reportes en Excel")
def descargar_todos_reportes(db: Session = Depends(get_db)):
    """
    Descarga un Excel con todos los reportes de incidencias.
    """
    reportes = db.query(models.Reporte).all()
    
    if not reportes:
        raise HTTPException(status_code=404, detail="No hay reportes para descargar")
    
    ruta_archivo = generar_excel_reportes(reportes)
    
    return FileResponse(
        path=ruta_archivo,
        filename=os.path.basename(ruta_archivo),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@router.get("/descargar/edificio/{edificio}", summary="Descargar reportes de un edificio en Excel")
def descargar_reportes_edificio(edificio: str, db: Session = Depends(get_db)):
    """
    Descarga un Excel con los reportes de un edificio específico.
    Ejemplo: /reportes/descargar/edificio/A3-A4
    """
    reportes = db.query(models.Reporte).filter(
        models.Reporte.edificio == edificio
    ).all()
    
    if not reportes:
        raise HTTPException(status_code=404, detail=f"No hay reportes para el edificio {edificio}")
    
    nombre_archivo = f"reportes_{edificio}"
    ruta_archivo = generar_excel_reportes(reportes, nombre_archivo)
    
    return FileResponse(
        path=ruta_archivo,
        filename=os.path.basename(ruta_archivo),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@router.get("/descargar/prioridad/{prioridad}", summary="Descargar reportes por prioridad en Excel")
def descargar_reportes_prioridad(prioridad: str, db: Session = Depends(get_db)):
    """
    Descarga un Excel con los reportes de una prioridad específica.
    Prioridades: alta, media, baja
    """
    try:
        prioridad_enum = models.PrioridadEnum(prioridad.lower())
    except Exception:
        raise HTTPException(status_code=400, detail=f"Prioridad inválida: {prioridad}")
    
    reportes = db.query(models.Reporte).filter(
        models.Reporte.prioridad_asignada == prioridad_enum
    ).all()
    
    if not reportes:
        raise HTTPException(status_code=404, detail=f"No hay reportes con prioridad {prioridad}")
    
    nombre_archivo = f"reportes_prioridad_{prioridad}"
    ruta_archivo = generar_excel_reportes(reportes, nombre_archivo)
    
    return FileResponse(
        path=ruta_archivo,
        filename=os.path.basename(ruta_archivo),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@router.get("/descargar/fecha/{fecha}", summary="Descargar reportes por fecha en Excel")
def descargar_reportes_fecha(fecha: str, db: Session = Depends(get_db)):
    """
    Descarga un Excel con los reportes de una fecha específica.
    Formato: YYYY-MM-DD (ej: 2025-12-10)
    """
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use: YYYY-MM-DD")
    
    reportes = db.query(models.Reporte).filter(
        models.Reporte.fecha_creacion.ilike(f"{fecha}%")
    ).all()
    
    if not reportes:
        raise HTTPException(status_code=404, detail=f"No hay reportes para la fecha {fecha}")
    
    nombre_archivo = f"reportes_{fecha}"
    ruta_archivo = generar_excel_reportes(reportes, nombre_archivo)
    
    return FileResponse(
        path=ruta_archivo,
        filename=os.path.basename(ruta_archivo),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )