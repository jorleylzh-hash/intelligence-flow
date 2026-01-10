import streamlit_authenticator as stauth
import streamlit as st

def get_authenticator():
    # Hash gerado para a senha "123"
    # Senha: 123
    hashed_pass = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W" 
    
    users_config = {
        "usernames": {
            "admin": {
                "name": "Admin Trader",
                "email": "admin@intelligenceflow.com",
                "password": hashed_pass
            }
        },
        "cookie": {
            "expiry_days": 30,
            "key": "random_signature_key_if_secure",
            "name": "auth_cookie_if"
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
