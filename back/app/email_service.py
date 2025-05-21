# app/email_service.py
import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from fastapi import HTTPException
from . import models
from .database import SessionLocal

# Cargar variables de entorno
load_dotenv()

# Configuración SMTP desde variables de entorno
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_ADDRESS = os.getenv("SMTP_EMAIL")
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_NAME = os.getenv("SENDER_NAME", "Sistema de Nóminas")

def send_payroll_email(usuario_id: str, periodo_pago: str):
    """
    Envía un correo electrónico con los detalles de la nómina
    Args:
        usuario_id: ID del usuario (puede ser el id numérico o id_usuario de 4 dígitos)
        periodo_pago: Periodo de pago (ej. '2023-12')
    Returns:
        dict: Mensaje de éxito o error
    """
    db = SessionLocal()
    try:
        # 1. Obtener datos del usuario (buscando por id o id_usuario)
        usuario = db.query(models.Usuario).filter(
            (models.Usuario.id == usuario_id) |  # Intenta como integer
            (models.Usuario.id_usuario == usuario_id)  # Intenta como string
        ).first()
        
        if not usuario:
            raise HTTPException(
                status_code=404,
                detail=f"Usuario con ID {usuario_id} no encontrado"
            )
        
        # 2. Buscar nómina usando el id interno (integer)
        nomina = db.query(models.Nomina).filter(
            models.Nomina.usuario_id == usuario.id,  # Usar el id real
            models.Nomina.periodo_pago == periodo_pago
        ).first()
        
        if not nomina:
            raise HTTPException(
                status_code=404,
                detail=f"Nómina no encontrada para el período {periodo_pago}"
            )

        # 3. Crear el mensaje de correo
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{SENDER_NAME} <{EMAIL_ADDRESS}>"
        msg['To'] = usuario.correo
        msg['Subject'] = f"Recibo de Nómina - {periodo_pago}"

        # 4. Crear contenido del correo
        text_content = create_text_content(usuario, nomina)
        html_content = create_html_content(usuario, nomina)

        # 5. Adjuntar ambas versiones
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))

        # 6. Enviar el correo
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            
        return {
            "status": "success", 
            "message": "Correo enviado exitosamente",
            "usuario_id": usuario.id_usuario  # Devolver el id visible al usuario
        }
        
    except HTTPException:
        # Re-lanzar las excepciones HTTP que ya hemos creado
        raise
    except smtplib.SMTPException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error al enviar el correo: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )
    finally:
        db.close()

def create_text_content(usuario: models.Usuario, nomina: models.Nomina) -> str:
    """Crea la versión en texto plano del correo"""
    return f"""
    Recibo de Nómina - {nomina.periodo_pago}
    Hola {usuario.correo.split('@')[0]},

    Detalles de tu nómina:
    - Horas trabajadas: {nomina.horas_trabajadas}
    - Horas extra: {nomina.horas_extra}
    - Bonificación: ${nomina.bonificacion:,.2f}
    - Total neto: ${nomina.total:,.2f}

    Saludos,
    {SENDER_NAME}
    """

def create_html_content(usuario: models.Usuario, nomina: models.Nomina) -> str:
    """Crea la versión HTML del correo con CSS en línea"""
    nombre_usuario = usuario.correo.split('@')[0]
    fecha_envio = datetime.datetime.now().strftime("%d/%m/%Y")
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Recibo de Nómina</title>
        <style type="text/css">
            .body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #2c3e50; padding: 20px; color: white; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 30px; }}
            .footer {{ text-align: center; font-size: 12px; color: #777; margin-top: 20px; }}
            .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            .table th {{ background-color: #f2f2f2; text-align: left; padding: 10px; }}
            .table td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
            .total {{ font-weight: bold; color: #27ae60; }}
        </style>
    </head>
    <body class="body">
        <div class="container">
            <div class="header">
                <h1>{usuario.empresa}</h1>
                <h2>Recibo de Nómina</h2>
            </div>
            
            <div class="content">
                <p>Estimado(a) <strong>{nombre_usuario}</strong>,</p>
                <p>Adjuntamos el detalle de tu nómina correspondiente al periodo:</p>
                <h3 style="text-align: center;">{nomina.periodo_pago}</h3>
                
                <table class="table">
                    <tr>
                        <th>Concepto</th>
                        <th>Valor</th>
                    </tr>
                    <tr>
                        <td>Horas trabajadas</td>
                        <td>{nomina.horas_trabajadas}</td>
                    </tr>
                    <tr>
                        <td>Horas extra</td>
                        <td>{nomina.horas_extra}</td>
                    </tr>
                    <tr>
                        <td>Bonificación</td>
                        <td>${nomina.bonificacion:,.2f}</td>
                    </tr>
                    <tr class="total">
                        <td>Total neto</td>
                        <td>${nomina.total:,.2f}</td>
                    </tr>
                </table>
                
                <p>Para cualquier consulta, por favor contacte al departamento de RRHH.</p>
            </div>
            
            <div class="footer">
                <p>Este es un mensaje automático, por favor no responda a este correo.</p>
                <p>Enviado el {fecha_envio} por {SENDER_NAME}</p>
            </div>
        </div>
    </body>
    </html>
    """