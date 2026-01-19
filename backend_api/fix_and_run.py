import os
import sys
import subprocess
import time

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def create_auth_service():
    content = """
import os
import random
import string
import resend
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY
    print(f"📧 Resend Configurado: ...{RESEND_API_KEY[-4:]}")
else:
    print("⚠️  RESEND_API_KEY não encontrada no .env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def generate_complex_code(length=8):
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choice(chars) for _ in range(length))

def send_verification_email(to_email: str, code: str):
    if not RESEND_API_KEY:
        print("❌ Erro: Sem chave API do Resend")
        return False
    try:
        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": "Codigo de Acesso IFMD",
            "html": f"<strong>Seu codigo: {code}</strong>"
        })
        print(f"✅ Email enviado: {r}")
        return True
    except Exception as e:
        print(f"❌ Erro Resend: {e}")
        return False
"""
    with open("auth_service.py", "w", encoding='utf-8') as f:
        f.write(content)
    print("✅ Arquivo 'auth_service.py' recriado com sucesso.")

def main():
    print("🔧 INICIANDO DIAGNÓSTICO E CORREÇÃO...")
    
    # 1. Verifica onde estamos
    current_dir = os.getcwd()
    print(f"📂 Diretório atual: {current_dir}")
    
    # 2. Verifica se main.py existe
    if not os.path.exists("main.py"):
        print("❌ ERRO CRÍTICO: 'main.py' não encontrado nesta pasta!")
        print("   Por favor, coloque este script na mesma pasta do main.py")
        return

    # 3. Recria o auth_service.py para garantir
    create_auth_service()

    # 4. Instala dependências forçadamente
    print("📦 Verificando dependências...")
    try:
        import resend
        import passlib
        import dotenv
    except ImportError:
        print("⚠️  Bibliotecas faltando. Instalando agora...")
        install("resend")
        install("passlib[bcrypt]")
        install("python-dotenv")
        install("email-validator")
        install("uvicorn")
        install("fastapi")
        install("sqlalchemy")
        install("psycopg2-binary")

    # 5. Inicia o servidor
    print("\n🚀 TUDO PRONTO! Iniciando Servidor...")
    time.sleep(2)
    os.system("uvicorn main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main()