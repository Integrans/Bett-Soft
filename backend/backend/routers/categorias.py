from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import Categoria  # <-- usar la clase correcta
from schemas.categorias_schema import CategoriaResponse

router = APIRouter(prefix="/categorias", tags=["Categorías"])

# ------------------------------------------------------------
# Función para obtener DB
# ------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------------------------------------
# Endpoint: obtener todas las categorías
# ------------------------------------------------------------
@router.get("/", response_model=list[CategoriaResponse])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()  # <-- Cambiado

# ------------------------------------------------------------
# Endpoint alternativo: listar categorías (sin response_model)
# ------------------------------------------------------------
@router.get("/categorias")
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()  # <-- Cambiado
