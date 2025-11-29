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

<<<<<<< HEAD

# ---------- LOGIN ----------
class AdminLogin(BaseModel):
    email: str
    password: str
=======
@router.post("/registro", response_model=AdminResponse)
def registrar_admin(data: AdminCreate, db: Session = Depends(get_db)):
    existe = db.query(Admin).filter(Admin.email == data.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
>>>>>>> origin/dev

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


<<<<<<< HEAD
# ---------- SERIALIZADOR ----------
def reporte_a_dict(r: models.Reporte) -> dict:
    return {
=======
@router.post("/login", response_model=AdminResponse)
def login_admin(data: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == data.email).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")

    if not verify_password(data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {"mensaje": "Login exitoso"}


class EstadoUpdate(BaseModel):
    id_admin: int
    id_estado: int


class PrioridadUpdate(BaseModel):
    id_admin: int
    prioridad_asignada: str

@router.get("/reportes", response_model=List[dict])
def listar_reportes(
    estado: Optional[int] = Query(None, description="Filtrar por id_estado"),
    edificio: Optional[str] = Query(None, description="Filtrar por edificio (ej. A-4)"),
    tipo_reporte: Optional[str] = Query(None, description="Filtrar por tipo de reporte"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Listar reportes con filtros opcionales (estado, edificio, tipo_reporte).
    """
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
            "prioridad_asignada": str(r.prioridad_asignada) if r.prioridad_asignada is not None else None,
            "imagen_url": r.imagen_url,
            "taza_o_orinal": str(r.taza_or_orinal) if getattr(r, "taza_or_orinal", None) is not None else None,
            "pasillo": str(r.pasillo) if getattr(r, "pasillo", None) is not None else None,
            "tipo_reporte": str(r.tipo_reporte) if getattr(r, "tipo_reporte", None) is not None else None,
            "edificio": r.edificio,
            "sexo": str(r.sexo) if getattr(r, "sexo", None) is not None else None
        })

    return {"total": total, "offset": offset, "limit": limit, "reportes": results}


@router.get("/reportes/{folio}", response_model=dict)
def obtener_reporte_por_folio(folio: str, db: Session = Depends(get_db)):
    """
    Obtener un reporte por su folio.
    """
    r = db.query(Reporte).filter(Reporte.folio == folio).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    result = {
>>>>>>> origin/dev
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

<<<<<<< HEAD
    reporte.id_estado = nuevo_estado
=======
    admin = db.query(Admin).filter(Admin.id_admin == body.id_admin).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")

    anterior = reporte.id_estado
    nuevo = body.id_estado

    reporte.id_estado = nuevo
    db.add(reporte)
>>>>>>> origin/dev
    db.commit()
    db.refresh(reporte)

<<<<<<< HEAD
    return {"mensaje": "Estado actualizado correctamente"}
=======
    sql = text(
        "INSERT INTO historial_reportes (id_reporte, id_admin, campo_modificado, valor_anterior, valor_nuevo, fecha_cambio) "
        "VALUES (:id_reporte, :id_admin, :campo, :val_ant, :val_new, :fecha)"
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


@router.put("/reportes/{id_reporte}/prioridad")
def actualizar_prioridad_reporte(id_reporte: int, body: PrioridadUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la prioridad de un reporte y guarda un registro en historial_reportes.
    body: { "id_admin": 1, "prioridad_asignada": "alta" }
    """
    if body.prioridad_asignada not in ("alta", "media", "baja"):
        raise HTTPException(status_code=400, detail="Prioridad inválida")

    reporte = db.query(Reporte).filter(Reporte.id_reporte == id_reporte).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    admin = db.query(Admin).filter(Admin.id_admin == body.id_admin).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")

    anterior = str(reporte.prioridad_asignada) if reporte.prioridad_asignada is not None else None
    nuevo = body.prioridad_asignada

    reporte.prioridad_asignada = nuevo
    db.add(reporte)
    db.commit()

    sql = text(
        "INSERT INTO historial_reportes (id_reporte, id_admin, campo_modificado, valor_anterior, valor_nuevo, fecha_cambio) "
        "VALUES (:id_reporte, :id_admin, :campo, :val_ant, :val_new, :fecha)"
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


@router.get("/reportes/{id_reporte}/historial", response_model=List[dict])
def obtener_historial(id_reporte: int, db: Session = Depends(get_db)):
    """
    Devuelve el historial de cambios para un reporte.
    """
    sql = text(
        "SELECT id_historial, id_reporte, id_admin, campo_modificado, valor_anterior, valor_nuevo, fecha_cambio "
        "FROM historial_reportes WHERE id_reporte = :id_reporte ORDER BY fecha_cambio DESC"
    )
    res = db.execute(sql, {"id_reporte": id_reporte}).fetchall()
    historial = []
    for row in res:
        historial.append({
            "id_historial": row["id_historial"],
            "id_reporte": row["id_reporte"],
            "id_admin": row["id_admin"],
            "campo_modificado": row["campo_modificado"],
            "valor_anterior": row["valor_anterior"],
            "valor_nuevo": row["valor_nuevo"],
            "fecha_cambio": row["fecha_cambio"]
        })

    return historial
>>>>>>> origin/dev
