import resend
import streamlit as st

# ================= CONFIGURAÇÕES =================
# Sua chave da Resend (certifique-se de que ela está correta)
RESEND_API_KEY = "re_hyuD7Eas_DG4QL7Aq79FuKzZK7rBUW9sw"  # <--- COLE SUA CHAVE REAL AQUI
SENDER_EMAIL = "noreply@seguranca.intelligenceflow.pro" # Ou seu dominio verificado ex: security@intelligenceflow.com
# =================================================

def send_otp_email(to_email, code):
    """
    Envia o código de 4 dígitos para acesso.
    """
    if not RESEND_API_KEY or "re_123" in RESEND_API_KEY:
        st.error("⚠️ Configuração de E-mail incompleta. Verifique a API Key no arquivo notifications.py")
        return False

    resend.api_key = RESEND_API_KEY

    html_content = f"""
    <div style="font-family: 'Segoe UI', sans-serif; max-width: 400px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; background-color: #0f172a;">
        <h2 style="color: #f8fafc; text-align: center; margin-bottom: 20px;">Intelligence Flow</h2>
        <p style="color: #94a3b8; text-align: center;">Seu código de acesso à Mesa Proprietária:</p>
        <div style="background-color: #1e293b; padding: 15px; text-align: center; border-radius: 8px; margin: 20px 0;">
            <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #3b82f6;">{code}</span>
        </div>
        <p style="color: #64748b; font-size: 12px; text-align: center;">Este código expira em breve. Se você não solicitou, ignore.</p>
    </div>
    """

    try:
        r = resend.Emails.send({
            "from": f"Intelligence Security <{SENDER_EMAIL}>",
            "to": to_email,
            "subject": f"🔑 Código de Acesso: {code}",
            "html": html_content
        })
        return True
    except Exception as e:
        st.error(f"Erro no envio: {e}")
        return False
