# app/main.py
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query, APIRouter, status, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from . import crud, models
from .database import engine, SessionLocal
from .email_service import send_payroll_email
from .metrics import salario_bruto_promedio, bonificacion_promedio, horas_extra_promedio, distribucion_edades, ventas_simuladas_por_mes

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
    fecha_nacimiento: Optional[date] = None  # Nuevo campo para la fecha de nacimiento

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
    nuevo = crud.crear_usuario(
        db,
        correo=usuario.correo,
        contrasena=usuario.contrasena,
        empresa=usuario.empresa,
        es_admin=usuario.es_admin,
        fecha_nacimiento=usuario.fecha_nacimiento
    )
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
    if fecha is None:
        raise HTTPException(status_code=400, detail="Debe proporcionar una fecha en formato 'YYYY-MM-DD'")
    
    try:
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use 'YYYY-MM-DD'.")

    usuarios = db.query(models.Usuario).filter(models.Usuario.es_admin == False).all()
    resultado = []

    for u in usuarios:
        horarios = db.query(models.HorarioSemanal).filter(
            models.HorarioSemanal.usuario_id == u.id,
            models.HorarioSemanal.fecha == fecha_dt
        ).all()

        if horarios:  # Solo incluir usuarios con horarios en esa fecha
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
@app.get("/admin/metrics")
def obtener_metricas(db: Session = Depends(get_db)):
    return {
        "salario_bruto_promedio": f"${salario_bruto_promedio(db):,.2f}",
        "bonificacion_promedio": f"${bonificacion_promedio(db):,.2f}",
        "horas_extra_promedio": round(horas_extra_promedio(db), 2),
        "distribucion_edades": distribucion_edades(db),
        "ventas_simuladas_por_mes": ventas_simuladas_por_mes(db)
    }

@app.delete("/admin/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db)
):
    # Verificar si el usuario es administrador (podrías añadir esta validación)
    # if not current_user.es_admin:
    #     raise HTTPException(status_code=403, detail="Solo administradores pueden eliminar usuarios")
    
    # Intentar eliminar el usuario
    eliminado = crud.eliminar_usuario(db, usuario_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)