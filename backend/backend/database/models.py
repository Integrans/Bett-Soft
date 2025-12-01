from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base
from enum import Enum as PyEnum   # <<--- ¡IMPORTANTE!


# =======================================================
# ENUMS PARA EL SISTEMA
# =======================================================

class PrioridadEnum(PyEnum):
    alta = "alta"
    media = "media"
    baja = "baja"


class SexoEnum(PyEnum):
    H = "H"
    M = "M"
    Mixto = "Mixto"


class TazaOrinalEnum(PyEnum):
    taza = "taza"
    orinal = "orinal"


class PasilloEnum(PyEnum):
    frente = "frente"
    atras = "atras"


class TipoReporteEnum(PyEnum):
    fuga = "fuga"
    taza_tapada = "taza_tapada"
    orinal_tapado = "orinal_tapado"
    no_papel = "no_papel"
    no_jabon = "no_jabon"
    suciedad = "suciedad"
    mal_olor = "mal_olor"


class EstadoEnum(PyEnum):
    pendiente = "pendiente"
    en_proceso = "en_proceso"
    resuelto = "resuelto"
    descartado = "descartado"


# =======================================================
# MODELO: Admin
# =======================================================

class Admin(Base):
    __tablename__ = "admins"

    id_admin = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    historial = relationship("HistorialReporte", back_populates="admin")


# =======================================================
# MODELO: Categorías
# =======================================================

class CategoriaIncidente(Base):
    __tablename__ = "categorias_incidente"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(200))
    prioridad_default = Column(Enum(PrioridadEnum), nullable=False)


# =======================================================
# MODELO: Baños
# =======================================================

class Bano(Base):
    __tablename__ = "banos"

    id_bano = Column(Integer, primary_key=True, index=True)
    edificio = Column(String(50), nullable=False)
    nivel = Column(Integer, nullable=False)
    sexo = Column(Enum(SexoEnum), nullable=False)
    tiene_orinal = Column(Integer, default=0)
    tiene_taza = Column(Integer, default=1)


# =======================================================
# MODELO: Estados del reporte
# =======================================================

class EstadoReporte(Base):
    __tablename__ = "estados_reporte"

    id_estado = Column(Integer, primary_key=True, index=True)
    nombre = Column(Enum(EstadoEnum), nullable=False)


# =======================================================
# MODELO: Reportes
# =======================================================

class Reporte(Base):
    __tablename__ = "reportes"

    id_reporte = Column(Integer, primary_key=True, index=True)
    folio = Column(String(20), unique=True, nullable=False)
    numero_cuenta = Column(String(50), nullable=False)

    id_bano = Column(Integer, ForeignKey("banos.id_bano"), nullable=False)
    id_categoria = Column(Integer, ForeignKey("categorias_incidente.id_categoria"), nullable=False)
    id_estado = Column(Integer, ForeignKey("estados_reporte.id_estado"), nullable=False, default=1)

    fecha_creacion = Column(DateTime, nullable=False)

    prioridad_asignada = Column(Enum(PrioridadEnum), nullable=False)

    imagen_url = Column(String(300))

    taza_o_orinal = Column(Enum(TazaOrinalEnum), nullable=True)
    pasillo = Column(Enum(PasilloEnum), nullable=True)

    tipo_reporte = Column(Enum(TipoReporteEnum), nullable=False)

    edificio = Column(String(50), nullable=False)
    sexo = Column(Enum(SexoEnum), nullable=False)


# =======================================================
# MODELO: Historial
# =======================================================

class HistorialReporte(Base):
    __tablename__ = "historial_reportes"

    id_historial = Column(Integer, primary_key=True, index=True)
    id_reporte = Column(Integer, ForeignKey("reportes.id_reporte"), nullable=False)
    id_admin = Column(Integer, ForeignKey("admins.id_admin"), nullable=False)

    campo_modificado = Column(String(50), nullable=False)
    valor_anterior = Column(String(100))
    valor_nuevo = Column(String(100))
    fecha_cambio = Column(DateTime)

    reporte = relationship("Reporte")
    admin = relationship("Admin", back_populates="historial")
