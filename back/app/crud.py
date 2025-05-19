# app/crud.py
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
    if not usuario:
        return None
    if not verificar_contrasena(contrasena, usuario.contrasena):
        return None
    return usuario

def calcular_nomina(horas_trabajadas: int, dias_incapacidad: int, horas_extra: int, bonificacion: float):
    salario_horas = horas_trabajadas * 20000
    salario_incapacidad = dias_incapacidad * 60000
    salario_extra = horas_extra * 30000
    salario_bruto = salario_horas + salario_incapacidad + salario_extra + bonificacion
    salud = salario_bruto * 0.04
    pension = salario_bruto * 0.04
    salario_neto = salario_bruto - salud - pension
    return salario_bruto, salud, pension, salario_neto

def crear_nomina(db: Session, usuario_id: int, horas_trabajadas: int, dias_incapacidad: int,
                 horas_extra: int, bonificacion: float, periodo_pago: str):
    salario_bruto, salud, pension, salario_neto = calcular_nomina(
        horas_trabajadas, dias_incapacidad, horas_extra, bonificacion
    )

    nomina = models.Nomina(
        usuario_id=usuario_id,
        horas_trabajadas=horas_trabajadas,
        dias_incapacidad=dias_incapacidad,
        horas_extra=horas_extra,
        bonificacion=bonificacion,
        periodo_pago=periodo_pago,
        salario_bruto=salario_bruto,
        salud=salud,
        pension=pension,
        salario_neto=salario_neto
    )
    db.add(nomina)
    db.commit()
    db.refresh(nomina)
    return nomina