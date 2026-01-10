import streamlit_authenticator as stauth
import streamlit as st

# O segredo está aqui: @st.cache_resource impede que o login seja recriado a cada clique
@st.cache_resource
def get_authenticator():
    # --- CONFIGURAÇÃO DE USUÁRIOS ---
    users_config = {
        "usernames": {
            "admin": {
                "name": "Head Trader",
                "email": "admin@intelligenceflow.com",
                # Senha: 123
                "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W"
            },
            "membro": {
                "name": "Trader Pro",
                "email": "membro@intelligenceflow.com",
                # Senha: 123
                "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W"
            }
        }
    }

    cookie = {
        "expiry_days": 30,
        "key": "random_signature_key_intelligence_flow_v2",
        "name": "auth_cookie_flow_v2",
    }

    # Instancia o autenticador apenas uma vez
    authenticator = stauth.Authenticate(
        users_config,
        cookie['name'],
        cookie['key'],
        cookie['expiry_days']
    )
    
    return authenticator
