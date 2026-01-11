import streamlit_authenticator as stauth
import streamlit as st

def get_authenticator():
    # --- CORREÇÃO DEFINITIVA DO HASH ---
    # Geramos o hash da senha "123" em tempo real para garantir compatibilidade
    # com a versão instalada no servidor.
    passwords_to_hash = ['123']
    hashed_passwords = stauth.Hasher(passwords_to_hash).generate()
    
    users_config = {
        "usernames": {
            "admin": {
                "name": "Head Trader",
                "email": "admin@intelligenceflow.com",
                "password": hashed_passwords[0] # Usa o hash gerado agora
            }
        },
        "cookie": {
            "expiry_days": 1,
            "key": "random_signature_key_final_v5",
            "name": "auth_cookie_v5"
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
