from datetime import datetime
from sqlalchemy.orm import Session
from database.models import Reporte

def generar_folio(db: Session):
    fecha = datetime.now().strftime("%Y%m%d")

    
    count = db.query(Reporte).filter(
        Reporte.folio.like(f"INC-{fecha}-%")
    ).count()

    consecutivo = str(count + 1).zfill(4) 

    folio = f"INC-{fecha}-{consecutivo}"
    return folio
