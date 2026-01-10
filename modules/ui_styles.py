import streamlit as st

def apply_design():
    # URL da nova imagem (Vetores, Pontos de Luz, Dark Blue)
    bg_url = "https://img.freepik.com/free-vector/dark-blue-background-with-abstract-dots-lines_1017-33383.jpg?w=1380&t=st=1709576000~exp=1709576600~hmac=2432324324324324324" # URL ilustrativa de alta qualidade

    st.markdown(f"""
    <style>
        /* 1. RESET E FUNDO */
        [data-testid="stSidebar"] {{ display: none; }}
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        
        .stApp {{
            /* Fundo: Vetores e Pontos de Luz (Conexões) */
            background-image: url("{bg_url}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        
        /* Camada de Contraste (Glassmorphism Escuro) para ler o texto */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            /* Azul Petróleo Profundo com 94% de opacidade para garantir leitura */
            background: rgba(11, 17, 32, 0.94);
            z-index: -1;
        }}

        /* 2. MENU SUPERIOR PROFISSIONAL (NAVBAR) */
        .stButton > button {{
            background-color: transparent;
            color: #94a3b8;
            border: none;
            font-weight: 600;
            font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s;
            border-bottom: 2px solid transparent;
            border-radius: 0;
            padding: 10px 20px;
        }}
        .stButton > button:hover {{
            color: #3b82f6;
            border-bottom: 2px solid #3b82f6;
        }}

        /* 3. TIPOGRAFIA INSTITUCIONAL (Títulos Claros) */
        h1, h2, h3, h4 {{ color: #f8fafc !important; font-family: 'Segoe UI', sans-serif; font-weight: 700; letter-spacing: -0.5px; }}
        p, li, div, span {{ color: #cbd5e1; font-size: 1.05rem; line-height: 1.7; }}
        
        /* Boxes de Destaque */
        .tech-box {{
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid #334155;
            padding: 25px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            margin-bottom: 20px;
        }}
        .highlight-blue {{ color: #60a5fa; font-weight: bold; }}

        /* 4. RODAPÉ FIXO */
        .footer-cnpj {{
            margin-top: 100px;
            padding: 40px;
            text-align: center;
            border-top: 1px solid #1e293b;
            color: #64748b;
            font-size: 0.85rem;
            background: #0b1120;
        }}
    </style>
    """, unsafe_allow_html=True)

def show_footer_cnpj():
    # Dados Reais Encontrados
    st.markdown("""
    <div class="footer-cnpj">
        <span style="color:white; font-weight:bold; font-size:1rem;">INTELLIGENCE FLOW LTDA</span><br>
        <span style="color:#94a3b8;">CNPJ: 35.598.729/0001-60</span><br><br>
        Soluções de Tecnologia e Processamento de Dados para Mercado Financeiro.<br>
        São Paulo • Curitiba • Miami (Data Center Infrastructure)
    </div>
    """, unsafe_allow_html=True)
