import streamlit as st
import modules.dashboard_v3 as dashboard_v3
import modules.auth_engine as auth_engine

# 1. Configuração Inicial
st.set_page_config(page_title="Intelligence Flow", page_icon="💠", layout="wide", initial_sidebar_state="collapsed")

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# 2. Navegação
st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para:", ["🏠 Institucional", "📈 Área do Trader"])

if page == "🏠 Institucional":
    # Carrega a página NOVA com gráficos 60fps
    dashboard_v3.show_landing_page()

elif page == "📈 Área do Trader":
    if hasattr(auth_engine, 'get_authenticator'):
        authenticator = auth_engine.get_authenticator()
        
        # --- CORREÇÃO DO ERRO 'MULTIPLE FORMS' ---
        # Adicionamos key='login_unique' para garantir que não haja conflito
        try:
            name, authentication_status, username = authenticator.login(location='main', key='login_unique')
        except TypeError:
            # Fallback para versões diferentes da lib
            name, authentication_status, username = authenticator.login(key='login_unique')

        if st.session_state["authentication_status"]:
            authenticator.logout('Sair', 'sidebar')
            st.title(f"Mesa de Operações | {name}")
            st.success("✅ Acesso Liberado: Feed de Dados em Tempo Real Ativo.")
            
            # Placeholder da Mesa
            c1, c2 = st.columns(2)
            c1.metric("Saldo", "R$ 50.000,00", "+1.5%")
            c2.metric("Latência", "12ms", "Estável")
            
        elif st.session_state["authentication_status"] == False:
            st.error('Usuário ou senha incorretos.')
        elif st.session_state["authentication_status"] == None:
            st.info('Por favor, faça login para acessar.')
    else:
        st.error("Erro no módulo de autenticação.")
