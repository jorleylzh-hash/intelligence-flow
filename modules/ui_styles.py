import streamlit as st

def apply_design():
    """
    Aplica o CSS global da aplicação (Estilo Dark/Institutional).
    """
    st.markdown("""
    <style>
        /* Importação de Fontes */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        
        /* Estrutura Geral */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #0f1115; /* Fundo Ultra Dark */
            color: #e2e8f0;
        }
        
        /* Menu de Navegação Superior */
        .nav-container {
            display: flex;
            justify-content: space-around;
            background-color: #1e293b;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #334155;
            margin-bottom: 20px;
        }
        
        /* Botões do Streamlit (Customização) */
        div.stButton > button {
            background-color: transparent;
            border: 1px solid transparent;
            color: #cbd5e1;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        div.stButton > button:hover {
            border-color: #d2a106; /* Dourado da Marca */
            color: #d2a106;
            background-color: rgba(210, 161, 6, 0.1);
        }
        
        div.stButton > button:focus {
            border-color: #d2a106;
            color: #d2a106;
            box-shadow: none;
        }

        /* Inputs e Caixas de Texto */
        .stTextInput > div > div > input {
            background-color: #1e293b;
            color: white;
            border: 1px solid #334155;
        }
        
        /* Métricas */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            color: #d2a106;
        }
    </style>
    """, unsafe_allow_html=True)

def show_footer_cnpj():
    """
    Rodapé simples com CNPJ (Usado na Landing Page ou Login).
    """
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #64748b; font-size: 0.8em;'>"
        "Intelligence Flow Ltda &copy; 2026 | CNPJ: 58.264.493/0001-33<br>"
        "Paranaguá - PR | Head of Operations: Jorley Zimermann"
        "</div>", 
        unsafe_allow_html=True
    )

def show_compliance_footer():
    """
    Rodapé Regulatório COMPLETO (Exigido pela CVM para telas logadas).
    CORRIGE O ERRO: AttributeError: module has no attribute 'show_compliance_footer'
    """
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #0f1115; color: #64748b; padding: 20px; font-size: 0.75rem; border-top: 1px solid #334155; text-align: justify; margin-top: 50px;">
        <strong>⚠️ DISCLAIMER REGULATÓRIO & RISCO DE MERCADO</strong><br><br>
        
        1. <strong>Natureza Tecnológica:</strong> O "Agente Intelligence Flow" é um sistema de Inteligência Artificial Generativa. As interpretações fornecidas são baseadas em modelos estatísticos e dados históricos, não garantindo rentabilidade futura.<br>
        
        2. <strong>Não é Recomendação (CVM 20):</strong> Este material tem caráter exclusivamente educativo e informativo (Full and Fair Disclosure). Nenhuma informação contida nesta plataforma constitui recomendação de investimento, análise de valores mobiliários ou "Call" de compra/venda.<br>
        
        3. <strong>Riscos:</strong> Operações em renda variável, derivativos e mercado de futuros (Day Trade) envolvem alto nível de risco e podem resultar na perda total do capital investido. O usuário é o único responsável por suas decisões.<br>
        
        4. <strong>Isenção:</strong> A Intelligence Flow Ltda não se responsabiliza por prejuízos financeiros decorrentes do uso das ferramentas automatizadas.
        
        <br><br>
        <center><strong>Intelligence Flow Solutions © 2026 - Todos os direitos reservados.</strong></center>
    </div>
    """, unsafe_allow_html=True)
