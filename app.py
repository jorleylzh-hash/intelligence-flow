import streamlit as st
import modules.landing_page as landing_page # Mudou de dashboard_v3 para landing_page
import modules.ecosystem as ecosystem         # Novo
import modules.solutions as solutions         # Novo
import modules.auth_engine as auth_engine
import modules.ui_styles as ui_styles
import modules.trading_desk as trading_desk

# CONFIGURAÇÃO
st.set_page_config(page_title="Intelligence Flow", page_icon="💠", layout="wide")
ui_styles.apply_design()

# STATE
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'authentication_status' not in st.session_state: st.session_state['authentication_status'] = None

# MENU SUPERIOR ATUALIZADO
st.markdown("<div class='nav-container'>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("🏠 PÁGINA INICIAL"): st.session_state.page = 'home'
with c2:
    if st.button("💠 ECOSSISTEMA"): st.session_state.page = 'ecosystem'
with c3:
    if st.button("💎 SOLUÇÕES"): st.session_state.page = 'solutions'
with c4:
    if st.button("📈 ÁREA DO TRADER"): st.session_state.page = 'trader'
st.markdown("</div>", unsafe_allow_html=True)

# ROTEAMENTO
if st.session_state.page == 'home':
    landing_page.show_landing_page()

elif st.session_state.page == 'ecosystem':
    ecosystem.show_ecosystem()

elif st.session_state.page == 'solutions':
    solutions.show_solutions()

elif st.session_state.page == 'trader':
    authenticator = auth_engine.get_authenticator()
    try:
        authenticator.login()
    except: pass

    if st.session_state.get('authentication_status'):
        c_usr, c_out = st.columns([6, 1])
        with c_usr: st.success(f"Logado: {st.session_state.get('name')}")
        with c_out: authenticator.logout('Sair', 'main')
        trading_desk.show_desk()
    elif st.session_state.get('authentication_status') is False:
        st.error('Credenciais Inválidas')
    elif st.session_state.get('authentication_status') is None:
        st.info('Acesso Restrito ao Sistema HFT.')

# RODAPÉ
ui_styles.show_footer_cnpj()
