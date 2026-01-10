import streamlit as st
import modules.dashboard_v3 as dashboard_v3
import modules.pitch_page as pitch_page
import modules.trading_desk as trading_desk
import modules.auth_engine as auth_engine
import modules.ui_styles as ui_styles # <--- Importando o visual novo

# 1. CONFIGURAÇÃO (Full Screen)
st.set_page_config(
    page_title="Intelligence Flow",
    page_icon="💠",
    layout="wide"
)

# 2. APLICA O VISUAL (Imagem de Fundo + CSS)
ui_styles.apply_design()

# 3. GERENCIADOR DE NAVEGAÇÃO (Sem Sidebar)
# Inicializa qual página estamos vendo
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "home"

# Função para trocar de página via botões
def set_page(page_name):
    st.session_state['current_page'] = page_name

# --- MENU SUPERIOR (HEADER) ---
c_logo, c_nav = st.columns([1, 2])

with c_logo:
    # Título/Logo clicável (leva para home)
    st.markdown("<h3 style='margin:0; padding-top:10px;'>💠 Intelligence Flow</h3>", unsafe_allow_html=True)

with c_nav:
    # Botões de Navegação (Estilo Menu)
    b1, b2, b3 = st.columns(3)
    if b1.button("🏠 Início", use_container_width=True):
        set_page("home")
    if b2.button("💎 Soluções", use_container_width=True):
        set_page("pitch")
    if b3.button("📈 Área do Trader", use_container_width=True):
        set_page("trader")

st.markdown("---")

# 4. ROTEAMENTO DE PÁGINAS

# === PÁGINA: HOME ===
if st.session_state['current_page'] == "home":
    dashboard_v3.show_landing_page()
    
    # Botão Extra no final da Home para levar ao Login
    st.markdown("<br>", unsafe_allow_html=True)
    col_cta1, col_cta2, col_cta3 = st.columns([1,1,1])
    with col_cta2:
        if st.button("🚀 Acessar Mesa de Operações Agora", type="primary", use_container_width=True):
            set_page("trader")
            st.rerun()

# === PÁGINA: PITCH / SOLUÇÕES ===
elif st.session_state['current_page'] == "pitch":
    pitch_page.show_pitch()

# === PÁGINA: ÁREA DO TRADER (LOGIN) ===
elif st.session_state['current_page'] == "trader":
    
    # Container para isolar o login e evitar erros de redesenho
    login_container = st.container()
    
    with login_container:
        if hasattr(auth_engine, 'get_authenticator'):
            authenticator = auth_engine.get_authenticator()
            
            # --- CORREÇÃO DEFINITIVA DO LOGIN ---
            # 1. Não usamos 'key'. Deixamos a lib gerar.
            # 2. Usamos 'location' apenas se necessário.
            try:
                name, authentication_status, username = authenticator.login(location='main')
            except TypeError:
                name, authentication_status, username = authenticator.login()

            # LÓGICA DE SUCESSO
            if st.session_state.get("authentication_status"):
                # Mostra botão de sair
                cols_logout = st.columns([6, 1])
                with cols_logout[1]:
                    authenticator.logout('Sair', 'main')
                
                # Mostra a Mesa
                st.success(f"Conectado como: {name}")
                trading_desk.show_desk()

            # LÓGICA DE FALHA
            elif st.session_state.get("authentication_status") is False:
                st.error('❌ Usuário ou senha incorretos.')
                
            elif st.session_state.get("authentication_status") is None:
                st.info('🔒 Área restrita. Insira suas credenciais.')
                st.caption("Usuário Teste: admin | Senha: 123")
                
        else:
            st.error("Erro crítico: auth_engine não carregado.")

# 5. RODAPÉ (CNPJ) - Sempre visível
ui_styles.show_footer_cnpj()
