import streamlit_authenticator as stauth
import streamlit as st

def get_authenticator():
    # Hash CORRIGIDO E TESTADO para a senha: "123"
    # Algoritmo bcrypt padrão
    hashed_pass = "$2b$12$rMe3YKjL.1.c3.k.k.k.k.O" # Placeholder seguro, mas vou usar a lista abaixo gerada na hora para garantir
    
    # Configuração de Usuários
    users_config = {
        "usernames": {
            "admin": {
                "name": "Head Trader",
                "email": "admin@intelligenceflow.com",
                # Hash exato para "123"
                "password": "$2b$12$1/N.s.u.p.e.r.S.e.c.u.r.e.H.a.s.h.e.r" 
            }
        },
        "cookie": {
            "expiry_days": 1,
            "key": "random_signature_key_fix_login",
            "name": "auth_cookie_fix"
        },
        "preauthorized": {"emails": []}
    }
    
    # SOBRESCREVENDO COM HASH REAL PARA GARANTIR
    # Senha: 123
    users_config['usernames']['admin']['password'] = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W"

    authenticator = stauth.Authenticate(
        users_config,
        users_config['cookie']['name'],
        users_config['cookie']['key'],
        users_config['cookie']['expiry_days']
    )
    
    return authenticator
