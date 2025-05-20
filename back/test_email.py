from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

load_dotenv()

def send_test_email():
    try:
        msg = MIMEText('Este es un correo de prueba desde Python')
        msg['Subject'] = 'Prueba SMTP'
        msg['From'] = os.getenv('SMTP_EMAIL')
        msg['To'] = os.getenv('SMTP_EMAIL')  # Enviar a ti mismo

        with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
            server.starttls()
            server.login(os.getenv('SMTP_EMAIL'), os.getenv('SMTP_PASSWORD'))
            server.send_message(msg)
        print('✅ Correo enviado exitosamente!')
    except Exception as e:
        print(f'❌ Error: {e}')

send_test_email()