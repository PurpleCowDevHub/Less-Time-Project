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

def send_payroll_email(usuario_id: str, periodo_pago: str, realtime_callback=None):
    """
    Envía un correo electrónico con los detalles de la nómina con seguimiento en tiempo real
    Args:
        usuario_id: ID del usuario (puede ser el id numérico o id_usuario de 4 dígitos)
        periodo_pago: Periodo de pago (ej. '2023-12')
        realtime_callback: Función para enviar actualizaciones en tiempo real
    Returns:
        dict: Mensaje de éxito o error
    """
    def update_status(message):
        if realtime_callback:
            realtime_callback({"status": "progress", "message": message})

    db = SessionLocal()
    try:
        update_status("Iniciando proceso de envío...")
        
        # 1. Obtener datos del usuario
        update_status("Buscando información del empleado...")
        usuario = db.query(models.Usuario).filter(
            (models.Usuario.id == usuario_id) |
            (models.Usuario.id_usuario == usuario_id)
        ).first()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # 2. Buscar nómina
        update_status("Buscando datos de nómina...")
        nomina = db.query(models.Nomina).filter(
            models.Nomina.usuario_id == usuario.id,
            models.Nomina.periodo_pago == periodo_pago
        ).first()
        
        if not nomina:
            raise HTTPException(status_code=404, detail="Nómina no encontrada")

        # 3. Preparar correo
        update_status("Preparando correo electrónico...")
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{SENDER_NAME} <{EMAIL_ADDRESS}>"
        msg['To'] = usuario.correo
        msg['Subject'] = f"{usuario.empresa} - Recibo de Nómina {periodo_pago}"

        # 4. Crear contenido
        text_content = create_text_content(usuario, nomina)
        html_content = create_html_content(usuario, nomina)

        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))

        # 5. Enviar correo
        update_status("Conectando con el servidor de correos...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            update_status("Enviando correo...")
            server.send_message(msg)
            
        update_status("Correo enviado exitosamente")
        return {
            "status": "success",
            "message": "Correo enviado exitosamente",
            "details": {
                "usuario": f"{usuario.nombre} {usuario.apellido}",
                "correo": usuario.correo,
                "periodo": periodo_pago,
                "fecha_envio": datetime.datetime.now().isoformat(),
                "total_nomina": nomina.total
            }
        }
        
    except HTTPException:
        update_status("Error al procesar la solicitud")
        raise
    except smtplib.SMTPException as e:
        update_status(f"Error SMTP: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "message": "Error al enviar el correo",
                "details": str(e)
            }
        )
    except Exception as e:
        update_status(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Error inesperado",
                "details": str(e)
            }
        )
    finally:
        db.close()

def create_text_content(usuario: models.Usuario, nomina: models.Nomina) -> str:
    """Crea la versión en texto plano del correo con más detalles"""
    salario_base = nomina.horas_trabajadas * 60000  # Asumiendo valor hora de 60,000
    incapacidad = nomina.dias_incapacidad * 20000 if nomina.dias_incapacidad else 0
    horas_extra = nomina.horas_extra * 30000 if nomina.horas_extra else 0
    
    return f"""
    {usuario.empresa.upper()}
    Recibo de Nómina - {nomina.periodo_pago}
    {'='*40}

    Estimado(a) {usuario.nombre} {usuario.apellido},

    A continuación encontrará el detalle de su nómina:

    DATOS DEL EMPLEADO:
    - Nombre: {usuario.nombre} {usuario.apellido}
    - Cédula: {usuario.cedula}
    - ID Empleado: {usuario.id_usuario}

    DETALLE DE NÓMINA:
    - Salario base: ${salario_base:,.2f}
    - Horas trabajadas: {nomina.horas_trabajadas}
    - Días incapacidad: {nomina.dias_incapacidad} (${incapacidad:,.2f})
    - Horas extra: {nomina.horas_extra} (${horas_extra:,.2f})
    - Bonificación: ${nomina.bonificacion:,.2f}
    
    DESCUENTOS:
    - Salud (4%): ${salario_base * 0.04:,.2f}
    - Pensión (4%): ${salario_base * 0.04:,.2f}

    TOTAL NETO: ${nomina.total:,.2f}

    Fecha de pago: {datetime.datetime.now().strftime('%d/%m/%Y')}

    Este es un mensaje automático. Para cualquier consulta, por favor 
    contacte al departamento de Recursos Humanos.

    Atentamente,
    {SENDER_NAME}
    {usuario.empresa}
    """

def create_html_content(usuario: models.Usuario, nomina: models.Nomina) -> str:
    """Crea la versión HTML del correo con diseño profesional"""
    salario_base = nomina.horas_trabajadas * 60000
    incapacidad = nomina.dias_incapacidad * 20000 if nomina.dias_incapacidad else 0
    horas_extra = nomina.horas_extra * 30000 if nomina.horas_extra else 0
    descuento_salud = salario_base * 0.04
    descuento_pension = salario_base * 0.04
    fecha_envio = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recibo de Nómina {nomina.periodo_pago}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 700px;
                margin: 20px auto;
                background: white;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #2c3e50, #3498db);
                color: white;
                padding: 30px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .header h2 {{
                margin: 5px 0 0;
                font-size: 18px;
                font-weight: normal;
            }}
            .content {{
                padding: 30px;
            }}
            .employee-info {{
                background: #f9f9f9;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            .section-title {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 5px;
                margin-top: 25px;
            }}
            .payroll-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            .payroll-table th {{
                background-color: #3498db;
                color: white;
                text-align: left;
                padding: 12px;
            }}
            .payroll-table td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }}
            .payroll-table tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .total-row {{
                font-weight: bold;
                background-color: #e8f4fc !important;
            }}
            .net-total {{
                color: #27ae60;
                font-size: 18px;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                background: #f5f5f5;
                color: #777;
                font-size: 12px;
            }}
            .signature {{
                margin-top: 30px;
                border-top: 1px dashed #ccc;
                padding-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{usuario.empresa}</h1>
                <h2>Recibo de Nómina - {nomina.periodo_pago}</h2>
            </div>
            
            <div class="content">
                <div class="employee-info">
                    <p><strong>Empleado:</strong> {usuario.nombre} {usuario.apellido}</p>
                    <p><strong>Cédula:</strong> {usuario.cedula}</p>
                    <p><strong>ID Empleado:</strong> {usuario.id_usuario}</p>
                    <p><strong>Fecha de envío:</strong> {fecha_envio}</p>
                </div>
                
                <h3 class="section-title">Detalle de Nómina</h3>
                <table class="payroll-table">
                    <thead>
                        <tr>
                            <th>Concepto</th>
                            <th>Cantidad</th>
                            <th>Valor</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Salario base</td>
                            <td>{nomina.horas_trabajadas} horas</td>
                            <td>${salario_base:,.2f}</td>
                        </tr>
                        <tr>
                            <td>Días incapacidad</td>
                            <td>{nomina.dias_incapacidad} días</td>
                            <td>${incapacidad:,.2f}</td>
                        </tr>
                        <tr>
                            <td>Horas extra</td>
                            <td>{nomina.horas_extra} horas</td>
                            <td>${horas_extra:,.2f}</td>
                        </tr>
                        <tr>
                            <td>Bonificación</td>
                            <td>-</td>
                            <td>${nomina.bonificacion:,.2f}</td>
                        </tr>
                        <tr class="total-row">
                            <td colspan="2">Total Bruto</td>
                            <td>${salario_base + incapacidad + horas_extra + nomina.bonificacion:,.2f}</td>
                        </tr>
                        <tr>
                            <td>Descuento salud (4%)</td>
                            <td>-</td>
                            <td>-${descuento_salud:,.2f}</td>
                        </tr>
                        <tr>
                            <td>Descuento pensión (4%)</td>
                            <td>-</td>
                            <td>-${descuento_pension:,.2f}</td>
                        </tr>
                        <tr class="total-row net-total">
                            <td colspan="2">TOTAL NETO</td>
                            <td>${nomina.total:,.2f}</td>
                        </tr>
                    </tbody>
                </table>
                
                <div class="signature">
                    <p>Este comprobante ha sido generado automáticamente por el sistema de nómina.</p>
                    <p>Para cualquier aclaración, por favor contacte al departamento de Recursos Humanos.</p>
                </div>
            </div>
            
            <div class="footer">
                <p>{usuario.empresa} - Sistema de Gestión de Nóminas</p>
                <p>© {datetime.datetime.now().year} - Todos los derechos reservados</p>
            </div>
        </div>
    </body>
    </html>
    """