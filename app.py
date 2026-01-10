import streamlit as st
import modules.dashboard_v3 as dashboard_v3
import modules.auth_engine as auth_engine
import time

# 1. Configuração da Página (Primeira linha obrigatória)
st.set_page_config(
    page_title="Intelligence Flow | Institutional",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicializar Estado de Autenticação
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# 3. Navegação Principal (Menu Lateral)
st.sidebar.title("Navegação")
selection = st.sidebar.radio("Ir para:", ["🏠 Página Institucional", "🔐 Área de Membros"])

# 4. Roteamento de Páginas
if selection == "🏠 Página Institucional":
    # Carrega a página pública (SEM LOGIN)
    dashboard_v3.show_landing_page()

elif selection == "🔐 Área de Membros":
    # Carrega a lógica de Login
    authenticator = auth_engine.get_authenticator()
    
    # Se já estiver logado
    if st.session_state["authentication_status"]:
        st.sidebar.success(f"Logado como: {st.session_state['name']}")
        authenticator.logout('Sair', 'sidebar')
        
        st.title("🖥️ Mesa de Operações (Restrito)")
        st.success("Acesso Autorizado. Carregando ferramentas de trading...")
        # Aqui você chamaria o módulo real: modules.trading_desk.show()
        st.info("Gráficos em tempo real e boletas estariam aqui.")
        
    # Se NÃO estiver logado
    else:
        st.markdown("## 🔐 Acesso à Mesa de Operações")
        st.write("Área exclusiva para assinantes e operadores da Intelligence Flow.")
        
        name, authentication_status, username = authenticator.login('Login', 'main')
        
        if authentication_status == False:
            st.error('Usuário ou senha incorretos.')
        elif authentication_status == None:
            st.warning('Por favor, insira suas credenciais.')
