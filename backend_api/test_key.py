import os
from dotenv import load_dotenv
import resend

# 1. Carrega o ambiente
load_dotenv()

# 2. Pega a chave
key = os.getenv("RESEND_API_KEY")

print("-" * 30)
if not key:
    print("❌ ERRO: O Python NÃO achou a chave. O arquivo .env está na mesma pasta?")
else:
    print(f"✅ Chave carregada: {key[:5]}...{key[-3:]}")
    print(f"   Tamanho: {len(key)} caracteres")
    
    # 3. Tenta enviar um e-mail de teste real
    print("\n📧 Tentando enviar e-mail de teste...")
    resend.api_key = key
    try:
        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "entregas@resend.dev", # E-mail de teste interno deles
            "subject": "Teste de API",
            "html": "<p>Funciona!</p>"
        })
        print(f"🚀 SUCESSO! ID do Email: {r.get('id')}")
    except Exception as e:
        print(f"💀 ERRO NO ENVIO: {e}")

print("-" * 30)