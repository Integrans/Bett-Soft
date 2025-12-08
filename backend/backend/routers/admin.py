from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.connection import SessionLocal
from database import models
from utils.password_utils import verify_password

from schemas.reportes_schema import ReporteAdmin


# 🚨 IMPORTANTE: sin prefix aquí
router = APIRouter(
    tags=["Administrador"]
)


# ---------- dependencia de BD ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class EstadoUpdate(BaseModel):
    id_estado: int   # 1 = pendiente, 2 = en_proceso, 3 = resuelto / descartado


# ---------- LOGIN ----------
class AdminLogin(BaseModel):
    email: str
    password: str


@router.post("/login")
def login_admin(datos: AdminLogin, db: Session = Depends(get_db)):
    admin = (
        db.query(models.Admin)
        .filter(models.Admin.email == datos.email)
        .first()
    )
    if not admin or not verify_password(datos.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {"mensaje": "Login correcto"}


# ---------- SERIALIZADOR SENCILLO ----------
def reporte_a_dict(r: models.Reporte) -> dict:
    return {
        "id_reporte": r.id_reporte,
        "folio": r.folio,
        "numero_cuenta": r.numero_cuenta,
        "id_bano": r.id_bano,
        "id_categoria": r.id_categoria,
        "fecha_creacion": r.fecha_creacion.isoformat() if r.fecha_creacion else None,
        "id_estado": r.id_estado,
        "prioridad_asignada": r.prioridad_asignada,
    }


# ---------- LISTAR REPORTES (ADMIN) ----------
@router.get("/reportes", response_model=List[ReporteAdmin])
def listar_reportes(db: Session = Depends(get_db)):

    reportes_db = db.query(models.Reporte).all()
    resultado: List[ReporteAdmin] = []

    for rep in reportes_db:

        categoria = (
            db.query(models.Categoria)
            .filter(models.Categoria.id_categoria == rep.id_categoria)
            .first()
        )

        bano = (
            db.query(models.Bano)
            .filter(models.Bano.id_bano == rep.id_bano)
            .first()
        )

        resultado.append(
            ReporteAdmin(
                id_reporte=rep.id_reporte,
                folio=rep.folio,
                numero_cuenta=rep.numero_cuenta,
                id_bano=rep.id_bano,
                id_categoria=rep.id_categoria,
                fecha_creacion=rep.fecha_creacion,
                id_estado=rep.id_estado,
                prioridad_asignada=rep.prioridad_asignada,

                # enriquecidos
                tipo_reporte=categoria.nombre if categoria else None,
                edificio=bano.edificio if bano else None,
                sexo=bano.sexo if bano else None,
            )
        )

    return resultado


# ---------- OBTENER REPORTE POR FOLIO ----------
@router.get("/reportes/{folio}", response_model=ReporteAdmin)
def obtener_reporte_por_folio(folio: str, db: Session = Depends(get_db)):

    reporte = (
        db.query(models.Reporte)
        .filter(models.Reporte.folio == folio)
        .first()
    )

    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    categoria = (
        db.query(models.Categoria)
        .filter(models.Categoria.id_categoria == reporte.id_categoria)
        .first()
    )

    bano = (
        db.query(models.Bano)
        .filter(models.Bano.id_bano == reporte.id_bano)
        .first()
    )

    return ReporteAdmin(
        id_reporte=reporte.id_reporte,
        folio=reporte.folio,
        numero_cuenta=reporte.numero_cuenta,
        id_bano=reporte.id_bano,
        id_categoria=reporte.id_categoria,
        fecha_creacion=reporte.fecha_creacion,
        id_estado=reporte.id_estado,
        prioridad_asignada=reporte.prioridad_asignada,

        tipo_reporte=categoria.nombre if categoria else None,
        edificio=bano.edificio if bano else None,
        sexo=bano.sexo if bano else None,
    )


# ---------- ACTUALIZAR ESTADO ----------
@router.put("/reportes/{folio}/estado")
def actualizar_estado_reporte(
    folio: str,
    payload: EstadoUpdate,
    db: Session = Depends(get_db),
):

    nuevo_estado = payload.id_estado

    if nuevo_estado not in (1, 2, 3):
        raise HTTPException(status_code=400, detail="Estado inválido")

    reporte = (
        db.query(models.Reporte)
        .filter(models.Reporte.folio == folio)
        .first()
    )

    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    reporte.id_estado = nuevo_estado
    db.commit()
    db.refresh(reporte)

    return {"mensaje": "Estado actualizado", "id_estado": reporte.id_estado}
