from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.connection import Base
import enum

# ---------------------------------------------------------
# ENUMS
# ---------------------------------------------------------

class SexoEnum(enum.Enum):
    H = "H"
    M = "M"
    Mixto = "Mixto"

class PasilloEnum(enum.Enum):
    frente = "frente"
    atras = "atras"

class TazaOrinalEnum(enum.Enum):
    taza = "taza"
    orinal = "orinal"

class TipoReporteEnum(enum.Enum):
    fuga = "fuga"
    taza_tapada = "taza_tapada"
    orinal_tapado = "orinal_tapado"
    no_papel = "no_papel"
    no_jabon = "no_jabon"
    suciedad = "suciedad"
    mal_olor = "mal_olor"

class PrioridadEnum(enum.Enum):
    alta = "alta"
    media = "media"
    baja = "baja"

class EstadoReporteEnum(enum.Enum):
    en_proceso = "en_proceso"
    resuelto = "resuelto"
    descartado = "descartado"

# ---------------------------------------------------------
# TABLA: BANOS
# ---------------------------------------------------------

class Bano(Base):
    __tablename__ = "banos"

    id_bano = Column(Integer, primary_key=True, index=True)
    edificio = Column(String(50), nullable=False)
    nivel = Column(Integer, nullable=False)
    sexo = Column(Enum(SexoEnum), nullable=False)
    tiene_orinal = Column(Integer, default=0)
    tiene_taza = Column(Integer, default=1)

    reportes = relationship("Reporte", back_populates="bano")

# ---------------------------------------------------------
# TABLA: CATEGORIAS INCIDENTE
# ---------------------------------------------------------

class Categoria(Base):
    __tablename__ = "categorias_incidente"

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)  # ✅ longitud definida
    descripcion = Column(String(200))
    prioridad_default = Column(Enum(PrioridadEnum), nullable=False)

    reportes = relationship("Reporte", back_populates="categoria")

# ---------------------------------------------------------
# TABLA: ESTADOS REPORTE
# ---------------------------------------------------------

class EstadoReporte(Base):
    __tablename__ = "estados_reporte"

    id_estado = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum(EstadoReporteEnum), nullable=False)

    reportes = relationship("Reporte", back_populates="estado")

# ---------------------------------------------------------
# TABLA: ADMINS
# ---------------------------------------------------------

class Admin(Base):
    __tablename__ = "admins"

    id_admin = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

# ---------------------------------------------------------
# TABLA: REPORTES
# ---------------------------------------------------------

class Reporte(Base):
    __tablename__ = "reportes"

    id_reporte = Column(Integer, primary_key=True, autoincrement=True)
    folio = Column(String(20), unique=True, nullable=False)
    numero_cuenta = Column(String(50), nullable=False)

    id_bano = Column(Integer, ForeignKey("banos.id_bano"), nullable=False)
    id_categoria = Column(Integer, ForeignKey("categorias_incidente.id_categoria"), nullable=False)
    id_estado = Column(Integer, ForeignKey("estados_reporte.id_estado"), nullable=False, default=1)

    fecha_creacion = Column(DateTime)
    prioridad_asignada = Column(Enum(PrioridadEnum), nullable=False)
    imagen_url = Column(String(300))

    taza_or_orinal = Column(Enum(TazaOrinalEnum), nullable=False)
    pasillo = Column(Enum(PasilloEnum), nullable=False)
    tipo_reporte = Column(Enum(TipoReporteEnum), nullable=False)

    bano = relationship("Bano", back_populates="reportes")
    categoria = relationship("Categoria", back_populates="reportes")
    estado = relationship("EstadoReporte", back_populates="reportes")
