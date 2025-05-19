# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from .database import Base
from datetime import date

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
    horas_trabajadas = Column(Integer, nullable=False)
    dias_incapacidad = Column(Integer, nullable=False)
    horas_extra = Column(Integer, nullable=False)
    bonificacion = Column(Float, default=0.0)
    periodo_pago = Column(String(50), nullable=False)

    salario_bruto = Column(Float, nullable=False)
    salud = Column(Float, nullable=False)
    pension = Column(Float, nullable=False)
    salario_neto = Column(Float, nullable=False)
    fecha_pago = Column(Date, default=date.today)   