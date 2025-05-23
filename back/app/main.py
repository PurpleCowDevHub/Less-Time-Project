# app/main.py
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query, APIRouter, status, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime, date
from . import crud, models
from .database import engine, SessionLocal
from .email_service import send_payroll_email
from .metrics import (
    salario_bruto_promedio,
    salario_bruto_sumatoria,
    salario_neto_promedio,
    salario_neto_sumatoria,
    horas_trabajadas_promedio,
    horas_trabajadas_sumatoria,
    bonificacion_promedio,
    bonificacion_sumatoria,
    edad_promedio,
    edad_sumatoria,
    distribucion_edades,
    ventas_simuladas_por_mes,
)

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
    nombre: str
    apellido: str
    cedula: str
    correo: str
    contrasena: str
    confirmar_contrasena: str
    empresa: str
    es_admin: bool = False
    fecha_nacimiento: Optional[date] = None

    @validator('nombre', 'apellido')
    def validate_nombres(cls, v):
        if not v.strip():
            raise ValueError('Este campo no puede estar vacío')
        if len(v) > 100:
            raise ValueError('Máximo 100 caracteres permitidos')
        return v.strip()

    @validator('cedula')
    def validate_cedula(cls, v):
        if not v.strip():
            raise ValueError('La cédula es requerida')
        if len(v) < 5:
            raise ValueError('La cédula debe tener al menos 5 caracteres')
        return v.strip()

    @validator('correo')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Ingrese un correo electrónico válido')
        return v.strip()

    @validator('contrasena')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe contener al menos un número')
        return v

    @validator('confirmar_contrasena')
    def passwords_match(cls, v, values, **kwargs):
        if 'contrasena' in values and v != values['contrasena']:
            raise ValueError('Las contraseñas no coinciden. Por favor verifique')
        return v


class UsuarioLogin(BaseModel):
    correo: str
    contrasena: str

class DatosNomina(BaseModel):
    usuario_id: str
    horas_trabajadas: float
    dias_incapacidad: int
    horas_extra: float
    bonificacion: float
    periodo_pago: str

class EmailRequest(BaseModel):
    usuario_id: str
    periodo_pago: str

class HorarioCrear(BaseModel):
    usuario_id: str  # Cambiado de int a str para aceptar id_usuario
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
    try:
        nuevo = crud.crear_usuario(
            db,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            cedula=usuario.cedula,
            correo=usuario.correo,
            contrasena=usuario.contrasena,
            empresa=usuario.empresa,
            es_admin=usuario.es_admin,
            fecha_nacimiento=usuario.fecha_nacimiento
        )
        
        if not nuevo:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "message": "No se pudo completar el registro",
                    "details": [
                        {
                            "field": "general",
                            "error": "El correo electrónico o la cédula ya están registrados",
                            "suggestion": "Utilice otro correo o cédula, o recupere su cuenta si ya está registrado"
                        }
                    ]
                }
            )
            
        return {
            "status": "success",
            "message": "Registro completado exitosamente",
            "data": {
                "usuario_id": nuevo.id_usuario,
                "nombre_completo": f"{nuevo.nombre} {nuevo.apellido}",
                "correo": nuevo.correo
            }
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "status": "error",
                "message": "Error de validación en los datos",
                "details": [{
                    "field": "contrasena",  # Esto se ajusta dinámicamente
                    "error": str(e),
                    "suggestion": "Revise los requisitos del campo"
                }]
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Error interno del servidor",
                "details": str(e)
            }
        )

@app.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = crud.autenticar_usuario(db, usuario.correo, usuario.contrasena)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    mensaje = "Bienvenido administrador" if user.es_admin else "Bienvenido usuario"
    return {
        "mensaje": mensaje,
        "usuario_id": user.id_usuario,
        "empresa": user.empresa
    }

# En main.py, actualizar los endpoints de listado:
@app.get("/admin/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).filter(models.Usuario.es_admin == False).all()
    return [{
        "id": u.id_usuario,  # Usar el nuevo id_usuario
        "nombre": f"{u.nombre} {u.apellido}",
        "cedula": u.cedula,
        "correo": u.correo, 
        "empresa": u.empresa
    } for u in usuarios]

@app.get("/admin/administradores")
def listar_administradores(db: Session = Depends(get_db)):
    admins = db.query(models.Usuario).filter(models.Usuario.es_admin == True).all()
    return [{
        "id": a.id_usuario,  # Usar el nuevo id_usuario
        "nombre": f"{a.nombre} {a.apellido}",
        "cedula": a.cedula,
        "correo": a.correo, 
        "empresa": a.empresa
    } for a in admins]

@app.post("/admin/crear_nomina")
def crear_nomina(datos: DatosNomina, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        (models.Usuario.id == datos.usuario_id) | 
        (models.Usuario.id_usuario == str(datos.usuario_id))
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    resultado = crud.crear_nomina(
        db,
        usuario_id=usuario.id,  
        horas_trabajadas=datos.horas_trabajadas,
        dias_incapacidad=datos.dias_incapacidad,
        horas_extra=datos.horas_extra,
        bonificacion=datos.bonificacion,
        periodo_pago=datos.periodo_pago
    )

    return {
        "mensaje": "Nómina registrada",
        "usuario_id": usuario.id_usuario,
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
    usuario = db.query(models.Usuario).filter(
        (models.Usuario.id == request.usuario_id) |  
        (models.Usuario.id_usuario == request.usuario_id)  
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    background_tasks.add_task(
        send_payroll_email, 
        usuario_id=usuario.id,  
        periodo_pago=request.periodo_pago
    )
    
    return {
        "message": "Correo de nómina en proceso de envío",
        "usuario_id": usuario.id_usuario  
    }

# --- Endpoints para horarios ---

@app.post("/admin/horarios")
def asignar_horario(horario: HorarioCrear, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == horario.usuario_id
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    crud.crear_o_actualizar_horario(
        db,
        usuario_id=usuario.id,  
        dia_semana=horario.dia_semana,
        hora_entrada=horario.hora_entrada,
        hora_salida=horario.hora_salida,
        observacion=horario.observacion,
        fecha=horario.fecha
    )
    return {"mensaje": "Horario asignado o actualizado"}

@app.get("/admin/horarios/{usuario_id}", response_model=List[HorarioResponse])
def obtener_horarios(usuario_id: str, fecha: Optional[str] = Query(None), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == usuario_id
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    query = db.query(models.HorarioSemanal).filter(models.HorarioSemanal.usuario_id == usuario.id)
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

        if horarios:
            resultado.append({
                "id": u.id_usuario,
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
        "salario_bruto_sumatoria": f"${salario_bruto_sumatoria(db):,.2f}",
        "salario_neto_promedio": f"${salario_neto_promedio(db):,.2f}",
        "salario_neto_sumatoria": f"${salario_neto_sumatoria(db):,.2f}",
        "horas_trabajadas_promedio": round(horas_trabajadas_promedio(db), 2),
        "horas_trabajadas_sumatoria": round(horas_trabajadas_sumatoria(db), 2),
        "bonificacion_promedio": f"${bonificacion_promedio(db):,.2f}",
        "bonificacion_sumatoria": f"${bonificacion_sumatoria(db):,.2f}",
        "edad_promedio": round(edad_promedio(db), 2),
        "edad_sumatoria": edad_sumatoria(db),
        "distribucion_edades": distribucion_edades(db),
        "ventas_simuladas_por_mes": ventas_simuladas_por_mes(db)
    }

@app.delete("/admin/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    usuario_id: str,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == usuario_id
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    
    eliminado = crud.eliminar_usuario(db, usuario.id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error al eliminar usuario con ID {usuario_id}"
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
