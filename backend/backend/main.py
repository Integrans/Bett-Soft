from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Base, engine
from routers import reportes, admin

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BettSoft API",
    description="API para reportes de baños en la FES Acatlán",
    version="1.0.0"
)

# ----------------------------
# CONFIGURAR CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠ En producción se usa dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# INCLUIR ROUTERS
# ----------------------------
app.include_router(reportes.router)
app.include_router(admin.router)

# ----------------------------
# RUTA DE PRUEBA
# ----------------------------
@app.get("/")
def root():
    return {"mensaje": "API BettSoft funcionando correctamente"}
