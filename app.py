import streamlit as st
import time
import random
from datetime import datetime

# IMPORTS DOS MÓDULOS
import modules.landing_page as landing_page
import modules.ecosystem as ecosystem
import modules.solutions as solutions
import modules.ui_styles as ui_styles
import modules.trading_desk as trading_desk
import modules.notifications as notifications # Novo módulo de disparo

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Intelligence Flow", page_icon="💠", layout="wide")
ui_styles.apply_design()

# --- GESTÃO DE ESTADO (SESSION STATE) ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'auth_status' not in st.session_state: st.session_state.auth_status = False
if 'otp_code' not in st.session_state: st.session_state.otp_code = None
if 'otp_email' not in st.session_state: st.session_state.otp_email = ""
if 'last_otp_time' not in st.session_state: st.session_state.last_otp_time = 0
if 'login_step' not in st.session_state: st.session_state.login_step = 1 # 1=Email, 2=Código

# --- MENU DE NAVEGAÇÃO ---
st.markdown("<div class='nav-container'>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("🏠 PÁGINA INICIAL"): st.session_state.page = 'home'
with c2:
    if st.button("💠 ECOSSISTEMA"): st.session_state.page = 'ecosystem'
with c3:
    if st.button("💎 SOLUÇÕES"): st.session_state.page = 'solutions'
with c4:
    if st.button("🔐 ÁREA DO TRADER"): st.session_state.page = 'trader'
st.markdown("</div>", unsafe_allow_html=True)

# --- ROTEAMENTO DE PÁGINAS ---
if st.session_state.page == 'home':
    landing_page.show_landing_page()

elif st.session_state.page == 'ecosystem':
    ecosystem.show_ecosystem()

elif st.session_state.page == 'solutions':
    solutions.show_solutions()

elif st.session_state.page == 'trader':
    
    # SE JÁ ESTIVER LOGADO
    if st.session_state.auth_status:
        c_usr, c_out = st.columns([6, 1])
        with c_usr: 
            st.success(f"Terminal Ativo | Usuário: {st.session_state.otp_email}")
        with c_out: 
            if st.button("LOGOFF", type="primary"):
                st.session_state.auth_status = False
                st.session_state.login_step = 1
                st.session_state.otp_code = None
                st.rerun()
        
        trading_desk.show_desk()

    # SE NÃO ESTIVER LOGADO (PROCESSO OTP)
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            st.markdown("""
            <div style="background:#1e293b; padding:30px; border-radius:10px; border:1px solid #334155; text-align:center;">
                <h3 style="color:white; margin-bottom:5px;">Acesso Institucional</h3>
                <p style="color:#94a3b8; font-size:0.9rem;">Autenticação via Token (OTP)</p>
            </div>
            """, unsafe_allow_html=True)
            
            # --- ETAPA 1: DIGITAR E-MAIL ---
            if st.session_state.login_step == 1:
                email_input = st.text_input("Digite seu e-mail corporativo", placeholder="ex: trader@intelligenceflow.com")
                
                if st.button("ENVIAR CÓDIGO DE ACESSO", type="primary", use_container_width=True):
                    if "@" in email_input and "." in email_input:
                        # Gera código de 4 dígitos
                        code = str(random.randint(1000, 9999))
                        
                        # Atualiza Estado
                        st.session_state.otp_code = code
                        st.session_state.otp_email = email_input
                        st.session_state.last_otp_time = time.time()
                        
                        # Envia E-mail
                        with st.spinner("Enviando token de segurança..."):
                            sent = notifications.send_otp_email(email_input, code)
                            
                        if sent:
                            st.session_state.login_step = 2
                            st.success("Código enviado! Verifique sua caixa de entrada.")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Falha ao enviar e-mail. Verifique a API Key no módulo notifications.")
                    else:
                        st.warning("Por favor, insira um e-mail válido.")

            # --- ETAPA 2: DIGITAR CÓDIGO ---
            elif st.session_state.login_step == 2:
                st.info(f"Código enviado para: **{st.session_state.otp_email}**")
                
                # Input do Código
                user_code = st.text_input("Informe o código de 4 dígitos", max_chars=4, placeholder="0000")
                
                # Botão Verificar
                if st.button("ACESSAR TERMINAL", type="primary", use_container_width=True):
                    if user_code == st.session_state.otp_code:
                        st.session_state.auth_status = True
                        st.success("Autenticado com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Código incorreto.")

                # Lógica de Reenvio (Timer 45s)
                time_elapsed = time.time() - st.session_state.last_otp_time
                time_remaining = 45 - int(time_elapsed)
                
                st.markdown("---")
                
                if time_remaining > 0:
                    st.caption(f"Aguarde {time_remaining}s para solicitar novo código.")
                    st.button(f"Reenviar Código ({time_remaining}s)", disabled=True, use_container_width=True)
                else:
                    if st.button("REENVIAR CÓDIGO AGORA", use_container_width=True):
                        # Gera novo código
                        new_code = str(random.randint(1000, 9999))
                        st.session_state.otp_code = new_code
                        st.session_state.last_otp_time = time.time()
                        
                        # Reenvia
                        notifications.send_otp_email(st.session_state.otp_email, new_code)
                        st.success("Novo código enviado!")
                        time.sleep(1)
                        st.rerun()
                
                # Opção de trocar e-mail
                if st.button("Voltar / Trocar E-mail", type="secondary", use_container_width=True):
                    st.session_state.login_step = 1
                    st.rerun()

# --- RODAPÉ ---
ui_styles.show_footer_cnpj()
