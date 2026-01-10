import streamlit as st
import modules.dashboard_v3 as dashboard_v3
import modules.auth_engine as auth_engine

# 1. CONFIGURAÇÃO (Full Screen e Ícone)
st.set_page_config(
    page_title="Intelligence Flow",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ESTADO DE SESSÃO
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# 3. BARRA LATERAL (Menu)
st.sidebar.markdown("### Navegação")
# Mudança de nome solicitada: Mesa Proprietária -> Área do Trader
page = st.sidebar.radio("Ir para:", ["🏠 Página Institucional", "📈 Área do Trader"])

if page == "🏠 Página Institucional":
    dashboard_v3.show_landing_page()

elif page == "📈 Área do Trader":
    # Verifica o motor de autenticação
    if hasattr(auth_engine, 'get_authenticator'):
        authenticator = auth_engine.get_authenticator()
        
        # --- CORREÇÃO DO ERRO DE LOGIN ---
        # Na versão nova, não se passa mais 'Login' como primeiro argumento solto.
        # Usa-se apenas location='main' ou chama direto.
        try:
            name, authentication_status, username = authenticator.login(location='main')
        except TypeError:
            # Fallback caso a versão varie, mas o padrão moderno é esse:
            name, authentication_status, username = authenticator.login()
            
        if st.session_state["authentication_status"]:
            # USUÁRIO LOGADO
            authenticator.logout('Sair', 'sidebar')
            
            st.title(f"Área do Trader | {name}")
            st.markdown("---")
            st.success("✅ Conexão segura estabelecida com o servidor de dados.")
            
            # Exemplo de conteúdo da Área do Trader
            st.info("Bem-vindo à mesa de operações. Selecione o ativo no menu superior (Futuro).")
            
            # Simulando um painel rápido
            c1, c2, c3 = st.columns(3)
            c1.metric("Saldo Disponível", "R$ 152.450,00", "0.0%")
            c2.metric("P&L Diário", "R$ 3.240,00", "+2.1%")
            c3.metric("Risco/Retorno", "1:3", "Ideal")
            
        elif st.session_state["authentication_status"] == False:
            st.error('Usuário ou senha incorretos.')
            
        elif st.session_state["authentication_status"] == None:
            st.warning('Por favor, realize o login para acessar as ferramentas de trading.')
            
    else:
        st.error("Erro crítico: O sistema de autenticação não pode ser carregado.")
