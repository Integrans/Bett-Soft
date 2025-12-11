from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database.connection import Base, engine, SessionLocal
from routers import reportes, admin, banos, categorias
from schemas.admin_schema import AdminLogin, AdminResponse
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

# =============================
# ENDPOINT DE LOGIN (raíz)
# =============================
@app.post("/login", response_model=AdminResponse)
def login(data: AdminLogin, db = Depends(lambda: SessionLocal())):
    """
    Endpoint de login que redirige al login del admin.
    Permite que el frontend llame a /login sin prefix.
    """
    from routers.admin import login_admin
    return login_admin(data, db)

# Routers
app.include_router(reportes.router)
app.include_router(admin.router)
app.include_router(banos.router)
app.include_router(categorias.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
