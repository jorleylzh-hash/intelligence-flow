import streamlit as st
import time

def show_splash_screen():
    if 'splash_shown' in st.session_state and st.session_state['splash_shown']:
        return

    # URL: Árvore Digital / Rede Neural Azul Neon
    SPLASH_VIDEO_URL = "https://i.pinimg.com/originals/e0/f8/33/e0f83350293eb70cf84b9015ba6a3943.gif"
    
    placeholder = st.empty()
    
    with placeholder.container():
        st.markdown(f"""
        <style>
        header, footer, #MainMenu {{visibility: hidden !important;}}
        .stApp > header {{display: none !important;}}
        
        .splash-fullscreen {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #000; z-index: 999999;
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
        }}
        
        .splash-bg-video {{
            position: absolute; top: 50%; left: 50%;
            min-width: 100%; min-height: 100%;
            transform: translate(-50%, -50%);
            opacity: 0.6; object-fit: cover;
        }}
        
        .loading-text {{
            z-index: 2; color: #d2a106;
            font-family: 'Inter', sans-serif; letter-spacing: 4px;
            font-weight: 600; font-size: 1.5rem;
            text-transform: uppercase;
            text-shadow: 0 0 20px rgba(210, 161, 6, 0.8);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{ 0% {{opacity: 0.6;}} 50% {{opacity: 1;}} 100% {{opacity: 0.6;}} }}
        </style>
        
        <div class="splash-fullscreen">
            <img src="{SPLASH_VIDEO_URL}" class="splash-bg-video">
            <div class="loading-text">Intelligence Flow<br><span style="font-size:0.6em; color:white;">Carregando Módulos...</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(4.5)
        
    placeholder.empty()
    st.session_state['splash_shown'] = True
