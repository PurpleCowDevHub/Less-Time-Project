# app/security.py
from cryptography.fernet import Fernet

# Clave secreta segura y constante (guárdala bien, no la regeneres cada vez)
CLAVE_SECRETA = b'mi_clave_super_secreta_1234567890123456'  # 32 bytes exactos
fernet = Fernet(Fernet.generate_key())

def hashear_contrasena(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def verificar_contrasena(password: str, hashed: str) -> bool:
    try:
        decrypted = fernet.decrypt(hashed.encode()).decode()
        return decrypted == password
    except:
        return False