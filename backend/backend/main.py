from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database.connection import Base, engine
from routers import reportes, admin, banos, categorias
import os

# Crear carpeta de uploads
os.makedirs("uploads", exist_ok=True)

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BettSoft API",
    description="API para reportes de baños en la FES Acatlán",
    version="1.0.0"
)

# 🔥 SERVIR ARCHIVOS ESTÁTICOS (IMÁGENES)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"mensaje": "API BettSoft funcionando correctamente"}

# Routers
app.include_router(reportes.router)
app.include_router(admin.router)
app.include_router(banos.router)
app.include_router(categorias.router)
