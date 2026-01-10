import streamlit as st
import modules.dashboard_v3 as dashboard_v3
import modules.auth_engine as auth_engine

# --- CONFIGURAÇÃO DA PÁGINA (Deve ser a primeira linha) ---
st.set_page_config(
    page_title="Intelligence Flow | Institutional",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INICIALIZAÇÃO DE ESTADO ---
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# --- BARRA LATERAL (LOGIN) ---
with st.sidebar:
    st.title("🔐 Acesso Restrito")
    # Chama o motor de autenticação (mas não bloqueia o app principal)
    authenticator = auth_engine.get_authenticator()
    name, authentication_status, username = authenticator.login('Login', 'main')

# --- LÓGICA DE EXIBIÇÃO ---

if st.session_state['authentication_status']:
    # === CENÁRIO 1: USUÁRIO LOGADO (ÁREA VIP) ===
    # Aqui você mostraria as ferramentas avançadas/operacionais
    st.sidebar.success(f"Bem-vindo, {name}!")
    st.sidebar.write("---")
    
    # Menu de Navegação do Usuário Logado
    page = st.sidebar.radio("Navegação", ["Home Institucional", "Mesa de Operações", "Gestão de Risco"])
    
    if page == "Home Institucional":
        dashboard_v3.show_dashboard()
    elif page == "Mesa de Operações":
        st.title("📈 Mesa de Operações (Área Privada)")
        st.info("Aqui entram os gráficos avançados, boletas e calculadoras exclusivas para assinantes.")
        # import modules.trading_desk as trading
        # trading.show()
    elif page == "Gestão de Risco":
        st.write("Ferramentas de Risco...")
        
    authenticator.logout('Sair', 'sidebar')

else:
    # === CENÁRIO 2: VISITANTE (PÁGINA PÚBLICA) ===
    # Mostra a página corporativa "Fantástica" para vender o produto
    dashboard_v3.show_dashboard()
    
    # Se a senha estiver errada
    if st.session_state['authentication_status'] == False:
        st.sidebar.error('Usuário ou senha incorretos')
    
    # Se não tiver tentado logar ainda
    elif st.session_state['authentication_status'] == None:
        st.sidebar.warning('Faça login para acessar a Mesa de Operações.')
