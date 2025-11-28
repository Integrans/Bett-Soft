from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.connection import SessionLocal
from database import models
from utils.password_utils import verify_password

router = APIRouter(
    prefix="/admin",
    tags=["Administrador"]
)

# ---------- dependencia de BD ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


# ---------- SERIALIZADOR ----------
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


# ---------- LISTAR / OBTENER ----------
@router.get("/reportes")
def listar_reportes(db: Session = Depends(get_db)):
    reportes = db.query(models.Reporte).all()
    return [reporte_a_dict(r) for r in reportes]


@router.get("/reportes/{folio}")
def obtener_reporte_por_folio(folio: str, db: Session = Depends(get_db)):
    reporte = db.query(models.Reporte).filter(models.Reporte.folio == folio).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return reporte_a_dict(reporte)


# ---------- ACTUALIZAR ESTADO ----------
class EstadoUpdate(BaseModel):
    id_estado: int

@router.put("/reportes/{folio}/estado")
def actualizar_estado_reporte(
    folio: str,
    body: EstadoUpdate,                 # body JSON: { "id_estado": 2 }
    db: Session = Depends(get_db),      # usar dependency correcta
):
    nuevo_estado = body.id_estado

    # solo permitimos 1, 2, 3
    if nuevo_estado not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Estado inválido")

    reporte = db.query(models.Reporte).filter(models.Reporte.folio == folio).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    reporte.id_estado = nuevo_estado
    db.commit()
    db.refresh(reporte)

    return {"mensaje": "Estado actualizado correctamente"}
