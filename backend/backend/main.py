from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Base, engine
from routers import reportes, admin
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from sqlalchemy.exc import IntegrityError
from database.models import (Bano, Reporte, SexoEnum, TipoReporteEnum, PrioridadEnum, EstadoReporteEnum, Categoria, EstadoReporte, HistorialReporte, Admin, EstadoReporte, PasilloEnum)

Base.metadata.create_all(bind=engine)

from database.models import (
    Categoria, 
    EstadoReporte, 
    Bano,
    Reporte,
    PrioridadEnum, 
    SexoEnum, 
    EstadoReporteEnum,
    TipoReporteEnum,
    HistorialReporte,
    Admin,
    PasilloEnum,
    EstadoReporte
)

def poblar_datos_iniciales():
    db = SessionLocal()
    try:
        print("🌱 Iniciando carga de datos...")

        estados_data = [
            (1, EstadoReporteEnum.en_proceso),
            (2, EstadoReporteEnum.resuelto),
            (3, EstadoReporteEnum.descartado)
        ]

        for id_est, enum_val in estados_data:
            exists = db.query(EstadoReporte).filter_by(id_estado=id_est).first()
            if not exists:
                db.add(EstadoReporte(id_estado=id_est, nombre=enum_val))

        categorias_data = [
            (1, 'fuga', 'Fuga de agua o tuberías', PrioridadEnum.alta),
            (2, 'taza_tapada', 'Taza de baño tapada', PrioridadEnum.alta),
            (3, 'orinal_tapado', 'Orinal tapado', PrioridadEnum.alta),
            (4, 'no_papel', 'No hay papel en dispensador', PrioridadEnum.media),
            (5, 'no_jabon', 'No hay jabón en dispensador', PrioridadEnum.media),
            (6, 'suciedad', 'Sanitario o área sucia', PrioridadEnum.baja),
            (7, 'mal_olor', 'Presencia de malos olores', PrioridadEnum.baja)
        ]

        for id_cat, nom, desc, prio in categorias_data:
            exists = db.query(Categoria).filter_by(id_categoria=id_cat).first()
            if not exists:
                db.add(Categoria(
                    id_categoria=id_cat, 
                    nombre=nom, 
                    descripcion=desc, 
                    prioridad_default=prio
                ))

        banos_data = [
            (1,'A-1',1, SexoEnum.M, 0,1), (2,'A-1',2, SexoEnum.H, 1,1),
            (3,'A-2',1, SexoEnum.M, 0,1), (4,'A-2',2, SexoEnum.H, 1,1),
            (5,'A-3',1, SexoEnum.M, 0,1), (6,'A-3',2, SexoEnum.H, 1,1),
            (7,'A-4',1, SexoEnum.M, 0,1), (8,'A-4',2, SexoEnum.H, 1,1),
            (9,'A-5',1, SexoEnum.M, 0,1), (10,'A-5',2, SexoEnum.H, 1,1),
            (11,'A-6',1, SexoEnum.M, 0,1), (12,'A-6',2, SexoEnum.H, 1,1),
            (13,'A-7',1, SexoEnum.M, 0,1), (14,'A-7',2, SexoEnum.Mixto, 0,1),
            (15,'A-8',1, SexoEnum.M, 0,1), (16,'A-8',2, SexoEnum.H, 1,1),
            (17,'A-9',1, SexoEnum.M, 0,1), (18,'A-9',2, SexoEnum.H, 1,1),
            (19,'A-10',1, SexoEnum.M, 0,1), (20,'A-10',2, SexoEnum.H, 1,1),
            (21,'A-11',1, SexoEnum.M, 0,1), (22,'A-11',2, SexoEnum.H, 1,1),
            (23,'A-12',1, SexoEnum.M, 0,1), (24,'A-12',2, SexoEnum.H, 1,1),
            (25,'A-13',1, SexoEnum.M, 0,1), (26,'A-13',2, SexoEnum.H, 1,1),
            (27,'A-14',1, SexoEnum.M, 0,1), (28,'A-14',2, SexoEnum.H, 1,1),
            (29,'A-15',1, SexoEnum.M, 0,1), (30,'A-15',1, SexoEnum.H, 1,1),
            (31,'A-15',2, SexoEnum.M, 0,1), (32,'A-15',2, SexoEnum.H, 1,1)
        ]

        for id_b, edif, niv, sex, orinal, taza in banos_data:
            exists = db.query(Bano).filter_by(id_bano=id_b).first()
            if not exists:
                db.add(Bano(
                    id_bano=id_b,
                    edificio=edif,
                    nivel=niv,
                    sexo=sex,
                    tiene_orinal=orinal,
                    tiene_taza=taza
                ))

        db.commit()
        print("✅ Base de datos poblada exitosamente.")
        
    except Exception as e:
        print(f"⚠️ Error poblando datos: {e}")
        db.rollback()
    finally:
        db.close()

poblar_datos_iniciales()

app = FastAPI(
    title="BettSoft API",
    description="API para reportes de baños en la FES Acatlán",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(reportes.router)
app.include_router(admin.router, prefix="/admin")


@app.get("/")
def root():
    return {"mensaje": "API BettSoft funcionando correctamente"}


