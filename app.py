import streamlit as st
import modules.dashboard_v3 as dashboard_v3
import modules.auth_engine as auth_engine
import modules.ui_styles as ui_styles
import modules.trading_desk as trading_desk

# CONFIG
st.set_page_config(page_title="Intelligence Flow", page_icon="💠", layout="wide")
ui_styles.apply_design()

# SESSION STATE
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'authentication_status' not in st.session_state: st.session_state['authentication_status'] = None

# MENU
c1, c2 = st.columns([1, 3])
with c1:
    st.markdown("<h3 style='margin:0; color:#fff;'>INTELLIGENCE FLOW</h3>", unsafe_allow_html=True)
with c2:
    b1, b2, b3 = st.columns(3)
    if b1.button("ECOSSISTEMA"): st.session_state.page = 'home'
    if b2.button("SOLUÇÕES"): st.session_state.page = 'home'
    if b3.button("ÁREA DO TRADER"): st.session_state.page = 'trader'

st.markdown("---")

# ROUTING
if st.session_state.page == 'home':
    dashboard_v3.show_landing_page()

elif st.session_state.page == 'trader':
    authenticator = auth_engine.get_authenticator()
    
    # --- CORREÇÃO DO ERRO 'CANNOT UNPACK' ---
    # Simplesmente chamamos o login. O resultado vai para st.session_state
    try:
        authenticator.login()
    except Exception as e:
        pass # Ignora erro de renderização se houver

    # VERIFICAÇÃO SEGURA
    if st.session_state.get('authentication_status'):
        # Logado com Sucesso
        c_user, c_out = st.columns([6, 1])
        with c_user:
            st.success(f"Terminal Ativo: {st.session_state.get('name')}")
        with c_out:
            authenticator.logout('Logoff', 'main')
        
        trading_desk.show_desk()
        
    elif st.session_state.get('authentication_status') is False:
        st.error('Acesso Negado: Usuário ou Senha incorretos.')
        
    elif st.session_state.get('authentication_status') is None:
        st.info('Acesso Restrito ao Núcleo de Processamento.')
        st.markdown("""
        <div style="font-size:0.8rem; color:#64748b; text-align:center;">
            Credenciais de Acesso Institucional Necessárias<br>
            (Teste: admin / 123)
        </div>
        """, unsafe_allow_html=True)

# FOOTER
ui_styles.show_footer_cnpj()
