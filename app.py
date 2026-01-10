import streamlit as st
import yfinance as yf
import os
import shutil

# --- VACINA PARA O RENDER (CRÍTICO) ---
# Desabilita o cache do yfinance para evitar "database is locked"
# Força o uso de diretório temporário se necessário, mas tenta desativar primeiro.
try:
    yf.pdr_override()
except:
    pass
    
# Forçar cache no /tmp ou desativar
cache_dir = "/tmp/yf_cache"
if os.path.exists(cache_dir):
    try:
        shutil.rmtree(cache_dir)
    except:
        pass
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir, exist_ok=True)
yf.set_tz_cache_location(cache_dir)
# -------------------------------------

import modules.dashboard_v3 as dashboard_v3
import modules.auth_engine as auth_engine
import modules.ui_styles as ui_styles
import modules.trading_desk as trading_desk

st.set_page_config(page_title="Intelligence Flow", page_icon="💠", layout="wide")
ui_styles.apply_design()

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'authentication_status' not in st.session_state: st.session_state['authentication_status'] = None

# MENU
c1, c2 = st.columns([1, 3])
with c1:
    st.markdown("<h3 style='margin:0; color:#fff;'>INTELLIGENCE FLOW</h3>", unsafe_allow_html=True)
with c2:
    b1, b2, b3 = st.columns(3)
    if b1.button("ECOSSISTEMA"): st.session_state.page = 'home'
    if b2.button("SOLUÇÕES"): st.session_state.page = 'home' # Placeholder
    if b3.button("ÁREA DO TRADER"): st.session_state.page = 'trader'

st.markdown("---")

# ROTEAMENTO
if st.session_state.page == 'home':
    dashboard_v3.show_landing_page()

elif st.session_state.page == 'trader':
    # LÓGICA DE LOGIN BLINDADA
    if st.session_state.get('authentication_status'):
        # LOGADO
        authenticator = auth_engine.get_authenticator()
        authenticator.logout('Sair', 'main')
        trading_desk.show_desk()
    else:
        # NÃO LOGADO
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            st.info("Acesso Restrito - Área de Clientes")
            # AQUI ESTAVA O ERRO DE CACHE.
            # Agora get_authenticator() não tem cache, então isso funciona.
            authenticator = auth_engine.get_authenticator()
            try:
                # Login simples, sem keys duplicadas
                name, authentication_status, username = authenticator.login()
            except Exception as e:
                st.error(f"Erro de renderização: {e}")
            
            if st.session_state.get('authentication_status') is False:
                st.error('Credenciais Inválidas')

# RODAPÉ ESTÁTICO DO SISTEMA
ui_styles.show_footer_cnpj()
