from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

<<<<<<< HEAD
load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_PORT =os.getenv("DB_PORT", "3306")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "bett_soft_bd")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Crear el engine
engine = create_engine(
    DATABASE_URL,
    echo=False,       
    pool_pre_ping=True
)

# Sesiones de DB
=======
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = "mysql+pymysql://root:@localhost:3306/bett_soft_db"

engine = create_engine(DATABASE_URL)

>>>>>>> origin/dev
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

<<<<<<< HEAD
# Dependencia para obtener la sesión de DB
=======
>>>>>>> origin/dev
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()