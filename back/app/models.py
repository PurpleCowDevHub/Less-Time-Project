# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Date
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String(255), unique=True, index=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    empresa = Column(String(255), nullable=False)
    es_admin = Column(Boolean, default=False)
    fecha_nacimiento = Column(Date, nullable=True)  # Nuevo campo para edad

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

class HorarioSemanal(Base):
    __tablename__ = "horarios_semanales"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    dia_semana = Column(String(10), nullable=False)  # Ej: 'Lunes', 'Martes', ...
    hora_entrada = Column(String(5))  # Ej: '08:00'
    hora_salida = Column(String(5))   # Ej: '17:00'
    observacion = Column(String(255), nullable=True)
    fecha = Column(Date, nullable=True)  # Opcional para semana específica
