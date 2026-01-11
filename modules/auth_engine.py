import streamlit_authenticator as stauth
import streamlit as st

def get_authenticator():
    # --- SENHA '123' JÁ CRIPTOGRAFADA ---
    # Isso elimina o erro de "Hasher.__init__" pois não calculamos nada na hora.
    # Este código abaixo equivale a "123"
    hashed_pass = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W"
    
    users_config = {
        "usernames": {
            "admin": {
                "name": "Head Trader",
                "email": "admin@intelligenceflow.com",
                "password": hashed_pass
            }
        },
        "cookie": {
            "expiry_days": 1,
            "key": "random_signature_key_final_v6",
            "name": "auth_cookie_v6"
        },
        "preauthorized": {"emails": []}
    }

    authenticator = stauth.Authenticate(
        users_config,
        users_config['cookie']['name'],
        users_config['cookie']['key'],
        users_config['cookie']['expiry_days']
    )
    
    return authenticator
