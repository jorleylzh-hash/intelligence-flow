import streamlit_authenticator as stauth

def get_authenticator():
    # Configuração de Usuários (Admin / Cliente)
    # Senhas criptografadas (Hash para "123")
    users_config = {
        "usernames": {
            "admin": {
                "name": "Head de Operações",
                "email": "admin@intelligenceflow.com",
                "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W"
            },
            "membro": {
                "name": "Trader Membro",
                "email": "membro@intelligenceflow.com",
                "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga311W"
            }
        }
    }

    cookie = {
        "expiry_days": 30,
        "key": "chave_secreta_randomica_brutal",
        "name": "auth_cookie_flow",
    }

    authenticator = stauth.Authenticate(
        users_config,
        cookie['name'],
        cookie['key'],
        cookie['expiry_days']
    )
    
    return authenticator
