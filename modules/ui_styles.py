import streamlit as st

def apply_design():
    st.markdown("""
    <style>
        /* RESET E FUNDO SÓLIDO */
        [data-testid="stSidebar"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        
        .stApp {
            background-color: #020617; /* Azul Noturno Quase Preto */
            background-image: none;
        }

        /* MENU SUPERIOR */
        .stButton > button {
            background: transparent;
            color: #94a3b8;
            border: 1px solid #1e293b;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 1px;
            transition: all 0.3s;
        }
        .stButton > button:hover {
            border-color: #3b82f6;
            color: #3b82f6;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.2);
        }

        /* TIPOGRAFIA */
        h1, h2, h3, h4 { color: #f8fafc !important; font-family: 'Segoe UI', sans-serif; }
        p, li, span, div { color: #cbd5e1; font-family: 'Segoe UI', sans-serif; }
        
        /* CAIXAS DE CONTEÚDO (CONCEITOS) */
        .concept-card {
            background: #0f172a;
            border-left: 4px solid #3b82f6;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 0 8px 8px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .concept-title { color: #60a5fa; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; }
        
        /* STATUS DAS APIS */
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: bold;
            margin-right: 10px;
        }

        /* RODAPÉ */
        .footer-cnpj {
            margin-top: 100px;
            padding: 40px;
            border-top: 1px solid #1e293b;
            text-align: center;
            background: #000000;
        }
    </style>
    """, unsafe_allow_html=True)

def show_footer_cnpj():
    st.markdown("""
    <div class="footer-cnpj">
        <strong style="color:white; font-size:1.1rem;">INTELLIGENCE FLOW TRATAMENTO DE DADOS LTDA</strong><br>
        <span style="color:#94a3b8;">CNPJ: 63.698.191/0001-27</span><br>
        <span style="color:#64748b;">Av. João Gualberto, 1721 - Conj 52, Andar 05 - Edif Vega Business<br>
        Juvevê - Curitiba/PR - CEP 80.030-001</span><br><br>
        © 2026 Intelligence Flow. Todos os direitos reservados.
    </div>
    """, unsafe_allow_html=True)
