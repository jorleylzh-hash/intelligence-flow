import streamlit as st
import time
# Importa as funcionalidades da pasta modules
from modules import ui_styles, auth_engine, dashboard_v3

# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Intelligence Flow", layout="wide", page_icon="🌪️")

# Inicializa o Banco de Dados
auth_engine.init_db()

# Verifica se existe sessão de login, se não, cria como Falso
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Aplica o estilo visual (CSS)
ui_styles.apply_design()

# --- 2. LÓGICA DE NAVEGAÇÃO (O PORTEIRO) ---
if not st.session_state.logged_in:
    # === TELA DE LOGIN ===
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
                    st.session_state.username = user[0][2] # Pega o nome do usuário
                    st.rerun() # Recarrega a página para entrar
                else:
                    st.error("Credenciais inválidas.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_register:
            st.warning("O cadastro gera credenciais automáticas.")
            new_name = st.text_input("Nome Completo")
            new_email = st.text_input("Seu Melhor Email")
            
            if st.button("GERAR CREDENCIAIS"):
                if new_name and new_email:
                    # Gera senha e salva
                    auto_pass = auth_engine.generate_password()
                    if auth_engine.create_user(new_email, auto_pass, new_name):
                        auth_engine.send_confirmation_email(new_email, new_name, auto_pass)
                        st.success("Cadastro realizado com sucesso!")
                        st.info(f"📧 Usuário: {new_email}")
                        st.code(f"🔑 Senha: {auto_pass}") # Mostra a senha na tela
                    else:
                        st.error("Email já cadastrado.")
                else:
                    st.error("Preencha todos os campos.")

else:
    # === TELA DO DASHBOARD (SÓ ENTRA AQUI SE LOGGED_IN FOR TRUE) ===
    # Barra Lateral com Logout
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        if st.button("SAIR DO SISTEMA (LOGOUT)"):
            st.session_state.logged_in = False
            st.rerun()
    
    # Chama o Dashboard que está na pasta modules
    dashboard_v3.show_dashboard()
