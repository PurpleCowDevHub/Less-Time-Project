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
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    horas_trabajadas = Column(Float, nullable=False)
    dias_incapacidad = Column(Integer, nullable=False)
    horas_extra = Column(Float, nullable=False)
    bonificacion = Column(Float, nullable=True)
    periodo_pago = Column(String(255), nullable=False)
    total = Column(Float, nullable=False)