# app/metrics.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from . import models
import random

def salario_bruto_promedio(db: Session):
    promedio = db.query(func.avg(models.Nomina.total)).scalar()
    return promedio or 0

def bonificacion_promedio(db: Session):
    promedio = db.query(func.avg(models.Nomina.bonificacion)).scalar()
    return promedio or 0

def horas_extra_promedio(db: Session):
    promedio = db.query(func.avg(models.Nomina.horas_extra)).scalar()
    return promedio or 0

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
    # Como no hay tabla ventas, simulamos por usuario y mes
    from collections import defaultdict
    import calendar
    # Simulamos ventas para los últimos 6 meses
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
            # Simulamos venta entre 1000 y 10000
            total_mes += random.uniform(1000, 10000)
        ventas[key] = round(total_mes, 2)
    return dict(sorted(ventas.items()))
