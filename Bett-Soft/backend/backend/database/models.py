from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

# ============================
# MODELO: Admin
# ============================
class Admin(Base):
    __tablename__ = "admins"

    id_admin = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    historial = relationship("HistorialReporte", back_populates="admin")


# ============================
# MODELO: Categorias
# ============================
class CategoriaIncidente(Base):
    __tablename__ = "categorias_incidente"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(200))
    prioridad_default = Column(Enum("alta", "media", "baja"), nullable=False)


# ============================
# MODELO: Baños
# ============================
class Bano(Base):
    __tablename__ = "banos"

    id_bano = Column(Integer, primary_key=True, index=True)
    edificio = Column(String(50), nullable=False)
    nivel = Column(Integer, nullable=False)
    sexo = Column(Enum("H", "M", "Mixto"), nullable=False)
    tiene_orinal = Column(Integer, default=0)
    tiene_taza = Column(Integer, default=1)


# ============================
# MODELO: Estados
# ============================
class EstadoReporte(Base):
    __tablename__ = "estados_reporte"

    id_estado = Column(Integer, primary_key=True, index=True)
    nombre = Column(Enum("en_proceso", "resuelto", "descartado"), nullable=False)


# ============================
# MODELO: Reportes
# ============================
class Reporte(Base):
    __tablename__ = "reportes"

    id_reporte = Column(Integer, primary_key=True, index=True)
    folio = Column(String(20), unique=True, nullable=False)
    numero_cuenta = Column(String(50), nullable=False)

    id_bano = Column(Integer, ForeignKey("banos.id_bano"), nullable=False)
    id_categoria = Column(Integer, ForeignKey("categorias_incidente.id_categoria"), nullable=False)
    id_estado = Column(Integer, ForeignKey("estados_reporte.id_estado"), nullable=False, default=1)

    fecha_creacion = Column(DateTime)
    prioridad_asignada = Column(Enum("alta", "media", "baja"), nullable=False)
    imagen_url = Column(String(300))
    taza_o_orinal = Column(Enum("taza", "orinal"), nullable=False)
    pasillo = Column(Enum("frente", "atras"), nullable=False)
    tipo_reporte = Column(Enum("fuga","taza_tapada","orinal_tapado","no_papel","no_jabon","suciedad","mal_olor"), nullable=False)

    edificio = Column(String(50), nullable=False)
    sexo = Column(Enum("H","M","Mixto"), nullable=False)


# ============================
# MODELO: Historial
# ============================
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
