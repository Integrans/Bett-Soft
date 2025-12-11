from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import Bano
from schemas.banos_schema import BanoResponse

router = APIRouter(prefix="/banos", tags=["Baños"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------
# GET: /banos
# --------------------------------------------
@router.get("/", response_model=list[BanoResponse])
def obtener_banos(db: Session = Depends(get_db)):
    return db.query(Bano).all()
