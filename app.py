import streamlit as st
from modules import ui_styles, auth_engine, dashboard_v3

# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Intelligence Flow", layout="wide", page_icon="🌪️")

# Inicializa o Banco de Dados
auth_engine.init_db()

# Verifica sessão
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Aplica estilo
ui_styles.apply_design()

# --- 2. NAVEGAÇÃO ---
if not st.session_state.logged_in:
    # === TELA DE LOGIN / CADASTRO ===
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        ui_styles.header_animation()
        st.markdown("<br>", unsafe_allow_html=True)
        
        tab_login, tab_register = st.tabs(["🔒 ACESSAR SISTEMA", "📝 NOVO CADASTRO"])
        
        with tab_login:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            email = st.text_input("Email Corporativo", key="login_email")
            password = st.text_input("Senha", type="password", key="login_pass")
            
            if st.button("CONECTAR KERNEL"):
                user = auth_engine.verify_login(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user[0][2]
                    st.rerun()
                else:
                    st.error("Acesso Negado: Email ou Senha incorretos.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_register:
            st.warning("⚠️ O envio de email está desativado. Copie sua senha abaixo.")
            new_name = st.text_input("Nome Completo")
            new_email = st.text_input("Seu Email")
            
            if st.button("CRIAR CONTA E GERAR SENHA"):
                if new_name and new_email:
                    auto_pass = auth_engine.generate_password()
                    
                    if auth_engine.create_user(new_email, auto_pass, new_name):
                        # Tenta notificar admin (se configurado)
                        auth_engine.send_whatsapp_admin(new_email, new_name, auto_pass)
                        
                        st.success("✅ Conta Criada!")
                        st.markdown("### 🔐 SUA CREDENCIAL")
                        st.info("Abaixo está sua senha provisória. Use o botão ao lado para copiar.")
                        
                        # --- CORREÇÃO DA CÓPIA (SENHA LIMPA) ---
                        st.code(auto_pass, language="text")
                        
                        st.caption("Dica: Cole a senha no Bloco de Notas antes de sair.")
                    else:
                        st.error("❌ Este email já possui cadastro.")
                else:
                    st.error("Preencha todos os campos.")

else:
    # === TELA DO DASHBOARD ===
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        if st.button("SAIR DO SISTEMA (LOGOUT)"):
            st.session_state.logged_in = False
            st.rerun()
    
    dashboard_v3.show_dashboard()
