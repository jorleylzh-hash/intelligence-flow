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
st.sidebar.markdown("### Navegação")
page = st.sidebar.radio("Ir para:", ["🏠 Institucional", "🔐 Mesa de Operações"])

if page == "🏠 Institucional":
    # Verifica se a função existe para evitar erro
    if hasattr(dashboard_v3, 'show_landing_page'):
        dashboard_v3.show_landing_page()
    else:
        st.error("Erro: A página institucional não foi encontrada no módulo.")

elif page == "🔐 Mesa de Operações":
    # --- AQUI ESTAVA O ERRO DE INDENTAÇÃO ---
    # Tudo abaixo deste elif precisa ter 4 espaços de recuo
    if hasattr(auth_engine, 'get_authenticator'):
        authenticator = auth_engine.get_authenticator()
        
        # COMANDO DE LOGIN (Versão 0.3.2)
        # Se você atualizou o requirements.txt, este comando vai funcionar:
        name, authentication_status, username = authenticator.login('Login', 'main')
        
        if st.session_state["authentication_status"]:
            # --- ÁREA LOGADA ---
            authenticator.logout('Sair', 'sidebar')
            st.title(f"Mesa de Operações | Bem-vindo, {name}")
            st.markdown("---")
            st.success("✅ Conexão segura estabelecida.")
            
            # Aqui entra o código da Mesa (Gráficos, boletas, etc.)
            col1, col2 = st.columns(2)
            col1.metric("Saldo", "R$ 100.000,00", "+1.2%")
            col2.metric("Latência", "24ms", "-5ms")
            
        elif st.session_state["authentication_status"] == False:
            st.error('Usuário ou senha incorretos.')
            
        elif st.session_state["authentication_status"] == None:
            st.warning('Por favor, insira suas credenciais de acesso.')
            
    else:
        st.error("Erro crítico: O motor de autenticação (auth_engine) falhou ao carregar.")
