import streamlit as st
import yfinance as yf  # <--- Importante ter este import
import os
import shutil

# --- CORREÇÃO DE EMERGÊNCIA PARA O RENDER ---
# Define o cache do yfinance para a pasta temporária do Linux
# Isso resolve o erro 'database is locked'
cache_dir = "/tmp/yf_cache"
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)  # Limpa cache antigo se existir
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
    
yf.set_tz_cache_location(cache_dir)
# --------------------------------------------

import modules.dashboard_v3 as dashboard_v3
import modules.trading_desk as trading_desk
import modules.auth_engine as auth_engine
import modules.ui_styles as ui_styles

# ... (O restante do seu código app.py continua igual abaixo) ...

# 1. SETUP INICIAL
st.set_page_config(page_title="Intelligence Flow", page_icon="💠", layout="wide")
ui_styles.apply_design()

# 2. GERENCIAMENTO DE ESTADO
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'authentication_status' not in st.session_state: st.session_state['authentication_status'] = None

# 3. MENU SUPERIOR PROFISSIONAL (SEM ÍCONES AMADORES)
c_brand, c_nav = st.columns([1, 2])

with c_brand:
    # Apenas texto elegante
    st.markdown("<h3 style='margin:0; padding-top:5px; color:#f8fafc;'>INTELLIGENCE FLOW</h3>", unsafe_allow_html=True)

with c_nav:
    # Botões de Texto Limpo
    col1, col2, col3 = st.columns(3)
    if col1.button("ECOSSISTEMA"):
        st.session_state.page = 'home'
    if col2.button("SOLUÇÕES IA"):
        st.session_state.page = 'solutions'
    if col3.button("ÁREA DO TRADER"):
        st.session_state.page = 'trader'

st.markdown("---")

# 4. ROTEAMENTO BLINDADO

# === PÁGINA HOME (O Long Scroll Educacional) ===
if st.session_state.page == 'home':
    dashboard_v3.show_landing_page()
    
    # CTA Final
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("ACESSAR TERMINAL DE OPERAÇÕES", type="primary", use_container_width=True):
            st.session_state.page = 'trader'
            st.rerun()

# === PÁGINA ÁREA DO TRADER (LOGIN SEM ERRO) ===
elif st.session_state.page == 'trader':
    
    # SE JÁ ESTIVER LOGADO -> MOSTRA A MESA
    if st.session_state.get('authentication_status'):
        # Header Logado
        c_logout_info, c_logout_btn = st.columns([5, 1])
        with c_logout_info:
            st.success(f"Conexão Segura Estabelecida: {st.session_state['name']}")
        
        # O logout do authenticator precisa ser chamado aqui
        if hasattr(auth_engine, 'get_authenticator'):
            authenticator = auth_engine.get_authenticator()
            with c_logout_btn:
                authenticator.logout('SAIR', 'main')
        
        # Carrega a Mesa
        trading_desk.show_desk()

    # SE NÃO ESTIVER LOGADO -> MOSTRA O LOGIN
    else:
        st.markdown("<br><br>", unsafe_allow_html=True)
        c_log1, c_log2, c_log3 = st.columns([1, 1, 1])
        
        with c_log2: # Centraliza o login
            st.markdown("<h3 style='text-align:center;'>ACESSO RESTRITO</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-size:0.9rem;'>Identifique-se para acessar o núcleo de processamento.</p>", unsafe_allow_html=True)
            
            if hasattr(auth_engine, 'get_authenticator'):
                authenticator = auth_engine.get_authenticator()
                
                # --- CORREÇÃO DO BUG: CHAMADA SIMPLES ---
                # Sem key manual, sem location se não precisar.
                try:
                    name, authentication_status, username = authenticator.login()
                except Exception as e:
                    st.error(f"Erro no módulo de login: {e}")

                if st.session_state.get('authentication_status') is False:
                    st.error('Credenciais Inválidas.')
                elif st.session_state.get('authentication_status') is None:
                    st.info('Aguardando credenciais...')

# 5. RODAPÉ CNPJ
ui_styles.show_footer_cnpj()


