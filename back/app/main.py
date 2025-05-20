# app/main.py
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from . import crud, models
from .database import engine, SessionLocal
from .email_service import send_payroll_email

# ✅ Solo crea las tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esquemas
class UsuarioRegistro(BaseModel):
    correo: str
    contrasena: str
    empresa: str
    es_admin: bool = False

class UsuarioLogin(BaseModel):
    correo: str
    contrasena: str

class DatosNomina(BaseModel):
    usuario_id: int
    horas_trabajadas: float
    dias_incapacidad: int
    horas_extra: float
    bonificacion: float
    periodo_pago: str

class EmailRequest(BaseModel):
    usuario_id: int
    periodo_pago: str

@app.post("/register")
def registrar(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    nuevo = crud.crear_usuario(db, usuario.correo, usuario.contrasena, usuario.empresa, usuario.es_admin)
    if not nuevo:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    return {
        "mensaje": "Usuario registrado correctamente",
        "usuario_id": nuevo.id,
        "Correo": nuevo.correo  # Cambia a nuevo.nombre si tienes ese campo en el modelo
    }

@app.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = crud.autenticar_usuario(db, usuario.correo, usuario.contrasena)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if user.es_admin:
        mensaje = "Bienvenido administrador"
    else:
        mensaje = "Bienvenido usuario"

    return {
        "mensaje": mensaje,
        "usuario_id": user.id,
        "empresa": user.empresa
    }

@app.get("/admin/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).filter(models.Usuario.es_admin == False).all()
    return [{"id": u.id, "correo": u.correo, "empresa": u.empresa} for u in usuarios]

@app.get("/admin/administradores")
def listar_administradores(db: Session = Depends(get_db)):
    admins = db.query(models.Usuario).filter(models.Usuario.es_admin == True).all()
    return [{"id": a.id, "correo": a.correo, "empresa": a.empresa} for a in admins]

@app.post("/admin/crear_nomina")
def crear_nomina(datos: DatosNomina, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == datos.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    resultado = crud.crear_nomina(
        db,
        usuario_id=datos.usuario_id,
        horas_trabajadas=datos.horas_trabajadas,
        dias_incapacidad=datos.dias_incapacidad,
        horas_extra=datos.horas_extra,
        bonificacion=datos.bonificacion,
        periodo_pago=datos.periodo_pago
    )

    return {
        "mensaje": "Nómina registrada",
        "usuario_id": resultado["usuario_id"],
        "salario_bruto": f"${resultado['salario_bruto']:,.0f}",
        "menos_salud_4%": f"- ${resultado['descuento_salud']:,.0f}",
        "menos_pension_4%": f"- ${resultado['descuento_pension']:,.0f}",
        "salario_neto": f"${resultado['salario_neto']:,.0f}",
        "periodo_pago": resultado["periodo_pago"]
    }

@app.post("/enviar-nomina")
async def enviar_nomina(
    request: EmailRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    background_tasks.add_task(send_payroll_email, request.usuario_id, request.periodo_pago)
    return {"message": "Correo de nómina en proceso de envío"}