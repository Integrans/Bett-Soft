from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import CategoriaIncidente
from schemas.categoria_schema import CategoriaCreate, CategoriaUpdate, CategoriaResponse

router = APIRouter(prefix="/categorias", tags=["Categorias"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Crear categoría
# -------------------------
@router.post("/", response_model=CategoriaResponse)
def crear_categoria(data: CategoriaCreate, db: Session = Depends(get_db)):

    categoria = CategoriaIncidente(
        nombre=data.nombre,
        descripcion=data.descripcion,
        prioridad_default=data.prioridad_default
    )

    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    return categoria


# -------------------------
# Listar categorías
# -------------------------
@router.get("/", response_model=list[CategoriaResponse])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(CategoriaIncidente).all()


# -------------------------
# Obtener por ID
# -------------------------
@router.get("/{id_categoria}", response_model=CategoriaResponse)
def obtener_categoria(id_categoria: int, db: Session = Depends(get_db)):

    categoria = db.query(CategoriaIncidente).filter(
        CategoriaIncidente.id_categoria == id_categoria
    ).first()

    if not categoria:
        return {"error": "La categoría no existe"}

    return categoria


# -------------------------
# Actualizar categoría
# -------------------------
@router.put("/{id_categoria}", response_model=CategoriaResponse)
def actualizar_categoria(id_categoria: int, data: CategoriaUpdate, db: Session = Depends(get_db)):

    categoria = db.query(CategoriaIncidente).filter(
        CategoriaIncidente.id_categoria == id_categoria
    ).first()

    if not categoria:
        return {"error": "La categoría no existe"}

    categoria.nombre = data.nombre
    categoria.descripcion = data.descripcion
    categoria.prioridad_default = data.prioridad_default

    db.commit()
    db.refresh(categoria)

    return categoria


# -------------------------
# Eliminar categoría
# -------------------------
@router.delete("/{id_categoria}")
def eliminar_categoria(id_categoria: int, db: Session = Depends(get_db)):

    categoria = db.query(CategoriaIncidente).filter(
        CategoriaIncidente.id_categoria == id_categoria
    ).first()

    if not categoria:
        return {"error": "La categoría no existe"}

    db.delete(categoria)
    db.commit()

    return {"mensaje": "Categoría eliminada correctamente"}
