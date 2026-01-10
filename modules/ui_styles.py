import streamlit as st

def apply_design():
    st.markdown("""
    <style>
        /* 1. LIMPEZA TOTAL DA INTERFACE */
        [data-testid="stSidebar"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        
        /* 2. FUNDO SÓLIDO SÓBRIO (INSTITUCIONAL) */
        .stApp {
            /* Azul Profundo Quase Preto (Estilo Terminal Financeiro) */
            background-color: #0b1120; 
            background-image: none; /* Garante que nenhuma imagem carregue */
        }

        /* 3. MENU SUPERIOR */
        .stButton > button {
            background-color: transparent;
            color: #94a3b8;
            border: 1px solid #1e293b;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s;
            padding: 8px 20px;
        }
        .stButton > button:hover {
            border-color: #3b82f6;
            color: #3b82f6;
            background-color: rgba(59, 130, 246, 0.05);
        }

        /* 4. TIPOGRAFIA */
        h1, h2, h3 { color: #f8fafc !important; font-family: 'Segoe UI', sans-serif; }
        p, div, span, li { color: #cbd5e1; }
        
        /* Cards de Notícias e Dados */
        .tech-card {
            background-color: #1e293b;
            border: 1px solid #334155;
            padding: 20px;
            border-radius: 8px;
        }

        /* 5. RODAPÉ FIXO */
        .footer-cnpj {
            margin-top: 80px;
            padding: 40px;
            text-align: center;
            border-top: 1px solid #1e293b;
            background-color: #020617;
            color: #64748b;
            font-size: 0.85rem;
        }
    </style>
    """, unsafe_allow_html=True)

def show_footer_cnpj():
    # DADOS EXATOS DO PDF ENVIADO
    st.markdown("""
    <div class="footer-cnpj">
        <strong style="color:#e2e8f0; font-size:1rem;">INTELLIGENCE FLOW TRATAMENTO DE DADOS LTDA</strong><br>
        CNPJ: 63.698.191/0001-27<br>
        Av. João Gualberto, 1721 - Conj 52, Andar 05 - Edif Vega Business<br>
        Juvevê - Curitiba/PR - CEP 80.030-001<br>
        <br>
        Compliance & Data Processing • © 2026
    </div>
    """, unsafe_allow_html=True)
