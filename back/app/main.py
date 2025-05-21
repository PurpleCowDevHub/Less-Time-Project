# app/main.py
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from . import crud, models
from .database import engine, SessionLocal
from .email_service import send_payroll_email

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Schemas ---

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

class HorarioCrear(BaseModel):
    usuario_id: int
    dia_semana: str
    hora_entrada: Optional[str] = None
    hora_salida: Optional[str] = None
    observacion: Optional[str] = None
    fecha: Optional[str] = None  # Formato 'YYYY-MM-DD'

class HorarioResponse(BaseModel):
    dia_semana: str
    hora_entrada: Optional[str]
    hora_salida: Optional[str]
    observacion: Optional[str]

# --- Endpoints ---

@app.post("/register")
def registrar(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    nuevo = crud.crear_usuario(db, usuario.correo, usuario.contrasena, usuario.empresa, usuario.es_admin)
    if not nuevo:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    return {
        "mensaje": "Usuario registrado correctamente",
        "usuario_id": nuevo.id,
        "Correo": nuevo.correo
    }

@app.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = crud.autenticar_usuario(db, usuario.correo, usuario.contrasena)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    mensaje = "Bienvenido administrador" if user.es_admin else "Bienvenido usuario"
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

# --- Endpoints para horarios ---

@app.post("/admin/horarios")
def asignar_horario(horario: HorarioCrear, db: Session = Depends(get_db)):
    crud.crear_o_actualizar_horario(
        db,
        usuario_id=horario.usuario_id,
        dia_semana=horario.dia_semana,
        hora_entrada=horario.hora_entrada,
        hora_salida=horario.hora_salida,
        observacion=horario.observacion,
        fecha=horario.fecha
    )
    return {"mensaje": "Horario asignado o actualizado"}

@app.get("/admin/horarios/{usuario_id}", response_model=List[HorarioResponse])
def obtener_horarios(usuario_id: int, fecha: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.HorarioSemanal).filter(models.HorarioSemanal.usuario_id == usuario_id)
    if fecha:
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
        query = query.filter(models.HorarioSemanal.fecha == fecha_dt)
    horarios = query.all()
    return horarios

@app.get("/admin/usuarios_con_horarios")
def listar_usuarios_con_horarios(fecha: Optional[str] = Query(None), db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).filter(models.Usuario.es_admin == False).all()
    fecha_dt = None
    if fecha:
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
    resultado = []
    for u in usuarios:
        query = db.query(models.HorarioSemanal).filter(models.HorarioSemanal.usuario_id == u.id)
        if fecha_dt:
            query = query.filter(models.HorarioSemanal.fecha == fecha_dt)
        horarios = query.all()
        resultado.append({
            "id": u.id,
            "correo": u.correo,
            "empresa": u.empresa,
            "horarios": [
                {
                    "dia_semana": h.dia_semana,
                    "hora_entrada": h.hora_entrada,
                    "hora_salida": h.hora_salida,
                    "observacion": h.observacion
                } for h in horarios
            ]
        })
    return resultado
