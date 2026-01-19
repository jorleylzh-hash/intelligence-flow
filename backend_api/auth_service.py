import os
import random
import string
import resend
from passlib.context import CryptContext
from dotenv import load_dotenv

# --- 1. CARREGAMENTO DE AMBIENTE ---
load_dotenv()

# Configura a API Key
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# ⚠️ CONFIGURAÇÃO DO DOMÍNIO VERIFICADO ⚠️
# Como seu domínio no Resend é "seguranca.intelligenceflow.pro":
VERIFIED_DOMAIN_EMAIL = "security@seguranca.intelligenceflow.pro" 

if not RESEND_API_KEY:
    print("⚠️ AVISO: 'RESEND_API_KEY' não encontrada no .env")
else:
    resend.api_key = RESEND_API_KEY
    print(f"📧 Motor de E-mail Ativo | Remetente: {VERIFIED_DOMAIN_EMAIL}")

# Hashing de Senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- 2. FUNÇÕES ---

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def generate_complex_code(length=8):
    # Gera código tipo: X7a9#m2P
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# --- 3. ENVIO DE E-MAIL ---

def send_verification_email(to_email: str, code: str):
    if not RESEND_API_KEY:
        print("❌ Erro: Sem chave Resend configurada.")
        return False

    try:
        html_content = f"""
        <div style="font-family: 'Courier New', monospace; background-color: #000; color: #fff; padding: 40px;">
            <div style="max-width: 500px; margin: 0 auto; border: 1px solid #333; padding: 30px; border-radius: 8px;">
                <h2 style="color: #fff; margin-bottom: 20px;">INTELLIGENCE <span style="color: #06b6d4;">FLOW</span></h2>
                <p>Solicitação de credencial de acesso.</p>
                
                <div style="margin: 30px 0;">
                    <p style="font-size: 10px; text-transform: uppercase; color: #666;">Verification Code</p>
                    <div style="background-color: #111; color: #06b6d4; font-size: 32px; font-weight: bold; text-align: center; padding: 20px; border: 1px solid #06b6d4; letter-spacing: 6px;">
                        {code}
                    </div>
                </div>
                
                <p style="font-size: 12px; color: #666;">Válido por 15 minutos.</p>
            </div>
        </div>
        """
        
        # O Resend agora vai aceitar porque o domínio bate com o verificado
        r = resend.Emails.send({
            "from": f"Intelligence Flow <{VERIFIED_DOMAIN_EMAIL}>", 
            "to": to_email,
            "subject": "🔐 IFMD Access Code",
            "html": html_content
        })
        
        print(f"✅ E-mail enviado para {to_email} | ID: {r.get('id')}")
        return True
        
    except Exception as e:
        print(f"❌ Falha crítica no envio: {e}")
        # Dica de debug caso falhe
        if "authorized" in str(e):
            print("💡 DICA: Verifique se o domínio 'seguranca.intelligenceflow.pro' está com status 'Verified' no painel do Resend.")
        return False