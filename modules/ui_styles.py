import streamlit as st

def apply_design():
    st.markdown("""
    <style>
        /* 1. ESCONDER SIDEBAR E MENU PADRÃO */
        [data-testid="stSidebar"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }

        /* 2. IMAGEM DE FUNDO (DATA INTEGRATION) */
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }

        /* 3. PELÍCULA DE VIDRO (Para ler o texto sobre a imagem) */
        .stApp::before {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(248, 250, 252, 0.85); /* Branco Azulado 85% opaco */
            z-index: -1;
        }

        /* 4. CABEÇALHO DE NAVEGAÇÃO (Menu Superior) */
        .nav-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            padding: 15px;
            background: white;
            border-radius: 50px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* 5. TIPOGRAFIA & CORES */
        h1, h2, h3 { color: #0f172a !important; font-family: 'Segoe UI', sans-serif; font-weight: 700; }
        p, li, div { color: #334155; font-size: 1.05rem; }
        
        /* Destaques */
        .hero-title {
            background: -webkit-linear-gradient(45deg, #0047AB, #00b4d8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem !important;
            font-weight: 800 !important;
            text-align: center;
        }

        /* 6. RODAPÉ CNPJ */
        .footer-cnpj {
            margin-top: 50px;
            padding: 20px;
            text-align: center;
            border-top: 1px solid #cbd5e1;
            color: #64748b;
            font-size: 0.8rem;
        }
    </style>
    """, unsafe_allow_html=True)

def show_footer_cnpj():
    st.markdown("""
    <div class="footer-cnpj">
        <b>Intelligence Flow Ltda</b> • CNPJ: 52.123.456/0001-99<br>
        Paranaguá/PR • Curitiba/PR<br>
        Todos os direitos reservados © 2026
    </div>
    """, unsafe_allow_html=True)
