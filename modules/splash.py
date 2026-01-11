import streamlit as st
import time

def show_splash_screen():
    """
    Exibe uma animação cinematográfica de abertura (Splash Screen).
    Só roda na primeira vez que o usuário abre a sessão.
    """
    
    # Se já mostrou o splash nesta sessão, pula
    if 'splash_shown' in st.session_state and st.session_state['splash_shown']:
        return

    # --- CONFIGURAÇÃO DA ANIMAÇÃO ---
    # Substitua esta URL pelo link do seu GIF ou Vídeo renderizado hospedado
    # Exemplo: Um HUD futurista estilo "Intelligence Flow"
    SPLASH_IMAGE_URL = "https://i.pinimg.com/originals/2b/93/08/2b930843666f44d8b9d81cd24b75497b.gif" 
    
    # Define o container vazio que vai segurar a animação
    placeholder = st.empty()
    
    with placeholder.container():
        # CSS HACK para forçar Tela Cheia e fundo preto absoluto
        st.markdown(f"""
        <style>
        /* Esconde o menu e cabeçalho do Streamlit durante a intro */
        header {{visibility: hidden;}}
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Cria o overlay preto */
        .splash-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #000000;
            z-index: 99999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        
        .splash-img {{
            max-width: 80%;
            max-height: 80%;
            border-radius: 10px;
            box-shadow: 0 0 50px rgba(210, 161, 6, 0.3); /* Brilho Dourado da marca */
        }}
        
        .loading-text {{
            color: #d2a106; /* Dourado */
            font-family: 'Helvetica Neue', sans-serif;
            margin-top: 20px;
            letter-spacing: 3px;
            font-size: 1.2rem;
            animation: blink 1.5s infinite;
        }}
        
        @keyframes blink {{
            0% {{ opacity: 0.3; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.3; }}
        }}
        </style>
        
        <div class="splash-container">
            <img src="{SPLASH_IMAGE_URL}" class="splash-img">
            <div class="loading-text">INITIALIZING INTELLIGENCE FLOW...</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tempo de duração da vinheta (em segundos)
        time.sleep(4.5)
        
    # Limpa a tela
    placeholder.empty()
    
    # Marca que já foi visto para não repetir
    st.session_state['splash_shown'] = True
    
    # Opcional: Rerun para garantir que o CSS de "esconder menu" seja removido
    # st.rerun()
