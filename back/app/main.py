# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import crud, models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas
class UsuarioRegistro(BaseModel):
    correo: str
    contrasena: str
    empresa: str

class UsuarioLogin(BaseModel):
    correo: str
    contrasena: str

class NominaEntrada(BaseModel):
    usuario_id: int
    horas_trabajadas: int
    dias_incapacidad: int
    horas_extra: int
    bonificacion: float = 0.0
    periodo_pago: str

@app.post("/register")
def registrar(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    nuevo = crud.crear_usuario(db, usuario.correo, usuario.contrasena, usuario.empresa)
    if not nuevo:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    return {"mensaje": "Usuario registrado correctamente"}

@app.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = crud.autenticar_usuario(db, usuario.correo, usuario.contrasena)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"mensaje": "Inicio de sesión exitoso", "usuario_id": user.id, "empresa": user.empresa}

@app.post("/admin/crear_nomina")
def crear_nomina(nomina: NominaEntrada, db: Session = Depends(get_db)):
    empleado = db.query(models.Usuario).filter(models.Usuario.id == nomina.usuario_id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    nueva_nomina = crud.crear_nomina(
        db,
        nomina.usuario_id,
        nomina.horas_trabajadas,
        nomina.dias_incapacidad,
        nomina.horas_extra,
        nomina.bonificacion,
        nomina.periodo_pago
    )
    return {
        "mensaje": "Nómina creada correctamente",
        "salario_bruto": nueva_nomina.salario_bruto,
        "salud": nueva_nomina.salud,
        "pension": nueva_nomina.pension,
        "salario_neto": nueva_nomina.salario_neto,
        "periodo_pago": nueva_nomina.periodo_pago
    }