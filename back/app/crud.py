# app/crud.py
from sqlalchemy.orm import Session
from . import models
from .security import hashear_contrasena, verificar_contrasena
from datetime import datetime, date

def generar_id_usuario(db: Session, es_admin: bool) -> str:
    # Obtener el último ID generado según el tipo de usuario
    if es_admin:
        ultimo_usuario = db.query(models.Usuario).filter(
            models.Usuario.es_admin == True
        ).order_by(models.Usuario.id_usuario.desc()).first()
        
        if ultimo_usuario:
            ultimo_id = int(ultimo_usuario.id_usuario)
            nuevo_id = str(ultimo_id + 1)
        else:
            nuevo_id = "9000"  # ID inicial para administradores
            
        # Verificar que no exceda el límite
        if int(nuevo_id) > 9999:
            raise ValueError("Se ha alcanzado el límite de IDs para administradores")
    else:
        ultimo_usuario = db.query(models.Usuario).filter(
            models.Usuario.es_admin == False
        ).order_by(models.Usuario.id_usuario.desc()).first()
        
        if ultimo_usuario:
            ultimo_id = int(ultimo_usuario.id_usuario)
            nuevo_id = str(ultimo_id + 1)
        else:
            nuevo_id = "1000"  # ID inicial para usuarios normales
            
        # Verificar que no exceda el límite
        if int(nuevo_id) > 8999:
            raise ValueError("Se ha alcanzado el límite de IDs para usuarios")
    
    return nuevo_id.zfill(4)  # Asegura que siempre tenga 4 dígitos

def crear_usuario(
    db: Session, 
    nombre: str,
    apellido: str,
    cedula: str,
    correo: str, 
    contrasena: str, 
    empresa: str, 
    es_admin: bool = False, 
    fecha_nacimiento: date = None
):
    # Verificar campos vacíos
    if not all([nombre, apellido, cedula, correo, contrasena, empresa]):
        return None
        
    # Verificar duplicados con mensajes específicos
    usuario_existente = db.query(models.Usuario).filter(
        models.Usuario.correo == correo
    ).first()
    if usuario_existente:
        return None
        
    cedula_existente = db.query(models.Usuario).filter(
        models.Usuario.cedula == cedula
    ).first()
    if cedula_existente:
        return None
        
    try:
        hashed_pw = hashear_contrasena(contrasena)
        id_usuario = generar_id_usuario(db, es_admin)  # Generar ID único
        
        nuevo_usuario = models.Usuario(
            id_usuario=id_usuario,  # Agregar el nuevo ID
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            cedula=cedula.strip(),
            correo=correo.strip().lower(),
            contrasena=hashed_pw,
            empresa=empresa.strip(),
            es_admin=es_admin,
            fecha_nacimiento=fecha_nacimiento
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error al crear usuario: {str(e)}")

def autenticar_usuario(db: Session, correo: str, contrasena: str):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if not usuario:
        return None
    if not verificar_contrasena(contrasena, usuario.contrasena):
        return None
    return usuario

def crear_nomina(db: Session, usuario_id: int, horas_trabajadas: float, dias_incapacidad: int,
                 horas_extra: float, bonificacion: float, periodo_pago: str):
    valor_hora = 60000
    valor_incapacidad = 20000
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

def eliminar_usuario(db: Session, usuario_id: int):
    """
    Elimina un usuario y todos sus registros relacionados (nominas, horarios)
    
    Args:
        db: Sesión de base de datos
        usuario_id: ID del usuario a eliminar
        
    Returns:
        bool: True si se eliminó correctamente, False si el usuario no existe
    """
    # Verificar si el usuario existe
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        return False
    
    try:
        # Eliminar registros relacionados primero para mantener la integridad referencial
        # Eliminar horarios del usuario
        db.query(models.HorarioSemanal).filter(
            models.HorarioSemanal.usuario_id == usuario_id
        ).delete()
        
        # Eliminar nominas del usuario
        db.query(models.Nomina).filter(
            models.Nomina.usuario_id == usuario_id
        ).delete()
        
        # Finalmente eliminar el usuario
        db.delete(usuario)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e