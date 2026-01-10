import streamlit_authenticator as stauth
import streamlit as st

def get_authenticator():
    # --- BASE DE DADOS DE USUÁRIOS (Simulada) ---
    # Aqui definimos o admin. A senha abaixo é o hash para "123".
    # Em produção real, isso viria de um arquivo config.yaml ou banco de dados.
    
    users_config = {
        "usernames": {
            "admin": {
                "name": "Head de Operações",
                "email": "admin@intelligenceflow.com",
                "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W" # Senha: 123
            },
            "investidor": {
                "name": "Cliente VIP",
                "email": "cliente@email.com",
                "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W" # Senha: 123
            }
        }
    }

    # --- CONFIGURAÇÃO DO COOKIE ---
    cookie_config = {
        "expiry_days": 30,
        "key": "random_signature_key_intelligence_flow", # Chave secreta interna
        "name": "auth_cookie_flow",
    }

    # --- INICIALIZA O OBJETO AUTENTICADOR ---
    authenticator = stauth.Authenticate(
        users_config,
        cookie_config['name'],
        cookie_config['key'],
        cookie_config['expiry_days']
    )
    
    return authenticator
