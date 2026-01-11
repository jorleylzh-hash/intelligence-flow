import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import requests
from datetime import datetime

# --- FUNÇÕES UTILITÁRIAS ---
def get_remote_ip():
    """
    Tenta identificar o IP do usuário de forma moderna e compatível.
    Remove o aviso 'deprecated' do Streamlit.
    """
    try:
        # Tenta o método novo (Streamlit 1.30+)
        if hasattr(st, "context") and hasattr(st.context, "headers"):
            headers = st.context.headers
            x_forwarded = headers.get("X-Forwarded-For")
            if x_forwarded: return x_forwarded.split(",")[0]
            
        # Fallback para método antigo (caso o servidor esteja desatualizado)
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        if headers:
            x_forwarded = headers.get("X-Forwarded-For")
            if x_forwarded: return x_forwarded.split(",")[0]
            
        return "Visitante"
    except: 
        return "N/A"

# --- FUNÇÕES DE DADOS ---
def fetch_brapi_history(ticker="PETR4"):
    url = f"https://brapi.dev/api/quote/{ticker}?range=1mo&interval=1d&fundamental=false"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()['results'][0]['historicalDataPrice']
            df = pd.DataFrame(data)
            df = df.rename(columns={'date': 'Date', 'close': 'Close', 'high': 'High', 'low': 'Low', 'open': 'Open'})
            df['Date'] = pd.to_datetime(df['Date'], unit='s')
            return df.sort_values('Date')
    except:
        pass
    
    # Fallback Sintético
    dates = pd.date_range(end=datetime.now(), periods=60, freq="D")
    price = 30.0 + np.cumsum(np.random.randn(60))
    return pd.DataFrame({"Date": dates, "Close": price, "Open": price, "High": price+0.5, "Low": price-0.5})

def run_monte_carlo(current_price, volatility, days_forecast=30, simulations=1000):
    dt = 1
    simulation_results = np.zeros((days_forecast, simulations))
    simulation_results[0] = current_price
    for t in range(1, days_forecast):
        shock = np.random.normal(0, 1, simulations)
        drift = -0.5 * (volatility ** 2) * dt
        diffusion = volatility * np.sqrt(dt) * shock
        simulation_results[t] = simulation_results[t-1] * np.exp(drift + diffusion)
    return simulation_results

# --- INTERFACE ---
def render_simulator():
    user_ip = get_remote_ip()
    
    st.markdown(f"""
    <div style="background:#3b82f6; padding:10px; border-radius:5px; margin-bottom:20px; color:white;">
        <strong>🕹️ SIMULADOR ATIVO</strong> | IP: {user_ip}
    </div>
    """, unsafe_allow_html=True)

    tab_replay, tab_montecarlo = st.tabs(["⏪ Market Replay", "🎲 Monte Carlo"])

    with tab_replay:
        c1, c2 = st.columns([1, 1])
        with c1: ticker_sim = st.selectbox("Ativo", ["PETR4", "VALE3", "WING26"])
        with c2: 
            if st.button("CARREGAR DADOS"):
                with st.spinner("Baixando..."):
                    st.session_state.replay_data = fetch_brapi_history(ticker_sim)
                    st.session_state.replay_index = 0
                    st.session_state.replay_running = False
                    st.success("Dados OK!")

        if st.session_state.get('replay_data') is not None:
            df = st.session_state.replay_data
            
            # Controles
            cc1, cc2, cc3 = st.columns(3)
            with cc1: 
                if st.button("▶️ PLAY"): st.session_state.replay_running = True
            with cc2: 
                if st.button("⏸️ PAUSE"): st.session_state.replay_running = False
            with cc3: 
                if st.button("⏹️ RESET"): 
                    st.session_state.replay_running = False
                    st.session_state.replay_index = 0
                    st.rerun()

            # Loop de Animação
            if st.session_state.replay_running and st.session_state.replay_index < len(df) - 1:
                st.session_state.replay_index += 1
                time.sleep(0.5) # Velocidade Fixa
                st.rerun()

            # Gráfico
            curr = st.session_state.replay_index
            df_slice = df.iloc[:curr+1]
            fig = go.Figure(data=[go.Candlestick(x=df_slice['Date'], open=df_slice['Open'], high=df_slice['High'], low=df_slice['Low'], close=df_slice['Close'])])
            fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

    with tab_montecarlo:
        st.subheader("Simulação Monte Carlo")
        c_mc1, c_mc2 = st.columns([1, 3])
        
        with c_mc1:
            mc_price = st.number_input("Preço", value=30.0)
            mc_vol = st.number_input("Volatilidade %", value=35.0) / 100
            if st.button("RODAR"):
                st.session_state.mc_paths = run_monte_carlo(mc_price, mc_vol/15.87, 30, 1000)

        with c_mc2:
            if 'mc_paths' in st.session_state:
                paths = st.session_state.mc_paths
                fig_mc = go.Figure()
                
                # Plota 50 linhas finas
                for i in range(50):
                    fig_mc.add_trace(go.Scatter(y=paths[:, i], mode='lines', line=dict(width=1, color='rgba(59, 130, 246, 0.1)'), showlegend=False))
                
                # Estatísticas e Linhas Principais (Aqui estava o erro de sintaxe)
                fig_mc.add_trace(go.Scatter(y=np.mean(paths, axis=1), mode='lines', name='Média', line=dict(color='white', width=3)))
                fig_mc.add_trace(go.Scatter(y=np.percentile(paths, 95, axis=1), mode='lines', name='Topo 95%', line=dict(color='green', width=2, dash='dot')))
                fig_mc.add_trace(go.Scatter(y=np.percentile(paths, 5, axis=1), mode='lines', name='Fundo 5%', line=dict(color='red', width=2, dash='dot')))
                
                fig_mc.update_layout(template="plotly_dark", height=400, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_mc, use_container_width=True)
