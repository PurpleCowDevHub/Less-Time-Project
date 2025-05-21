# app/crud.py
from sqlalchemy.orm import Session
from . import models
from .security import hashear_contrasena, verificar_contrasena
from datetime import datetime

def crear_usuario(db: Session, correo: str, contrasena: str, empresa: str, es_admin: bool = False):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if usuario_existente:
        return None
    hashed_pw = hashear_contrasena(contrasena)
    nuevo_usuario = models.Usuario(correo=correo, contrasena=hashed_pw, empresa=empresa, es_admin=es_admin)
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
    descuento_salud = bruto * aporte_salud
    descuento_pension = bruto * aporte_pension
    total = bruto - descuento_salud - descuento_pension

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

    return {
        "usuario_id": usuario_id,
        "salario_bruto": bruto,
        "descuento_salud": descuento_salud,
        "descuento_pension": descuento_pension,
        "salario_neto": total,
        "periodo_pago": periodo_pago
    }

def crear_o_actualizar_horario(db: Session, usuario_id: int, dia_semana: str,
                               hora_entrada: str = None, hora_salida: str = None,
                               observacion: str = None, fecha: str = None):
    query = db.query(models.HorarioSemanal).filter(
        models.HorarioSemanal.usuario_id == usuario_id,
        models.HorarioSemanal.dia_semana == dia_semana
    )
    if fecha:
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
        query = query.filter(models.HorarioSemanal.fecha == fecha_dt)
    horario = query.first()

    if horario:
        horario.hora_entrada = hora_entrada
        horario.hora_salida = hora_salida
        horario.observacion = observacion
        if fecha:
            horario.fecha = fecha_dt
    else:
        nuevo_horario = models.HorarioSemanal(
            usuario_id=usuario_id,
            dia_semana=dia_semana,
            hora_entrada=hora_entrada,
            hora_salida=hora_salida,
            observacion=observacion,
            fecha=datetime.strptime(fecha, "%Y-%m-%d").date() if fecha else None
        )
        db.add(nuevo_horario)

    db.commit()
