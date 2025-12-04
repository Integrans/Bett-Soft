from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.connection import SessionLocal
from database.models import Admin, Reporte
from schemas.admin_schema import AdminCreate, AdminLogin, AdminResponse
from utils.password_utils import hash_password, verify_password
from datetime import datetime

# YA NO LLEVA PREFIX AQUÍ
router = APIRouter(tags=["Administrador"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# -------------------------------------------------------
# REGISTRO
# -------------------------------------------------------
@router.post("/registro", response_model=AdminResponse)
def registrar_admin(data: AdminCreate, db: Session = Depends(get_db)):

    # Validar email existente ANTES de crear
    existe = db.query(Admin).filter(Admin.email == data.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    admin = Admin(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(admin)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    return AdminResponse(mensaje="Administrador creado")



# -------------------------------------------------------
# LOGIN
# -------------------------------------------------------
@router.post("/login", response_model=AdminResponse)
def login_admin(data: AdminLogin, db: Session = Depends(get_db)):

    admin = db.query(Admin).filter(Admin.email == data.email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")

    if not verify_password(data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return AdminResponse(mensaje="Login exitoso")


# ----------------------------------------------------------------
# BODY SCHEMAS
# ----------------------------------------------------------------
class EstadoUpdate(BaseModel):
    id_admin: int
    id_estado: int


class PrioridadUpdate(BaseModel):
    id_admin: int
    prioridad_asignada: str  # "alta"|"media"|"baja"


# ----------------------------------------------------------------
# LISTAR REPORTES
# ----------------------------------------------------------------
@router.get("/reportes", response_model=List[dict])
def listar_reportes(
    estado: Optional[int] = Query(None, description="Filtrar por id_estado"),
    edificio: Optional[str] = Query(None, description="Filtrar por edificio (ej. A-4)"),
    tipo_reporte: Optional[str] = Query(None, description="Filtrar por tipo de reporte"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Reporte)

    if estado is not None:
        query = query.filter(Reporte.id_estado == estado)
    if edificio:
        query = query.filter(Reporte.edificio == edificio)
    if tipo_reporte:
        query = query.filter(Reporte.tipo_reporte == tipo_reporte)

    total = query.count()
    rows = query.order_by(Reporte.fecha_creacion.desc()).offset(offset).limit(limit).all()

    results = []
    for r in rows:
        results.append({
            "id_reporte": r.id_reporte,
            "folio": r.folio,
            "numero_cuenta": r.numero_cuenta,
            "id_bano": r.id_bano,
            "id_categoria": getattr(r, "id_categoria", None),
            "fecha_creacion": r.fecha_creacion,
            "id_estado": r.id_estado,
            "prioridad_asignada": str(r.prioridad_asignada) if r.prioridad_asignada else None,
            "imagen_url": r.imagen_url,
            "taza_o_orinal": str(r.taza_or_orinal) if getattr(r, "taza_or_orinal", None) else None,
            "pasillo": str(r.pasillo) if getattr(r, "pasillo", None) else None,
            "tipo_reporte": str(r.tipo_reporte) if getattr(r, "tipo_reporte", None) else None,
            "edificio": r.edificio,
            "sexo": str(r.sexo) if getattr(r, "sexo", None) else None
        })

    return {"total": total, "offset": offset, "limit": limit, "reportes": results}


# ----------------------------------------------------------------
# OBTENER REPORTE POR FOLIO
# ----------------------------------------------------------------
@router.get("/reportes/{folio}", response_model=dict)
def obtener_reporte_por_folio(folio: str, db: Session = Depends(get_db)):
    r = db.query(Reporte).filter(Reporte.folio == folio).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    return {
        "id_reporte": r.id_reporte,
        "folio": r.folio,
        "numero_cuenta": r.numero_cuenta,
        "id_bano": r.id_bano,
        "id_categoria": getattr(r, "id_categoria", None),
        "fecha_creacion": r.fecha_creacion,
        "id_estado": r.id_estado,
        "prioridad_asignada": str(r.prioridad_asignada) if r.prioridad_asignada else None,
        "imagen_url": r.imagen_url,
        "taza_o_orinal": str(r.taza_or_orinal) if getattr(r, "taza_or_orinal", None) else None,
        "pasillo": str(r.pasillo) if getattr(r, "pasillo", None) else None,
        "tipo_reporte": str(r.tipo_reporte) if getattr(r, "tipo_reporte", None) else None,
        "edificio": r.edificio,
        "sexo": str(r.sexo) if getattr(r, "sexo", None) else None
    }


# ----------------------------------------------------------------
# ACTUALIZAR ESTADO
# ----------------------------------------------------------------
@router.put("/reportes/{id_reporte}/estado")
def actualizar_estado_reporte(id_reporte: int, body: EstadoUpdate, db: Session = Depends(get_db)):
    reporte = db.query(Reporte).filter(Reporte.id_reporte == id_reporte).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    admin = db.query(Admin).filter(Admin.id_admin == body.id_admin).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")

    anterior = reporte.id_estado
    nuevo = body.id_estado

    reporte.id_estado = nuevo
    db.commit()

    sql = text(
        """
        INSERT INTO historial_reportes 
        (id_reporte, id_admin, campo_modificado, valor_anterior, valor_nuevo, fecha_cambio)
        VALUES (:id_reporte, :id_admin, :campo, :val_ant, :val_new, :fecha)
        """
    )

    db.execute(sql, {
        "id_reporte": id_reporte,
        "id_admin": body.id_admin,
        "campo": "id_estado",
        "val_ant": str(anterior),
        "val_new": str(nuevo),
        "fecha": datetime.utcnow()
    })
    db.commit()

    return {"mensaje": "Estado actualizado", "id_reporte": id_reporte, "id_estado": nuevo}


# ----------------------------------------------------------------
# ACTUALIZAR PRIORIDAD
# ----------------------------------------------------------------
@router.put("/reportes/{id_reporte}/prioridad")
def actualizar_prioridad_reporte(id_reporte: int, body: PrioridadUpdate, db: Session = Depends(get_db)):
    if body.prioridad_asignada not in ("alta", "media", "baja"):
        raise HTTPException(status_code=400, detail="Prioridad inválida")

    reporte = db.query(Reporte).filter(Reporte.id_reporte == id_reporte).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    admin = db.query(Admin).filter(Admin.id_admin == body.id_admin).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")

    anterior = reporte.prioridad_asignada
    nuevo = body.prioridad_asignada

    reporte.prioridad_asignada = nuevo
    db.commit()

    sql = text(
        """
        INSERT INTO historial_reportes 
        (id_reporte, id_admin, campo_modificado, valor_anterior, valor_nuevo, fecha_cambio)
        VALUES (:id_reporte, :id_admin, :campo, :val_ant, :val_new, :fecha)
        """
    )

    db.execute(sql, {
        "id_reporte": id_reporte,
        "id_admin": body.id_admin,
        "campo": "prioridad_asignada",
        "val_ant": anterior,
        "val_new": nuevo,
        "fecha": datetime.utcnow()
    })
    db.commit()

    return {"mensaje": "Prioridad actualizada", "id_reporte": id_reporte, "prioridad_asignada": nuevo}


# ----------------------------------------------------------------
# HISTORIAL
# ----------------------------------------------------------------
@router.get("/reportes/{id_reporte}/historial", response_model=List[dict])
def obtener_historial(id_reporte: int, db: Session = Depends(get_db)):
    sql = text(
        """
        SELECT id_historial, id_reporte, id_admin, campo_modificado, 
               valor_anterior, valor_nuevo, fecha_cambio
        FROM historial_reportes 
        WHERE id_reporte = :id_reporte
        ORDER BY fecha_cambio DESC
        """
    )

    res = db.execute(sql, {"id_reporte": id_reporte}).fetchall()

    return [
        {
            "id_historial": row["id_historial"],
            "id_reporte": row["id_reporte"],
            "id_admin": row["id_admin"],
            "campo_modificado": row["campo_modificado"],
            "valor_anterior": row["valor_anterior"],
            "valor_nuevo": row["valor_nuevo"],
            "fecha_cambio": row["fecha_cambio"],
        }
        for row in res
    ]
