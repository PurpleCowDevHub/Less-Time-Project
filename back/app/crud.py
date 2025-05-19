# app/crud.py
from sqlalchemy.orm import Session
from . import models
from .security import hashear_contrasena, verificar_contrasena

def crear_usuario(db: Session, correo: str, contrasena: str, empresa: str):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if usuario_existente:
        return None  # Ya existe
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