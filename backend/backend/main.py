from fastapi import FastAPI
from database.connection import engine, Base
from routers import estados
from routers import reportes, categorias, banos, admin

app = FastAPI()

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(reportes.router)
app.include_router(categorias.router)
app.include_router(banos.router)
app.include_router(admin.router)
app.include_router(estados.router)
