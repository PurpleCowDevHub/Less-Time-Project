from sqlalchemy.orm import Session
from . import models
from .security import hashear_contrasena, verificar_contrasena

def crear_usuario(db: Session, correo: str, contrasena: str, empresa: str):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if usuario_existente:
        return None
    hashed_pw = hashear_contrasena(contrasena)
    nuevo_usuario = models.Usuario(correo=correo, contrasena=hashed_pw, empresa=empresa)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def autenticar_usuario(db: Session, correo: str, contrasena: str):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if not usuario or not verificar_contrasena(contrasena, usuario.contrasena):
        return None
    return usuario

def crear_nomina(db: Session, usuario_id: int, horas_trabajadas: float, dias_incapacidad: int,
                 horas_extra: float, bonificacion: float, periodo_pago: str):
    valor_hora = 20000
    valor_incapacidad = 60000
    valor_hora_extra = 30000
    aporte_salud = 0.04
    aporte_pension = 0.04

    salario_base = horas_trabajadas * valor_hora
    incapacidad = dias_incapacidad * valor_incapacidad
    overtime = horas_extra * valor_hora_extra

    bruto = salario_base + incapacidad + overtime + bonificacion
    descuentos = bruto * (aporte_salud + aporte_pension)
    total = bruto - descuentos

    nomina = models.Nomina(
        usuario_id=usuario_id,
        horas_trabajadas=horas_trabajadas,
        dias_incapacidad=dias_incapacidad,
        horas_extra=horas_extra,
        bonificacion=bonificacion,
        periodo_pago=periodo_pago,
        total=total
    )
    db.add(nomina)
    db.commit()
    db.refresh(nomina)
    return nomina

def obtener_usuarios(db: Session):
    return db.query(models.Usuario).all()