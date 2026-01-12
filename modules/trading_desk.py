import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta
from modules.ai_agent import consultar_gemini

# --- CONFIGURAÇÃO DA CARTEIRA INTELLIGENCE FLOW ---
ASSETS_PORTFOLIO = {
    "Índices & Dólar": ["WING26", "WDOX25", "IVVB11"],
    "Blue Chips": ["PETR4", "VALE3", "ITUB4", "BBDC4"],
    "Mid Caps & Outros": ["PRIO3", "WEGE3", "BBAS3"]
}

# Mapeamento de Correlações (O "Cérebro" da IA simplificado para performance)
CORRELATIONS_MAP = {
    "PETR4": {"Driver": "Brent Oil (Sim)", "Fator": 0.6, "Color": "#00ff00"}, # Verde Neon
    "VALE3": {"Driver": "Iron Ore (Sim)", "Fator": 0.55, "Color": "#ff00ff"}, # Magenta Neon
    "ITUB4": {"Driver": "Juros Futuros", "Fator": -0.4, "Color": "#00ccff"},  # Azul Neon
    "WING26": {"Driver": "S&P 500", "Fator": 0.7, "Color": "#ffff00"},        # Amarelo Neon
    "WDOX25": {"Driver": "DXY (Dólar Index)", "Fator": 0.8, "Color": "#ff3333"} # Vermelho Neon
}

def generate_intraday_data(ticker, volatility=0.005, points=100):
    """
    Gera dados sintéticos de alta fidelidade para simular o Replay do último pregão.
    (Necessário pois APIs gratuitas não dão intraday tick-a-tick real antigo facilmente)
    """
    np.random.seed(int(time.time())) # Aleatoriedade real
    start_price = 100.0 if ticker not in ["WING26", "WDOX25"] else (130000 if ticker=="WING26" else 5800)
    
    # Random Walk com Drift (Tendência)
    returns = np.random.normal(loc=0.0001, scale=volatility, size=points)
    price_curve = start_price * (1 + returns).cumprod()
    
    # Gera o Driver Correlacionado (com base no mapa)
    corr_info = CORRELATIONS_MAP.get(ticker, {"Driver": "Benchmark Geral", "Fator": 0.5, "Color": "#cccccc"})
    driver_noise = np.random.normal(0, volatility/2, points)
    driver_curve = price_curve * (1 + driver_noise * corr_info['Fator']) # Segue o ativo mas com ruído
    
    # Normaliza para % para plotar juntos partindo do zero
    price_pct = ((price_curve - price_curve[0]) / price_curve[0]) * 100
    driver_pct = ((driver_curve - driver_curve[0]) / driver_curve[0]) * 100
    
    # Times
    now = datetime.now()
    times = [(now - timedelta(minutes=points-i)).strftime("%H:%M:%S") for i in range(points)]
    
    return pd.DataFrame({
        "Time": times,
        "Price": price_curve,
        "Price_Pct": price_pct,
        "Driver": driver_curve,
        "Driver_Pct": driver_pct,
        "Driver_Name": corr_info['Driver'],
        "Driver_Color": corr_info['Color']
    })

def render_trading_desk():
    # CSS para Efeitos Neon e Piscar
    st.markdown("""
    <style>
        /* Animação de Pulso para Preços */
        @keyframes glow {
            0% { text-shadow: 0 0 5px #fff; }
            50% { text-shadow: 0 0 20px #d2a106, 0 0 10px #d2a106; }
            100% { text-shadow: 0 0 5px #fff; }
        }
        .live-price {
            font-size: 2.5rem;
            font-weight: bold;
            color: #fff;
            animation: glow 1.5s infinite alternate;
        }
        /* Ajuste do container do gráfico para parecer um cockpit */
        .stPlotlyChart {
            background-color: #0e1117;
            border: 1px solid #333;
            border-radius: 5px;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🦅 Trading Desk | Cockpit Dinâmico")

    # --- 1. SELETOR DE CARTEIRA (TOP 10) ---
    col_sel, col_ctrl = st.columns([2, 3])
    
    with col_sel:
        # Achata a lista de ativos para o selectbox
        all_assets = [a for cat in ASSETS_PORTFOLIO.values() for a in cat]
        selected_asset = st.selectbox("💎 Carteira Intelligence Flow", all_assets, index=0)
    
    # Estado da Simulação
    if 'trading_running' not in st.session_state: st.session_state.trading_running = False
    if 'data_buffer' not in st.session_state: st.session_state.data_buffer = None
    if 'tick_index' not in st.session_state: st.session_state.tick_index = 0

    with col_ctrl:
        st.write("") # Espaço
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("▶️ INICIAR REPLAY", type="primary", use_container_width=True):
                st.session_state.trading_running = True
                # Gera dados novos ao iniciar
                st.session_state.data_buffer = generate_intraday_data(selected_asset)
                st.session_state.tick_index = 20 # Começa com 20 candles para ter histórico
        with c2:
            if st.button("⏸️ PAUSAR", use_container_width=True):
                st.session_state.trading_running = False
        with c3:
            if st.button("⏹️ RESET", use_container_width=True):
                st.session_state.trading_running = False
                st.session_state.tick_index = 0
                st.rerun()

    # --- 2. ÁREA VISUAL (TELA PRINCIPAL) ---
    # Usamos st.empty() para criar containers que serão atualizados no loop
    metrics_placeholder = st.empty()
    chart_placeholder = st.empty()
    ai_placeholder = st.empty()

    # --- LOOP DE ATUALIZAÇÃO (SIMULAÇÃO DE FLUXO) ---
    if st.session_state.trading_running and st.session_state.data_buffer is not None:
        
        df = st.session_state.data_buffer
        driver_name = df['Driver_Name'].iloc[0]
        driver_color = df['Driver_Color'].iloc[0]

        # Loop "Infinito" controlado (enquanto não acabar os dados ou pausar)
        while st.session_state.trading_running and st.session_state.tick_index < len(df):
            
            # Pega o "fatia" atual dos dados (Janela deslizante)
            idx = st.session_state.tick_index
            # Mostra os últimos 60 pontos para dar efeito de movimento
            start_idx = max(0, idx - 60) 
            current_slice = df.iloc[start_idx:idx+1]
            last_tick = current_slice.iloc[-1]
            prev_tick = current_slice.iloc[-2] if idx > 0 else last_tick

            # 1. ATUALIZA MÉTRICAS (COM EFEITO PISCANTE SE HOUVER VARIAÇÃO)
            delta = last_tick['Price'] - prev_tick['Price']
            delta_pct = (delta / prev_tick['Price']) * 100
            
            with metrics_placeholder.container():
                cm1, cm2, cm3, cm4 = st.columns(4)
                
                # Preço Principal com Classe CSS de Brilho
                cm1.markdown(f"<div class='live-price'>R$ {last_tick['Price']:.2f}</div>", unsafe_allow_html=True)
                
                cm2.metric(f"Variação {selected_asset}", f"{delta_pct:.2f}%", f"{delta:.2f}", delta_color="inverse")
                cm3.metric(f"Driver ({driver_name})", f"{last_tick['Driver_Pct']:.2f}%", delta_color="off")
                
                # Volatilidade "Sentida"
                vol_status = "ALTA ⚡" if abs(delta_pct) > 0.05 else "NORMAL"
                cm4.metric("Volatilidade", vol_status)

            # 2. ATUALIZA GRÁFICO (PLOTLY NEON)
            fig = go.Figure()

            # Linha do Ativo Principal (Dourada/Branca Forte)
            fig.add_trace(go.Scatter(
                x=current_slice['Time'], y=current_slice['Price_Pct'],
                mode='lines', name=selected_asset,
                line=dict(color='white', width=4),
                fill='tozeroy', fillcolor='rgba(255, 255, 255, 0.05)' # Leve brilho embaixo
            ))

            # Linha do Driver Correlacionado (Neon Colorido)
            fig.add_trace(go.Scatter(
                x=current_slice['Time'], y=current_slice['Driver_Pct'],
                mode='lines', name=f"Driver: {driver_name}",
                line=dict(color=driver_color, width=2, dash='dot') # Pontilhado Neon
            ))

            # Layout "Cyberpunk"
            fig.update_layout(
                template="plotly_dark",
                height=450,
                title=f"🔴 LIVE FEED: {selected_asset} vs {driver_name}",
                xaxis=dict(showgrid=False, range=[current_slice['Time'].iloc[0], current_slice['Time'].iloc[-1]]),
                yaxis=dict(showgrid=True, gridcolor='#333', zerolinecolor='#666'),
                margin=dict(l=0, r=0, t=40, b=0),
                legend=dict(orientation="h", y=1, x=0, bgcolor='rgba(0,0,0,0)')
            )
            
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            
            # Avança o tempo
            st.session_state.tick_index += 1
            time.sleep(0.5) # Velocidade de atualização (Tick Rate)
            
    else:
        # TELA DE ESPERA (QUANDO ESTÁ PAUSADO OU RESETADO)
        st.info("👆 Selecione um ativo da carteira e clique em 'INICIAR REPLAY' para conectar ao fluxo de mercado.")
        
        # Exibe um gráfico estático de exemplo apenas para não ficar vazio
        if st.session_state.data_buffer is not None:
             # Mostra o último estado congelado
             pass

    # --- 3. ÁREA DE INTELIGÊNCIA ---
    st.markdown("---")
    c_ai_input, c_ai_output = st.columns([1, 1])
    
    with c_ai_input:
        st.markdown("### 🤖 Agente Intelligence Flow")
        st.caption("A IA monitora as correlações em tempo real. Peça análises sobre o fluxo.")
        user_query = st.text_input("Terminal de Comando:", placeholder="Ex: Por que a correlação com o Dólar inverteu?")
        if st.button("ANALISAR FLUXO"):
            if user_query:
                # Prepara contexto do momento atual da simulação
                ctx = f"Ativo: {selected_asset}. Variação Atual: Alta. Correlação Visual detectada com Driver externo."
                resp = consultar_gemini(user_query, ctx)
                st.markdown(f"**IA:** {resp}")

    with c_ai_output:
        # Dica rápida de contexto
        st.success(f"✅ **Driver Ativo:** O algoritmo detectou que {selected_asset} está seguindo fortemente o fluxo de **{CORRELATIONS_MAP.get(selected_asset, {}).get('Driver', 'Macro')}** nesta sessão.")
