import streamlit as st

def apply_design():
    # Design Glassmorphism + Cyberpunk
    st.markdown("""
    <style>
        /* Fundo e Fontes */
        .stApp { 
            background-color: #0c0a09; 
            background-image: radial-gradient(circle at 50% 50%, #1c1917 0%, #0c0a09 100%);
            color: #e7e5e4; 
        }
        
        /* Caixa de Login Estilizada */
        .login-box {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            text-align: center;
        }

        /* Botões Neon */
        div.stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #10b981 0%, #059669 100%);
            color: white;
            border: none;
            padding: 12px;
            font-weight: bold;
            border-radius: 5px;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            box-shadow: 0 0 15px #10b981;
            transform: scale(1.02);
        }
        
        /* Inputs */
        div[data-baseweb="input"] {
            background-color: #1c1917;
            border: 1px solid #44403c;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

def header_animation():
    # Título Dinâmico
    st.markdown("""
    <h1 style='text-align: center; font-size: 60px; background: linear-gradient(to right, #10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        INTELLIGENCE FLOW
    </h1>
    <p style='text-align: center; color: #a8a29e; letter-spacing: 3px; font-family: monospace;'>
        INSTITUTIONAL GRADE ANALYTICS
    </p>
    """, unsafe_allow_html=True)