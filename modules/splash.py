import streamlit as st
import time

def show_splash_screen():
    """
    Exibe uma animação cinematográfica de abertura (Splash Screen) com fundo de vídeo/GIF.
    Só roda na primeira vez que o usuário abre a sessão.
    """
    
    # Se já mostrou o splash nesta sessão, pula
    if 'splash_shown' in st.session_state and st.session_state['splash_shown']:
        return

    # --- CONFIGURAÇÃO DA VÍDEO-VINHETA ---
    # URL de um GIF de alta qualidade que simula uma "Matrix" de dados azul neon e formas geométricas.
    # NOTA PARA O JORLEY: Para o efeito exato de "cubos desfragmentando", você pode renderizar um vídeo MP4,
    # hospedá-lo (ex: S3, GitHub Pages) e substituir esta URL.
    SPLASH_VIDEO_URL = "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzhqbnh5NmJ6Nnd4OG55NmJ6Nnd4OG55NmJ6Nnd4OG55NmJ6Nnd4OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bmEHA9J7T8qI/giphy.gif"
    
    # Define o container vazio que vai segurar a animação
    placeholder = st.empty()
    
    with placeholder.container():
        # CSS para criar o efeito de vídeo de fundo em tela cheia
        st.markdown(f"""
        <style>
        /* Esconde a interface padrão do Streamlit durante a intro */
        header, footer, #MainMenu {{visibility: hidden !important;}}
        .stApp > header {{display: none !important;}}
        
        /* Container principal que cobre toda a tela */
        .splash-fullscreen {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #000; /* Fundo preto caso o vídeo demore a carregar */
            z-index: 999999; /* Garante que fique por cima de tudo */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }}
        
        /* O vídeo/GIF de fundo */
        .splash-bg-video {{
            position: absolute;
            top: 50%;
            left: 50%;
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            transform: translate(-50%, -50%); /* Centraliza perfeitamente */
            opacity: 0.6; /* Leve transparência para o texto se destacar */
            z-index: -1; /* Fica atrás do texto */
            object-fit: cover; /* Cobre a tela sem distorcer */
        }}
        
        /* O texto e logo sobrepostos */
        .splash-content {{
            z-index: 1;
            text-align: center;
        }}

        .loading-text {{
            color: #d2a106; /* Dourado da marca */
            font-family: 'Inter', sans-serif; /* Mesma fonte do sistema */
            margin-top: 20px;
            letter-spacing: 4px;
            font-weight: 600;
            font-size: 1.3rem;
            text-transform: uppercase;
            animation: pulseText 2s infinite ease-in-out;
            text-shadow: 0 0 10px rgba(210, 161, 6, 0.5);
        }}
        
        /* Animação suave do texto piscando */
        @keyframes pulseText {{
            0% {{ opacity: 0.4; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.4; }}
        }}
        </style>
        
        <div class="splash-fullscreen">
            <img src="{SPLASH_VIDEO_URL}" class="splash-bg-video">
            
            <div class="splash-content">
                <div class="loading-text">Iniciando Sistema Intelligence Flow...</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tempo de duração da vinheta (em segundos)
        time.sleep(5.0)
        
    # Limpa a tela, removendo a vinheta
    placeholder.empty()
    
    # Marca que já foi visto para não repetir nesta sessão
    st.session_state['splash_shown'] = True
