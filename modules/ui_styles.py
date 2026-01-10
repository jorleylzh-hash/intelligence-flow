import streamlit as st

def apply_design():
    st.markdown("""
    <style>
        /* 1. RESET E FUNDO (Tech + Finance + AI) */
        [data-testid="stSidebar"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        
        .stApp {
            /* Fundo: Rede Neural Financeira Abstrata (Escuro/Azul Profundo) */
            background-image: url("https://img.freepik.com/premium-photo/futuristic-stock-market-background-with-trend-graph-digits-3d-view_102583-3972.jpg");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }
        
        /* Camada de Contraste (Glassmorphism Escuro) para ler o texto */
        .stApp::before {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(15, 23, 42, 0.92); /* Azul Noite Profundo 92% Opaco */
            z-index: -1;
        }

        /* 2. MENU SUPERIOR PROFISSIONAL (NAVBAR) */
        .stButton > button {
            background-color: transparent;
            color: #94a3b8;
            border: none;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s;
            border-bottom: 2px solid transparent;
            border-radius: 0;
            padding: 10px 20px;
        }
        .stButton > button:hover {
            color: #3b82f6;
            border-bottom: 2px solid #3b82f6;
            background-color: rgba(59, 130, 246, 0.05);
        }
        .stButton > button:focus {
            color: #fff;
            border-bottom: 2px solid #fff;
            box-shadow: none;
        }

        /* 3. TIPOGRAFIA INSTITUCIONAL */
        h1, h2, h3 { color: #f8fafc !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
        p, li, div { color: #cbd5e1; font-size: 1.05rem; line-height: 1.6; }
        
        /* Destaques Conceituais */
        .concept-highlight { color: #60a5fa; font-weight: bold; }
        .math-box { font-family: 'Courier New', monospace; background: rgba(0,0,0,0.3); padding: 10px; border-left: 3px solid #f59e0b; color: #fbbf24; }

        /* 4. RODAPÉ FIXO */
        .footer-cnpj {
            margin-top: 80px;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #334155;
            color: #64748b;
            font-size: 0.8rem;
            background: #0f172a;
        }
    </style>
    """, unsafe_allow_html=True)

def show_footer_cnpj():
    st.markdown("""
    <div class="footer-cnpj">
        <span style="color:white; font-weight:bold;">INTELLIGENCE FLOW LTDA</span><br>
        CNPJ: 52.123.456/0001-99 • Compliance & Risk Management<br>
        Paranaguá/PR • Curitiba/PR • Miami/FL (Data Center)
    </div>
    """, unsafe_allow_html=True)
