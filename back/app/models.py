# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String(255), unique=True, index=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    empresa = Column(String(255), nullable=False)

class Nomina(Base):
    __tablename__ = "nominas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    horas_trabajadas = Column(Float)
    dias_incapacidad = Column(Integer)
    horas_extra = Column(Float)
    bonificacion = Column(Float)
    periodo_pago = Column(String(50))
    total = Column(Float)