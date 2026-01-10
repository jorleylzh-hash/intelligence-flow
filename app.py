import streamlit as st
import time
from modules import ui_styles, auth_engine, dashboard_v3

# Configuração deve ser a primeira linha
st.set_page_config(page_title="Intelligence Flow", layout="wide", page_icon="🌪️")

# Inicializa Banco de Dados
auth_engine.init_db()

# Gerenciamento de Sessão (Login)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Aplica o Design
ui_styles.apply_design()

# --- NAVEGAÇÃO ---
if not st.session_state.logged_in:
    # TELA DE APRESENTAÇÃO / LOGIN
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        ui_styles.header_animation()
        st.markdown("<br>", unsafe_allow_html=True)
        
        tab_login, tab_register = st.tabs(["🔒 ACESSAR SISTEMA", "📝 SOLICITAR ACESSO"])
        
        with tab_login:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            email = st.text_input("Email Corporativo", key="login_email")
            password = st.text_input("Senha", type="password", key="login_pass")
            
            if st.button("CONECTAR KERNEL"):
                user = auth_engine.verify_login(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user[0][2] # Nome
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_register:
            st.warning("O cadastro gera credenciais automáticas enviadas por email.")
            new_name = st.text_input("Nome Completo")
            new_email = st.text_input("Seu Melhor Email")
            
            if st.button("GERAR CREDENCIAIS"):
                if new_name and new_email:
                    # Gera senha automática
                    auto_pass = auth_engine.generate_password()
                    
                    # Salva no Banco
                    if auth_engine.create_user(new_email, auto_pass, new_name):
                        # Envia Email (Simulado se não configurar SMTP)
                        auth_engine.send_confirmation_email(new_email, new_name, auto_pass)
                        
                        st.success("Cadastro realizado!")
                        st.info(f"📧 EMAIL ENVIADO PARA: {new_email}")
                        st.code(f"SENHA GERADA (Cópia de Segurança): {auto_pass}")
                    else:
                        st.error("Email já cadastrado.")
                else:
                    st.error("Preencha todos os campos.")

else:
    # USUÁRIO LOGADO -> MOSTRA O DASHBOARD
    with st.sidebar:
        st.write(f"Usuário: **{st.session_state.username}**")
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()
    
    # Chama o módulo do Dashboard
    dashboard_v3.show_dashboard()