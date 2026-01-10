import streamlit as st
import modules.dashboard_v3 as dashboard_v3
import modules.auth_engine as auth_engine
import time

# 1. Configuração da Página
st.set_page_config(
    page_title="Intelligence Flow | Institutional",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicializar Estado
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# 3. Menu Lateral
st.sidebar.title("Navegação")
selection = st.sidebar.radio("Ir para:", ["🏠 Página Institucional", "🔐 Área de Membros"])

# 4. Roteamento Inteligente (AQUI ESTÁ A CORREÇÃO)
if selection == "🏠 Página Institucional":
    # Verifica qual função existe no arquivo para evitar o erro
    if hasattr(dashboard_v3, 'show_landing_page'):
        dashboard_v3.show_landing_page()
    elif hasattr(dashboard_v3, 'show_dashboard'):
        dashboard_v3.show_dashboard()
    else:
        st.error("Erro crítico: Nenhuma função de visualização encontrada no módulo dashboard_v3.")

elif selection == "🔐 Área de Membros":
    # Verifica se o motor de autenticação existe
    if hasattr(auth_engine, 'get_authenticator'):
        authenticator = auth_engine.get_authenticator()
        
        if st.session_state["authentication_status"]:
            st.sidebar.success(f"Logado como: {st.session_state['name']}")
            authenticator.logout('Sair', 'sidebar')
            st.title("🖥️ Mesa de Operações (Restrito)")
            st.success("Acesso Autorizado.")
            st.info("Painel de Trading carregado com sucesso.")
        else:
            st.markdown("## 🔐 Acesso à Mesa de Operações")
            st.write("Área exclusiva para assinantes.")
            name, authentication_status, username = authenticator.login('Login', 'main')
            
            if authentication_status == False:
                st.error('Usuário ou senha incorretos.')
            elif authentication_status == None:
                st.warning('Insira suas credenciais.')
    else:
        st.error("Erro: O módulo 'auth_engine' não foi carregado corretamente.")
