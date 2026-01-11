import streamlit as st
import time
import random
from datetime import datetime

# --- IMPORTAÇÃO DOS MÓDULOS ---
# Certifique-se de que todos estes arquivos existem na pasta 'modules/'
import modules.landing_page as landing_page
import modules.ecosystem as ecosystem
import modules.solutions as solutions
import modules.ui_styles as ui_styles
import modules.trading_desk as trading_desk
import modules.notifications as notifications
import modules.simulator as simulator
import modules.splash as splash

# --- CONFIGURAÇÃO DA PÁGINA (Deve ser a primeira linha Streamlit) ---
st.set_page_config(page_title="Intelligence Flow", page_icon="💠", layout="wide")

# --- 1. ABERTURA CINEMATOGRÁFICA (SPLASH SCREEN) ---
# Executa a animação de entrada apenas na primeira carga
splash.show_splash_screen()

# --- 2. ESTILOS VISUAIS (CSS) ---
ui_styles.apply_design()

# --- 3. GESTÃO DE ESTADO (SESSION STATE) ---
# Inicializa variáveis globais se não existirem
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'auth_status' not in st.session_state: st.session_state.auth_status = False
if 'otp_code' not in st.session_state: st.session_state.otp_code = None
if 'otp_email' not in st.session_state: st.session_state.otp_email = ""
if 'last_otp_time' not in st.session_state: st.session_state.last_otp_time = 0
if 'login_step' not in st.session_state: st.session_state.login_step = 1

# --- 4. MENU DE NAVEGAÇÃO SUPERIOR ---
st.markdown("<div class='nav-container'>", unsafe_allow_html=True)

# Layout de 5 colunas para acesso rápido a todas as áreas
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button("🏠 INÍCIO", use_container_width=True): 
        st.session_state.page = 'home'
with c2:
    if st.button("💠 ECOSSISTEMA", use_container_width=True): 
        st.session_state.page = 'ecosystem'
with c3:
    if st.button("💎 SOLUÇÕES", use_container_width=True): 
        st.session_state.page = 'solutions'
with c4:
    # Área restrita (pede login)
    if st.button("🔐 TRADER", use_container_width=True): 
        st.session_state.page = 'trader'
with c5:
    # Simulador (Agora público para todos)
    if st.button("🕹️ SIMULADOR", use_container_width=True): 
        st.session_state.page = 'simulator'

st.markdown("</div>", unsafe_allow_html=True)

# --- 5. ROTEAMENTO DE PÁGINAS ---

if st.session_state.page == 'home':
    landing_page.show_landing_page()

elif st.session_state.page == 'ecosystem':
    ecosystem.show_ecosystem()

elif st.session_state.page == 'solutions':
    solutions.show_solutions()

elif st.session_state.page == 'simulator':
    # Chama o módulo do Simulador (Brapi + Monte Carlo)
    simulator.render_simulator()

elif st.session_state.page == 'trader':
    # --- LÓGICA DE LOGIN DA ÁREA TRADER ---
    if st.session_state.auth_status:
        # USUÁRIO LOGADO
        c_usr, c_out = st.columns([6, 1])
        with c_usr: 
            st.success(f"Terminal Ativo | Usuário: {st.session_state.otp_email}")
        with c_out: 
            if st.button("LOGOFF", type="primary"):
                st.session_state.auth_status = False
                st.session_state.login_step = 1
                st.session_state.otp_code = None
                st.rerun()
        
        # Renderiza o Trading Desk (Gráficos + IA)
        try:
            trading_desk.render_trading_desk()
        except AttributeError:
            # Fallback caso a função tenha nome antigo
            trading_desk.show_desk()

    else:
        # TELA DE LOGIN (NÃO LOGADO)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            st.markdown("""
            <div style="background:#1e293b; padding:30px; border-radius:10px; border:1px solid #334155; text-align:center;">
                <h3 style="color:white; margin-bottom:5px;">Acesso Institucional</h3>
                <p style="color:#94a3b8; font-size:0.9rem;">Autenticação via Token (OTP)</p>
            </div>
            """, unsafe_allow_html=True)
            
            # --- ETAPA 1: E-MAIL ---
            if st.session_state.login_step == 1:
                email_input = st.text_input("Digite seu e-mail corporativo", placeholder="ex: trader@intelligenceflow.com")
                
                if st.button("ENVIAR CÓDIGO DE ACESSO", type="primary", use_container_width=True):
                    if "@" in email_input and "." in email_input:
                        code = str(random.randint(1000, 9999))
                        
                        st.session_state.otp_code = code
                        st.session_state.otp_email = email_input
                        st.session_state.last_otp_time = time.time()
                        
                        with st.spinner("Enviando token de segurança..."):
                            # Tenta enviar e-mail real
                            try:
                                sent = notifications.send_otp_email(email_input, code)
                            except:
                                sent = False
                            
                            # MODO FALLBACK (Se o Resend falhar, mostra na tela para não travar)
                            if not sent:
                                st.warning(f"Modo Debug: Seu código é {code}")
                                sent = True

                        if sent:
                            st.session_state.login_step = 2
                            st.success("Código gerado!")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.warning("E-mail inválido.")

            # --- ETAPA 2: CÓDIGO OTP ---
            elif st.session_state.login_step == 2:
                st.info(f"Código enviado para: **{st.session_state.otp_email}**")
                
                user_code = st.text_input("Informe o código de 4 dígitos", max_chars=4, placeholder="0000")
                
                if st.button("ACESSAR TERMINAL", type="primary", use_container_width=True):
                    if user_code == st.session_state.otp_code:
                        st.session_state.auth_status = True
                        st.success("Autenticado com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Código incorreto.")
                
                if st.button("Voltar", type="secondary"):
                    st.session_state.login_step = 1
                    st.rerun()

# --- 6. RODAPÉ JURÍDICO (COMPLIANCE) ---
# Aparece em todas as páginas conforme regra da CVM
ui_styles.show_compliance_footer()
