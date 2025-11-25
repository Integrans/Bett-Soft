from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# --- LÓGICA DE CONEXIÓN INTELIGENTE ---

# 1. Primero preguntamos: "¿Docker me dio una dirección completa?"
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Si Docker no dijo nada (es None), asumimos que estamos en tu PC Local
if not DATABASE_URL:
    # Esta es tu conexión local de siempre (XAMPP/Workbench)
    DATABASE_URL = "mysql+pymysql://root:@localhost:3306/bett_soft_db"

# --------------------------------------

# Creamos el motor con la URL que haya ganado (Docker o Local)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# La función para que las rutas usen la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()