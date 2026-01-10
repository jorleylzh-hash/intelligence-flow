import streamlit as st
import modules.dashboard_v3 as dashboard_v3
import modules.auth_engine as auth_engine
import modules.ui_styles as ui_styles
import modules.trading_desk as trading_desk

# CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Intelligence Flow", page_icon="💠", layout="wide")
ui_styles.apply_design()

# ESTADO DA SESSÃO
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'authentication_status' not in st.session_state: st.session_state['authentication_status'] = None

# MENU SUPERIOR
c_header = st.container()
with c_header:
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown("<h3 style='margin:0; color:#fff;'>INTELLIGENCE FLOW</h3>", unsafe_allow_html=True)
    with c2:
        b1, b2, b3 = st.columns(3)
        if b1.button("ECOSSISTEMA"): st.session_state.page = 'home'
        if b2.button("SOLUÇÕES"): st.session_state.page = 'home'
        if b3.button("ÁREA DO TRADER"): st.session_state.page = 'trader'
    st.markdown("---")

# ROTEAMENTO
if st.session_state.page == 'home':
    dashboard_v3.show_landing_page()

elif st.session_state.page == 'trader':
    
    # Instancia o autenticador
    authenticator = auth_engine.get_authenticator()
    
    # --- CORREÇÃO DO ERRO DE LOGIN ---
    # Não tentamos 'desempacotar' (name, status = ...) imediatamente
    # Deixamos o widget rodar e verificamos o session_state depois
    try:
        authenticator.login()
    except Exception as e:
        # Se der erro visual, ignoramos para não crashar a tela, pois o estado pode já estar salvo
        pass

    # VERIFICAÇÃO DE ESTADO (A forma segura)
    if st.session_state.get('authentication_status'):
        # USUÁRIO LOGADO
        c_user, c_out = st.columns([6, 1])
        with c_user:
            st.success(f"Bem-vindo, {st.session_state.get('name')}")
        with c_out:
            authenticator.logout('Sair', 'main')
            
        # MOSTRA A MESA
        trading_desk.show_desk()
        
    elif st.session_state.get('authentication_status') is False:
        st.error('Usuário ou senha incorretos')
        
    elif st.session_state.get('authentication_status') is None:
        st.info('Área Restrita. Por favor, identifique-se.')
        st.caption("Admin / 123")

# RODAPÉ COM CNPJ CORRETO
ui_styles.show_footer_cnpj()
