import streamlit as st

def apply_design():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        html, body, [class*="css"] {font-family: 'Inter', sans-serif; background-color: #0f1115; color: #e2e8f0;}
        .nav-container {display: flex; justify-content: space-around; background-color: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 20px;}
        div.stButton > button {background-color: transparent; border: 1px solid transparent; color: #cbd5e1; width: 100%;}
        div.stButton > button:hover {border-color: #d2a106; color: #d2a106; background-color: rgba(210, 161, 6, 0.1);}
        .stTextInput > div > div > input {background-color: #1e293b; color: white; border: 1px solid #334155;}
    </style>
    """, unsafe_allow_html=True)

def show_footer_cnpj():
    st.markdown("---")
    st.markdown("<div style='text-align:center; color:#64748b; font-size:0.8em;'>Intelligence Flow Ltda © 2026 | CNPJ: 58.264.493/0001-33</div>", unsafe_allow_html=True)

def show_compliance_footer():
    # A variável abaixo NÃO pode ter indentação (espaços) no início das linhas
    html_content = """
<div style="background-color: #0f1115; color: #64748b; padding: 15px; font-size: 0.75rem; border-top: 1px solid #334155; text-align: justify; margin-top: 30px;">
    <strong style="color: #94a3b8;">⚠️ DISCLAIMER REGULATÓRIO & RISCO DE MERCADO</strong><br><br>
    <strong>1. Natureza Tecnológica:</strong> O "Agente Intelligence Flow" é um sistema de Inteligência Artificial Generativa. Interpretações baseadas em estatística, não garantem rentabilidade.<br>
    <strong>2. Não é Recomendação (CVM 20):</strong> Material estritamente educativo (Full and Fair Disclosure). Não constitui oferta ou Call de compra/venda.<br>
    <strong>3. Riscos:</strong> Day Trade envolve alto risco e possibilidade de perda total do capital.<br>
    <strong>4. Isenção:</strong> A Intelligence Flow Ltda não se responsabiliza por decisões financeiras tomadas com base na ferramenta.
    <br><br>
    <div style="text-align: center;"><strong>Intelligence Flow Solutions © 2026</strong> - Todos os direitos reservados.</div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)
