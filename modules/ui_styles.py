import streamlit as st

def apply_design():
    st.markdown("""
    <style>
        /* 1. RESET E FUNDO (Deep Navy Professional) */
        [data-testid="stSidebar"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        
        .stApp {
            background-color: #0f172a; /* Azul Noturno */
            background-image: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
        }

        /* 2. MENU DE NAVEGAÇÃO RESPONSIVO */
        .nav-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            padding: 10px;
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid #334155;
        }
        
        .stButton > button {
            background: transparent;
            color: #cbd5e1;
            border: 1px solid transparent;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 1px;
            transition: all 0.3s;
            width: 100%; /* Mobile Friendly */
        }
        
        .stButton > button:hover {
            border-color: #3b82f6;
            color: #3b82f6;
            background: rgba(59, 130, 246, 0.1);
        }

        /* 3. TIPOGRAFIA RESPONSIVA */
        h1 { font-size: 2.5rem !important; }
        h2 { font-size: 1.8rem !important; }
        
        /* Ajustes para Mobile (Smartphones) */
        @media only screen and (max-width: 600px) {
            h1 { font-size: 1.8rem !important; }
            h2 { font-size: 1.4rem !important; }
            .stButton > button { font-size: 0.7rem; padding: 5px; }
        }
        
        /* Ajustes para Smart TV (4K) */
        @media only screen and (min-width: 2000px) {
            .stApp { zoom: 1.5; } /* Aumenta escala para ver de longe */
        }

        /* 4. CARDS E CONTEÚDO */
        .tech-card {
            background: #1e293b;
            border: 1px solid #334155;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .highlight-text { color: #60a5fa; font-weight: bold; }
        .math-block { 
            background: #020617; 
            padding: 15px; 
            border-left: 3px solid #f59e0b; 
            font-family: 'Courier New', monospace;
            color: #fbbf24;
            overflow-x: auto;
        }

        /* 5. RODAPÉ */
        .footer-cnpj {
            margin-top: 80px;
            padding: 30px;
            border-top: 1px solid #334155;
            text-align: center;
            background: #020617;
            font-size: 0.8rem;
            color: #64748b;
        }
    </style>
    """, unsafe_allow_html=True)

def show_footer_cnpj():
    st.markdown("""
    <div class="footer-cnpj">
        <strong style="color:#e2e8f0;">INTELLIGENCE FLOW TRATAMENTO DE DADOS LTDA</strong><br>
        CNPJ: 63.698.191/0001-27<br>
        Av. João Gualberto, 1721 - Conj 52, Andar 05 - Edif Vega Business - Curitiba/PR<br>
        © 2026 Intelligence Flow System
    </div>
    """, unsafe_allow_html=True)
