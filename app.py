import streamlit as st
import modules.dashboard_v3 as dashboard_v3
import modules.auth_engine as auth_engine

# 1. CONFIGURAÇÃO (OBRIGATÓRIO SER A PRIMEIRA LINHA)
st.set_page_config(
    page_title="Intelligence Flow",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. INICIALIZAÇÃO DE ESTADO
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# 3. LÓGICA DE NAVEGAÇÃO
# O usuário escolhe no menu se quer ver o site ou entrar na mesa
st.sidebar.markdown("### Navegação")
page = st.sidebar.radio("Ir para:", ["🏠 Institucional", "🔐 Mesa de Operações"])

if page == "🏠 Institucional":
    # Carrega a Landing Page Fantástica (Pública)
    dashboard_v3.show_landing_page()

elif page == "🔐 Mesa de Operações":
    # Lógica de Login (Área Privada)
   # ... dentro do if da Área de Membros ...

if hasattr(auth_engine, 'get_authenticator'):
    authenticator = auth_engine.get_authenticator()
    
    # COMANDO PARA A VERSÃO 0.3.2 (Simples e Funcional)
    name, authentication_status, username = authenticator.login('Login', 'main')
    
    if st.session_state["authentication_status"]:
        # ... código de sucesso ...
        authenticator.logout('Sair', 'sidebar')
        st.write(f'Bem-vindo *{name}*')
        # ... carregar mesa ...
            
            # Placeholder para os gráficos reais de trading
            st.info("Aqui seriam carregados os gráficos de VWAP, Bandas e Fluxo em Tempo Real.")
            
            col1, col2 = st.columns(2)
            col1.metric("Saldo Simulado", "R$ 100.000,00", "+2.5%")
            col2.metric("Risco Diário", "Baixo", "Ok")
            
        elif st.session_state["authentication_status"] == False:
            st.error('Usuário ou senha incorretos.')
        elif st.session_state["authentication_status"] == None:
            st.warning('Por favor, faça login para acessar os dados sensíveis.')
            
    else:
        st.error("Erro crítico: Motor de autenticação não encontrado.")

