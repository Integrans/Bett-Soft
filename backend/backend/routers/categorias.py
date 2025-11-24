from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import CategoriaIncidente
from schemas.categorias_schema import CategoriaResponse

router = APIRouter(prefix="/categorias", tags=["Categorías"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[CategoriaResponse])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(CategoriaIncidente).all()
