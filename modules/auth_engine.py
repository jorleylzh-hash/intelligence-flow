import streamlit_authenticator as stauth
import streamlit as st

def get_authenticator():
    # Configuração explícita e correta
    users_config = {
        "usernames": {
            "admin": {
                "name": "Admin Trader",
                "email": "admin@intelligenceflow.com",
                "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W" # Senha: 123
            }
        },
        "cookie": {
            "expiry_days": 30,
            "key": "random_signature_key_if_2026",
            "name": "auth_cookie_if"
        },
        "preauthorized": {"emails": []}
    }

    # Instanciação direta
    authenticator = stauth.Authenticate(
        users_config,
        users_config['cookie']['name'],
        users_config['cookie']['key'],
        users_config['cookie']['expiry_days']
    )
    
    return authenticator
