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

# Esquemas para registro/login
class UsuarioRegistro(BaseModel):
    correo: str
    contrasena: str
    empresa: str

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

@app.post("/register")
def registrar(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    nuevo = crud.crear_usuario(db, usuario.correo, usuario.contrasena, usuario.empresa)
    if not nuevo:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    return {"mensaje": "Usuario registrado correctamente", "usuario_id": nuevo.id}

@app.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = crud.autenticar_usuario(db, usuario.correo, usuario.contrasena)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"mensaje": "Inicio de sesión exitoso", "usuario_id": user.id, "empresa": user.empresa}

@app.get("/admin/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()
    return [{"id": u.id, "correo": u.correo, "empresa": u.empresa} for u in usuarios]

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