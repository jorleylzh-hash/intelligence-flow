import streamlit as st
import modules.dashboard_v3 as dashboard_v3
import modules.auth_engine as auth_engine

# 1. Configuração
st.set_page_config(page_title="Intelligence Flow", page_icon="💠", layout="wide", initial_sidebar_state="collapsed")

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# 2. Menu
st.sidebar.markdown("### Navegação")
page = st.sidebar.radio("Ir para:", ["🏠 Página Institucional", "📈 Área do Trader"])

if page == "🏠 Página Institucional":
    dashboard_v3.show_landing_page()

elif page == "📈 Área do Trader":
    # O cache agora cuida de manter o objeto estável
    if hasattr(auth_engine, 'get_authenticator'):
        authenticator = auth_engine.get_authenticator()
        
        # Chamada SIMPLIFICADA (Sem keys conflitantes)
        try:
            name, authentication_status, username = authenticator.login(location='main')
        except:
            name, authentication_status, username = authenticator.login()

        if st.session_state["authentication_status"]:
            authenticator.logout('Sair', 'sidebar')
            st.title(f"Mesa de Operações | {name}")
            st.success("✅ Conexão Ativa.")
            
            # Painel Simples
            c1, c2 = st.columns(2)
            c1.metric("Saldo", "R$ 50.000,00", "+1.2%")
            c2.metric("Latência", "15ms", "OK")
            
        elif st.session_state["authentication_status"] == False:
            st.error('Usuário ou senha incorretos.')
        elif st.session_state["authentication_status"] == None:
            st.info('Faça login para acessar os sinais.')
