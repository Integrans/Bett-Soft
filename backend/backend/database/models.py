from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .connection import Base

class Bano(Base):
    __tablename__ = "banos"

    id_bano = Column(Integer, primary_key=True, index=True)
    edificio = Column(String(50))
    nivel = Column(String(20))
    numero = Column(Integer)
    sexo = Column(Enum("H", "M", "Mixto"))

    reportes = relationship("Reporte", back_populates="bano")


class CategoriaIncidente(Base):
    __tablename__ = "categorias_incidente"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    descripcion = Column(String(200))
    prioridad_default = Column(Enum("alta", "media", "baja"))

    reportes = relationship("Reporte", back_populates="categoria")


class EstadoReporte(Base):
    __tablename__ = "estados_reporte"

    id_estado = Column(Integer, primary_key=True, index=True)
    nombre = Column(Enum("en_proceso", "resuelto", "descartado"))

    reportes = relationship("Reporte", back_populates="estado")


class Reporte(Base):
    __tablename__ = "reportes"

    id_reporte = Column(Integer, primary_key=True, index=True)
    folio = Column(String(20), unique=True, index=True)
    id_bano = Column(Integer, ForeignKey("banos.id_bano"))
    id_categoria = Column(Integer, ForeignKey("categorias_incidente.id_categoria"))
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.now)
    id_estado = Column(Integer, ForeignKey("estados_reporte.id_estado"))
    prioridad_asignada = Column(Enum("alta", "media", "baja"))
    imagen_url = Column(String(300))

    bano = relationship("Bano", back_populates="reportes")
    categoria = relationship("CategoriaIncidente", back_populates="reportes")
    estado = relationship("EstadoReporte", back_populates="reportes")
