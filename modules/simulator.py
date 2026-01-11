import streamlit as st
import pandas as pd
import numpy as np
import time
from streamlit.web.server.websocket_headers import _get_websocket_headers

# --- CONFIGURAÇÕES DE SEGURANÇA ---
MASTER_USER = "jorley.zimermann@intelligenceflow.pro"

def get_remote_ip():
    """
    Tenta obter o IP real do cliente, mesmo atrás do proxy do Render.
    """
    try:
        headers = _get_websocket_headers()
        if headers:
            # O Render e outros clouds passam o IP real neste cabeçalho
            x_forwarded_for = headers.get("X-Forwarded-For")
            if x_forwarded_for:
                # Pega o primeiro IP da lista (o do cliente)
                return x_forwarded_for.split(",")[0]
        return "IP Não Detectado"
    except Exception:
        return "Erro IP"

def check_security_clearance(email_atual):
    """
    Verifica se o usuário é o Master e valida o ambiente.
    """
    ip_atual = get_remote_ip()
    
    # 1. Verifica Email Master
    if email_atual != MASTER_USER:
        st.error(f"⛔ ACESSO NEGADO. Usuário {email_atual} não tem permissão nível Master.")
        st.stop()
        return False

    # 2. Exibição de Auditoria (IP)
    # Nota: Em produção, você pode descomentar a linha abaixo para bloquear IPs desconhecidos
    # if ip_atual not in ['SEU_IP_CASA', 'SEU_IP_ESCRITORIO']: st.stop()
    
    return True, ip_atual

# --- LÓGICA DO SIMULADOR ---
def generate_market_scenario(trend, volatility):
    """
    Gera dados fictícios baseados na tendência escolhida pelo Master.
    Trend: 'bull', 'bear', 'flat'
    """
    periods = 50
    start_price = 120000 # Base WING
    
    # Define o viés matemático
    if trend == 'bull': bias = 0.002
    elif trend == 'bear': bias = -0.002
    else: bias = 0.0
    
    # Gera Random Walk
    returns = np.random.normal(loc=bias, scale=volatility, size=periods)
    price_curve = start_price * (1 + returns).cumprod()
    
    # Cria DataFrame simulando a estrutura da B3
    times = pd.date_range(end=pd.Timestamp.now(), periods=periods, freq="5min").strftime("%H:%M")
    
    df = pd.DataFrame({
        "Hora": times,
        "WING26": price_curve,
        "PETR4": price_curve * 0.0003 + np.random.normal(0, 0.5, periods), # Correlacionado
        "VALE3": price_curve * 0.00025 - np.random.normal(0, 0.5, periods), # Divergente as vezes
        "DI1F27": 10.5 + np.random.normal(0, 0.05, periods) * (-1 if trend == 'bull' else 1) # Juros Inverso
    })
    
    return df

def render_simulator():
    # --- CAMADA DE SEGURANÇA ---
    email = st.session_state.get('otp_email', 'Desconhecido')
    autorizado, user_ip = check_security_clearance(email)
    
    if autorizado:
        st.markdown(f"""
        <div style="background:#22c55e; padding:10px; border-radius:5px; color:black; font-weight:bold; margin-bottom:20px;">
            🔓 MODO GOD: ACESSO MASTER LIBERADO <br>
            <span style="font-size:0.8em">IP Detectado: {user_ip} | Device Check: OK</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("## 🕹️ Simulador de Mercado & Backtest")
        st.warning("⚠️ Atenção: Os dados gerados aqui são SINTÉTICOS para fins de teste de estresse da plataforma.")

        col_conf, col_view = st.columns([1, 3])
        
        with col_conf:
            st.subheader("Configurar Cenário")
            cenario = st.selectbox("Tendência de Mercado", ["Bull Market (Alta)", "Bear Market (Baixa)", "Consolidação (Lateral)"])
            volatilidade = st.slider("Volatilidade (VIX)", 0.001, 0.020, 0.005, format="%.3f")
            
            if st.button("GERAR SIMULAÇÃO", type="primary"):
                trend_map = {'Bull Market (Alta)': 'bull', 'Bear Market (Baixa)': 'bear', 'Consolidação (Lateral)': 'flat'}
                df_sim = generate_market_scenario(trend_map[cenario], volatilidade)
                st.session_state['sim_data'] = df_sim
                st.success("Cenário Gerado!")

        with col_view:
            if 'sim_data' in st.session_state:
                df = st.session_state['sim_data']
                
                # Visualização Rápida
                st.line_chart(df.set_index("Hora")[["WING26", "PETR4", "VALE3"]])
                
                st.markdown("### Dados Brutos (JSON/CSV)")
                st.dataframe(df, height=200)
                
                st.info("ℹ️ Estes dados podem ser injetados no módulo 'Trading Desk' para testar a IA.")
