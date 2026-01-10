import streamlit as st

def apply_design():
    # URL ESTÁVEL (Unsplash - Abstract Blue Data Network)
    # Esta imagem não expira e não tem proteção de hotlink que troque o conteúdo
    bg_url = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop"

    st.markdown(f"""
    <style>
        /* 1. RESET E FUNDO */
        [data-testid="stSidebar"] {{ display: none; }}
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        
        .stApp {{
            /* Cor de fundo de segurança (Azul Escuro) caso a imagem demore a carregar */
            background-color: #0f172a;
            /* Imagem de Fundo: Rede Global de Dados (Space/Tech) */
            background-image: url("{bg_url}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        
        /* Camada de Contraste Profissional (Overlay) */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            /* Gradiente Sutil para garantir leitura: Azul Profundo -> Preto */
            background: linear-gradient(to bottom, rgba(15, 23, 42, 0.85), rgba(2, 6, 23, 0.95));
            z-index: -1;
        }}

        /* 2. MENU SUPERIOR (NAVBAR) - Estilo Tech Limpo */
        .stButton > button {{
            background-color: rgba(255, 255, 255, 0.05);
            color: #e2e8f0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s;
            border-radius: 4px;
            padding: 8px 24px;
        }}
        .stButton > button:hover {{
            color: #60a5fa; /* Azul Neon */
            border-color: #60a5fa;
            background-color: rgba(59, 130, 246, 0.1);
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
        }}

        /* 3. TIPOGRAFIA INSTITUCIONAL */
        h1, h2, h3, h4 {{ 
            color: #f8fafc !important; 
            font-family: 'Segoe UI', 'Roboto', sans-serif; 
            font-weight: 700; 
            letter-spacing: -0.5px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        p, li, div, span {{ 
            color: #cbd5e1; 
            font-size: 1.05rem; 
            line-height: 1.6; 
        }}
        
        /* Boxes Técnicos (Vidro Fosco) */
        .tech-box {{
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(148, 163, 184, 0.1);
            padding: 25px;
            border-radius: 12px;
            backdrop-filter: blur(5px);
            margin-bottom: 20px;
            transition: transform 0.2s;
        }}
        .tech-box:hover {{
            border-color: #3b82f6;
            background: rgba(30, 41, 59, 0.6);
        }}

        /* 4. RODAPÉ FIXO (Escuro) */
        .footer-cnpj {{
            margin-top: 100px;
            padding: 40px;
            text-align: center;
            border-top: 1px solid #1e293b;
            color: #64748b;
            font-size: 0.85rem;
            background: linear-gradient(to top, #020617, #0f172a);
        }}
    </style>
    """, unsafe_allow_html=True)

def show_footer_cnpj():
    st.markdown("""
    <div class="footer-cnpj">
        <span style="color:#e2e8f0; font-weight:bold; font-size:1rem; letter-spacing:1px;">INTELLIGENCE FLOW LTDA</span><br>
        <span style="color:#94a3b8;">CNPJ: 35.598.729/0001-60</span><br><br>
        <span style="color:#64748b;">Soluções de Tecnologia e Processamento de Dados de Alta Performance.</span><br>
        São Paulo • Curitiba • Miami Infrastructure
    </div>
    """, unsafe_allow_html=True)
