import streamlit as st
import time
import random
from datetime import datetime
import os

# --- IMPORTAÇÃO DOS MÓDULOS ---
import modules.landing_page as landing_page
import modules.ecosystem as ecosystem
import modules.solutions as solutions
import modules.ui_styles as ui_styles
import modules.trading_desk as trading_desk
import modules.notifications as notifications
import modules.simulator as simulator
import modules.splash as splash

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Intelligence Flow", page_icon="💠", layout="wide")

# Splash Screen e Estilos
splash.show_splash_screen()
ui_styles.apply_design()

# --- GESTÃO DE ESTADO ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'auth_status' not in st.session_state: st.session_state.auth_status = False
if 'otp_code' not in st.session_state: st.session_state.otp_code = None
if 'otp_email' not in st.session_state: st.session_state.otp_email = ""
if 'login_step' not in st.session_state: st.session_state.login_step = 1

# --- MENU DE NAVEGAÇÃO ---
st.markdown("<div class='nav-container'>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1: 
    if st.button("🏠 INÍCIO", use_container_width=True): st.session_state.page = 'home'
with c2: 
    if st.button("💠 ECOSSISTEMA", use_container_width=True): st.session_state.page = 'ecosystem'
with c3: 
    if st.button("💎 SOLUÇÕES", use_container_width=True): st.session_state.page = 'solutions'
with c4: 
    if st.button("🔐 TRADER", use_container_width=True): st.session_state.page = 'trader'
with c5: 
    if st.button("🕹️ SIMULADOR", use_container_width=True): st.session_state.page = 'simulator'
st.markdown("</div>", unsafe_allow_html=True)

# --- ROTEAMENTO ---
if st.session_state.page == 'home':
    landing_page.show_landing_page()

elif st.session_state.page == 'ecosystem':
    ecosystem.show_ecosystem()

elif st.session_state.page == 'solutions':
    solutions.show_solutions()

elif st.session_state.page == 'simulator':
    simulator.render_simulator()

elif st.session_state.page == 'trader':
    # Lógica de Login
    if st.session_state.auth_status:
        c_usr, c_out = st.columns([6, 1])
        with c_usr: st.success(f"Terminal Ativo | Usuário: {st.session_state.otp_email}")
        with c_out: 
            if st.button("LOGOFF", type="primary"):
                st.session_state.auth_status = False
                st.session_state.login_step = 1
                st.rerun()
        
        trading_desk.render_trading_desk()

    else:
        # TELA DE LOGIN
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("<h3 style='text-align:center;'>Acesso Institucional</h3>", unsafe_allow_html=True)
            
            if st.session_state.login_step == 1:
                email_input = st.text_input("E-mail corporativo", key="login_email")
                if st.button("ENVIAR CÓDIGO", type="primary", use_container_width=True):
                    if "@" in email_input:
                        code = str(random.randint(1000, 9999))
                        st.session_state.otp_code = code
                        st.session_state.otp_email = email_input
                        try: notifications.send_otp_email(email_input, code)
                        except: st.warning(f"Modo Debug: Código {code}")
                        st.session_state.login_step = 2
                        st.rerun()
                    else:
                        st.warning("E-mail inválido")
            
            elif st.session_state.login_step == 2:
                st.info(f"Código enviado para: {st.session_state.otp_email}")
                user_code = st.text_input("Código", max_chars=4, key="login_code")
                if st.button("ENTRAR", type="primary", use_container_width=True):
                    if user_code == st.session_state.otp_code:
                        st.session_state.auth_status = True
                        st.rerun()
                    else:
                        st.error("Código incorreto")
                if st.button("Voltar"):
                    st.session_state.login_step = 1
                    st.rerun()

ui_styles.show_compliance_footer()
