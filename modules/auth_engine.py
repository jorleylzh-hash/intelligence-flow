import streamlit_authenticator as stauth
import streamlit as st

# REMOVIDO @st.cache_resource para evitar o erro "CachedWidgetWarning"
# A recriação deste objeto é rápida e não justifica o risco de crash.
def get_authenticator():
    # --- CONFIGURAÇÃO DE USUÁRIOS ---
    users_config = {
        "usernames": {
            "admin": {
                "name": "Head Trader",
                "email": "admin@intelligenceflow.com",
                "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W" # Senha: 123
            },
            "membro": {
                "name": "Trader Pro",
                "email": "membro@intelligenceflow.com",
                "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W" # Senha: 123
            }
        }
    }

    cookie = {
        "expiry_days": 30,
        "key": "random_signature_key_intelligence_flow_v3", # Chave nova
        "name": "auth_cookie_flow_v3",
    }

    authenticator = stauth.Authenticate(
        users_config,
        cookie['name'],
        cookie['key'],
        cookie['expiry_days']
    )
    
    return authenticator
