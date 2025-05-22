# app/metrics.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from . import models
import random

def salario_neto_promedio(db: Session):
    promedio = db.query(func.avg(models.Nomina.total)).scalar()
    return promedio or 0

def salario_neto_sumatoria(db: Session):
    suma = db.query(func.sum(models.Nomina.total)).scalar()
    return suma or 0

def salario_bruto_promedio(db: Session):
    nominas = db.query(models.Nomina).all()
    total_bruto = 0
    count = 0
    for n in nominas:
        bruto = (
            (n.horas_trabajadas or 0)*60000 +
            (n.dias_incapacidad or 0)*20000 +
            (n.horas_extra or 0)*30000 +
            (n.bonificacion or 0)
        )
        total_bruto += bruto
        count += 1
    if count == 0:
        return 0
    return total_bruto / count

def salario_bruto_sumatoria(db: Session):
    nominas = db.query(models.Nomina).all()
    total_bruto = 0
    for n in nominas:
        bruto = (
            (n.horas_trabajadas or 0)*60000 +
            (n.dias_incapacidad or 0)*20000 +
            (n.horas_extra or 0)*30000 +
            (n.bonificacion or 0)
        )
        total_bruto += bruto
    return total_bruto

def horas_trabajadas_promedio(db: Session):
    promedio = db.query(func.avg(models.Nomina.horas_trabajadas)).scalar()
    return promedio or 0

def horas_trabajadas_sumatoria(db: Session):
    suma = db.query(func.sum(models.Nomina.horas_trabajadas)).scalar()
    return suma or 0

def bonificacion_promedio(db: Session):
    promedio = db.query(func.avg(models.Nomina.bonificacion)).scalar()
    return promedio or 0

def bonificacion_sumatoria(db: Session):
    suma = db.query(func.sum(models.Nomina.bonificacion)).scalar()
    return suma or 0

def edad_promedio(db: Session):
    hoy = date.today()
    usuarios = db.query(models.Usuario).filter(models.Usuario.fecha_nacimiento != None).all()
    edades = []
    for u in usuarios:
        edad = hoy.year - u.fecha_nacimiento.year - ((hoy.month, hoy.day) < (u.fecha_nacimiento.month, u.fecha_nacimiento.day))
        edades.append(edad)
    if not edades:
        return 0
    return sum(edades) / len(edades)

def edad_sumatoria(db: Session):
    hoy = date.today()
    usuarios = db.query(models.Usuario).filter(models.Usuario.fecha_nacimiento != None).all()
    total = 0
    for u in usuarios:
        edad = hoy.year - u.fecha_nacimiento.year - ((hoy.month, hoy.day) < (u.fecha_nacimiento.month, u.fecha_nacimiento.day))
        total += edad
    return total

def distribucion_edades(db: Session):
    hoy = date.today()
    usuarios = db.query(models.Usuario).filter(models.Usuario.fecha_nacimiento != None).all()
    rangos = {
        "<20": 0,
        "20-29": 0,
        "30-39": 0,
        "40-49": 0,
        "50-59": 0,
        "60+": 0,
    }
    for u in usuarios:
        if not u.fecha_nacimiento:
            continue
        edad = hoy.year - u.fecha_nacimiento.year - ((hoy.month, hoy.day) < (u.fecha_nacimiento.month, u.fecha_nacimiento.day))
        if edad < 20:
            rangos["<20"] += 1
        elif 20 <= edad <= 29:
            rangos["20-29"] += 1
        elif 30 <= edad <= 39:
            rangos["30-39"] += 1
        elif 40 <= edad <= 49:
            rangos["40-49"] += 1
        elif 50 <= edad <= 59:
            rangos["50-59"] += 1
        else:
            rangos["60+"] += 1
    return rangos

def ventas_simuladas_por_mes(db: Session):
    from collections import defaultdict
    ventas = defaultdict(float)
    usuarios = db.query(models.Usuario).all()
    meses = []
    hoy = date.today()
    for i in range(6):
        mes_anio = (hoy.month - i - 1) % 12 + 1
        anio = hoy.year - ((hoy.month - i - 1) // 12)
        meses.append((anio, mes_anio))
    for anio, mes in meses:
        key = f"{anio}-{mes:02d}"
        total_mes = 0
        for _ in usuarios:
            total_mes += random.uniform(1000, 10000)
        ventas[key] = round(total_mes, 2)
    return dict(sorted(ventas.items()))

