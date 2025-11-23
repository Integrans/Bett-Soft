from datetime import datetime
from sqlalchemy.orm import Session
from database.models import Reporte

def generar_folio(db: Session):
    # Formato: INC-YYYYMMDD-0001
    fecha = datetime.now().strftime("%Y%m%d")

    # Contar reportes del día
    count = db.query(Reporte).filter(
        Reporte.folio.like(f"INC-{fecha}-%")
    ).count()

    consecutivo = str(count + 1).zfill(4)  # 0001, 0002...

    folio = f"INC-{fecha}-{consecutivo}"
    return folio
