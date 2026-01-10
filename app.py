import streamlit as st
import modules.dashboard_v3 as dashboard_v3
import modules.pitch_page as pitch_page
import modules.trading_desk as trading_desk
import modules.auth_engine as auth_engine

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA (Deve ser sempre a primeira linha)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Intelligence Flow",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. INICIALIZAÇÃO DE ESTADO (SESSION STATE)
# -----------------------------------------------------------------------------
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL (MENU DE NAVEGAÇÃO)
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 🧭 Navegação")

# Definição das Rotas
selection = st.sidebar.radio(
    "Ir para:", 
    ["🏠 Página Inicial", "💎 Por que Intelligence Flow?", "📈 Área do Trader"]
)

# Botão de Logout (Só aparece se estiver logado)
if st.session_state.get('authentication_status'):
    st.sidebar.markdown("---")
    # Nota: O logout será renderizado pelo authenticator dentro da lógica abaixo

# -----------------------------------------------------------------------------
# 4. ROTEAMENTO DE PÁGINAS (LOGIC CORE)
# -----------------------------------------------------------------------------

# === ROTA 1: LANDING PAGE (PÚBLICA) ===
if selection == "🏠 Página Inicial":
    try:
        dashboard_v3.show_landing_page()
    except Exception as e:
        st.error(f"Erro ao carregar Landing Page: {e}")

# === ROTA 2: PITCH DE VENDAS (PÚBLICA) ===
elif selection == "💎 Por que Intelligence Flow?":
    try:
        pitch_page.show_pitch()
    except Exception as e:
        st.error(f"Erro ao carregar Página de Vendas: {e}")

# === ROTA 3: ÁREA DO TRADER (PRIVADA/LOGIN) ===
elif selection == "📈 Área do Trader":
    
    # Verifica se o motor de autenticação existe
    if hasattr(auth_engine, 'get_authenticator'):
        authenticator = auth_engine.get_authenticator()
        
        # --- BLOCO DE LOGIN (BLINDADO CONTRA ERROS) ---
        # Usamos try/except para garantir compatibilidade com versões diferentes da lib
        # A chave 'key' evita o erro "Duplicate Widget Key"
        try:
            name, authentication_status, username = authenticator.login(location='main', key='login_unique_form')
        except TypeError:
            # Fallback caso a versão instalada não aceite 'location'
            name, authentication_status, username = authenticator.login(key='login_unique_form')

        # --- LÓGICA PÓS-LOGIN ---
        if st.session_state["authentication_status"]:
            # 1. Botão de Sair na Sidebar
            authenticator.logout('Sair', 'sidebar')
            
            # 2. Carrega a Mesa de Operações (Trading Desk)
            try:
                trading_desk.show_desk()
            except Exception as e:
                st.error(f"Erro ao carregar Mesa de Operações: {e}")
                st.info("Verifique se o módulo 'trading_desk.py' foi criado corretamente.")
            
        elif st.session_state["authentication_status"] == False:
            st.error('❌ Usuário ou senha incorretos.')
            
        elif st.session_state["authentication_status"] == None:
            st.info('🔒 Esta é uma área restrita. Por favor, insira suas credenciais.')
            
    else:
        st.error("Erro crítico: O módulo 'auth_engine' falhou ao carregar.")

# -----------------------------------------------------------------------------
# 5. RODAPÉ GLOBAL (Opcional)
# -----------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.caption("Intelligence Flow v2.5 © 2026")
