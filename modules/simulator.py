import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import requests
from datetime import datetime, timedelta
from streamlit.web.server.websocket_headers import _get_websocket_headers

# --- FUNÇÕES UTILITÁRIAS ---
def get_remote_ip():
    """Tenta identificar o IP do usuário para registro visual."""
    try:
        headers = _get_websocket_headers()
        if headers:
            x_forwarded_for = headers.get("X-Forwarded-For")
            if x_forwarded_for: return x_forwarded_for.split(",")[0]
        return "Visitante"
    except: return "N/A"

# --- FUNÇÕES DE DADOS (BRAPI & MONTE CARLO) ---

def fetch_brapi_history(ticker="PETR4"):
    """
    Busca histórico real na Brapi para usar no Replay.
    """
    # Tenta buscar 1 mês de dados diários
    url = f"https://brapi.dev/api/quote/{ticker}?range=1mo&interval=1d&fundamental=false"
    
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()['results'][0]['historicalDataPrice']
            df = pd.DataFrame(data)
            # Renomear para padrão interno (Capitalize)
            df = df.rename(columns={'date': 'Date', 'close': 'Close', 'high': 'High', 'low': 'Low', 'open': 'Open'})
            df['Date'] = pd.to_datetime(df['Date'], unit='s')
            return df.sort_values('Date')
    except Exception as e:
        st.warning(f"API Brapi indisponível ou limite atingido. Usando dados sintéticos.")
    
    # Fallback: Dados Sintéticos se a API falhar
    dates = pd.date_range(end=datetime.now(), periods=60, freq="D")
    price = 30.0 + np.cumsum(np.random.randn(60))
    return pd.DataFrame({"Date": dates, "Close": price, "Open": price, "High": price+0.5, "Low": price-0.5})

def run_monte_carlo(current_price, volatility, days_forecast=30, simulations=1000):
    """
    Executa Simulação de Monte Carlo (Movimento Browniano Geométrico).
    """
    dt = 1  # passo de tempo (1 dia)
    simulation_results = np.zeros((days_forecast, simulations))
    simulation_results[0] = current_price
    
    for t in range(1, days_forecast):
        # Fórmula: St = St-1 * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z)
        shock = np.random.normal(0, 1, simulations)
        drift = -0.5 * (volatility ** 2) * dt
        diffusion = volatility * np.sqrt(dt) * shock
        simulation_results[t] = simulation_results[t-1] * np.exp(drift + diffusion)
        
    return simulation_results

# --- INTERFACE PRINCIPAL DO SIMULADOR ---

def render_simulator():
    user_ip = get_remote_ip()
    
    # Header Público
    st.markdown(f"""
    <div style="background:#3b82f6; padding:10px; border-radius:5px; margin-bottom:20px; color:white;">
        <strong>🕹️ SIMULADOR OPEN ACCESS</strong> | IP: {user_ip} | Ferramentas de Estudo Liberadas
    </div>
    """, unsafe_allow_html=True)

    tab_replay, tab_montecarlo = st.tabs(["⏪ Market Replay (Brapi)", "🎲 Simulação Monte Carlo"])

    # ==============================================================================
    # ABA 1: MARKET REPLAY (DADOS HISTÓRICOS)
    # ==============================================================================
    with tab_replay:
        st.subheader("Simulador de Pregão (Dados Históricos)")
        
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            ticker_sim = st.selectbox("Ativo Base", ["PETR4", "VALE3", "WING26"], key="sim_ticker")
        
        # Inicializa o estado do Replay
        if 'replay_data' not in st.session_state: st.session_state.replay_data = None
        if 'replay_index' not in st.session_state: st.session_state.replay_index = 0
        if 'replay_running' not in st.session_state: st.session_state.replay_running = False

        # Botão de Carga
        with c2:
            st.write("") # Espaço visual
            if st.button("CARREGAR DADOS 📥"):
                with st.spinner(f"Baixando histórico de {ticker_sim}..."):
                    df = fetch_brapi_history(ticker_sim)
                    st.session_state.replay_data = df
                    st.session_state.replay_index = 0
                    st.session_state.replay_running = False
                    st.success(f"{len(df)} candles carregados!")

        # Player de Controle
        if st.session_state.replay_data is not None:
            df = st.session_state.replay_data
            max_idx = len(df) - 1
            
            # Barra de Controles
            cc1, cc2, cc3, cc4 = st.columns(4)
            with cc1:
                if st.button("▶️ PLAY"): st.session_state.replay_running = True
            with cc2:
                if st.button("⏸️ PAUSE"): st.session_state.replay_running = False
            with cc3:
                if st.button("⏹️ RESET"): 
                    st.session_state.replay_running = False
                    st.session_state.replay_index = 0
                    st.rerun()
            with cc4:
                velocidade = st.slider("Velocidade (ms)", 100, 2000, 500) / 1000.0

            # Lógica de Loop (Animação)
            chart_placeholder = st.empty()
            info_placeholder = st.empty()

            if st.session_state.replay_running:
                if st.session_state.replay_index < max_idx:
                    st.session_state.replay_index += 1
                    time.sleep(velocidade)
                    st.rerun()
                else:
                    st.session_state.replay_running = False

            # Renderiza o Gráfico com o corte atual
            curr_idx = st.session_state.replay_index
            df_slice = df.iloc[:curr_idx+1]
            
            # Gráfico Candle
            fig = go.Figure(data=[go.Candlestick(
                x=df_slice['Date'],
                open=df_slice['Open'], high=df_slice['High'],
                low=df_slice['Low'], close=df_slice['Close']
            )])
            fig.update_layout(template="plotly_dark", height=400, title=f"Replay: {ticker_sim}")
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            
            # Info Financeira
            last_candle = df_slice.iloc[-1]
            var_pct = ((last_candle['Close'] - last_candle['Open']) / last_candle['Open']) * 100
            cor_txt = "green" if var_pct >= 0 else "red"
            info_placeholder.markdown(f"📅 **{last_candle['Date'].strftime('%d/%m/%Y')}** | Preço: **R$ {last_candle['Close']:.2f}** | Var: <span style='color:{cor_txt}'>{var_pct:.2f}%</span>", unsafe_allow_html=True)

    # ==============================================================================
    # ABA 2: MONTE CARLO
    # ==============================================================================
    with tab_montecarlo:
        st.subheader("🎲 Projeção Estocástica (Monte Carlo)")
        st.markdown("Projeta 1.000 caminhos futuros baseados na volatilidade.")

        mc_col1, mc_col2 = st.columns([1, 3])
        
        with mc_col1:
            mc_price = st.number_input("Preço Atual (R$)", value=30.00)
            mc_vol = st.number_input("Volatilidade Anual (%)", value=35.0) / 100
            mc_days = st.slider("Dias para Projetar", 10, 90, 30)
            
            if st.button("RODAR SIMULAÇÃO ⚡"):
                daily_vol = mc_vol / np.sqrt(252)
                paths = run_monte_carlo(mc_price, daily_vol, mc_days, 1000)
                st.session_state.mc_paths = paths

        with mc_col2:
            if 'mc_paths' in st.session_state:
                paths = st.session_state.mc_paths
                
                fig_mc = go.Figure()
                
                # Plota amostra de caminhos
                for i in range(50):
                    fig_mc.add_trace(go.Scatter(y=paths[:, i], mode='lines', line=dict(width=1, color='rgba(59, 130, 246, 0.1)'), showlegend=False))
                
                # Estatísticas
                mean_path = np.mean(paths, axis=1)
                p95 = np.percentile(paths, 95, axis=1)
                p05 = np.percentile(paths, 5, axis=1)
                
                fig_mc.add_trace(go.Scatter(y=mean_path, mode='lines', name='Média', line=dict(
