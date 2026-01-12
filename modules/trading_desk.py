import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta
from modules.ai_agent import consultar_gemini

# --- DADOS ESTRUTURAIS ---
ASSETS_PORTFOLIO = {
    "Dólar & Macro": ["WDOX25", "WING26"],
    "ADRs (Arbitragem)": ["PETR4", "VALE3", "ITUB4", "PBR", "VALE"],
}

def generate_macro_data(ticker, points=100):
    """
    Gera dados macroeconômicos correlacionados para os 3 painéis do WDO.
    """
    np.random.seed(int(time.time()))
    
    # Base Price
    base = 5800 if ticker == "WDOX25" else (132000 if ticker == "WING26" else 35.00)
    vol = 0.001
    
    # 1. Ativo Principal
    returns = np.random.normal(0, vol, points)
    price = base * (1 + returns).cumprod()
    
    # 2. Drivers Globais (DXY, SPX, US10Y)
    dxy = price * (1 + np.random.normal(0, vol, points)) # DXY segue WDO (Dólar forte lá, forte aqui)
    spx = price * (1 - np.random.normal(0, vol, points)) # SPX inverso ao WDO (Risk On = Dólar cai)
    us10y = price * (1 + np.random.normal(0, vol*0.5, points)) # Yields sobem, Dólar sobe
    
    # 3. Drivers Commodities (Oil, Iron)
    oil = price * (1 - np.random.normal(0, vol*1.2, points)) # Oil sobe, Dólar cai (Brasil exporta)
    iron = price * (1 - np.random.normal(0, vol*1.1, points))
    
    # 4. Drivers Locais (DI, IBOV)
    di = price * (1 + np.random.normal(0, vol*0.8, points)) # Juros sobem (Risco fiscal), Dólar sobe
    ibov = price * (1 - np.random.normal(0, vol, points))   # Bolsa cai, Dólar sobe
    
    # 5. Arbitragem (ADR vs Local) - Só para Petro/Vale
    adr_price = (price / 5.80) * (1 + np.random.normal(0, 0.002, points)) # Simula preço em USD
    
    times = [(datetime.now() - timedelta(minutes=points-i)).strftime("%H:%M") for i in range(points)]
    
    return {
        "times": times, "price": price, 
        "global": {"DXY": dxy, "S&P500": spx, "US10Y": us10y},
        "commodities": {"Brent Oil": oil, "Iron Ore": iron},
        "local": {"DI Futuro": di, "Ibovespa": ibov},
        "arbitrage": {"ADR_USD": adr_price, "FX": 5.80 + np.random.normal(0, 0.01, points)}
    }

def render_chart_panel(title, times, main_data, correlations, main_name):
    """Renderiza um gráfico limpo com o ativo principal e suas correlações específicas."""
    fig = go.Figure()
    
    # Normalização percentual para plotar juntos
    base_0 = main_data[0]
    main_pct = ((main_data - base_0) / base_0) * 100
    
    # Ativo Principal
    fig.add_trace(go.Scatter(x=times, y=main_pct, mode='lines', name=main_name, line=dict(color='white', width=3)))
    
    # Correlações
    colors = ['#ef4444', '#22c55e', '#eab308', '#3b82f6'] # Red, Green, Yellow, Blue
    for i, (name, data) in enumerate(correlations.items()):
        base_c = data[0]
        corr_pct = ((data - base_c) / base_c) * 100
        fig.add_trace(go.Scatter(x=times, y=corr_pct, mode='lines', name=name, line=dict(color=colors[i%4], width=1.5, dash='dot')))

    fig.update_layout(
        template="plotly_dark", height=300, title=title,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", y=1, x=0, bgcolor='rgba(0,0,0,0)'),
        yaxis=dict(showgrid=True, gridcolor='#333'), xaxis=dict(showgrid=False)
    )
    return fig

def render_trading_desk():
    st.markdown("## 🦅 Central de Inteligência | WDO & Arbitragem")
    
    # --- CONTROLES (FORA DO LOOP) ---
    c_sel, c_btn = st.columns([1, 2])
    with c_sel:
        all_assets = [a for cat in ASSETS_PORTFOLIO.values() for a in cat]
        selected_asset = st.selectbox("Ativo em Foco", all_assets, index=0)
    
    with c_btn:
        st.write("")
        col_b1, col_b2, col_b3 = st.columns(3)
        if col_b1.button("▶️ MONITORAR"): st.session_state.trading_running = True
        if col_b2.button("⏸️ PAUSAR"): st.session_state.trading_running = False
        if col_b3.button("⏹️ RESET"): st.session_state.trading_running = False

    # Inicializa estado
    if 'trading_running' not in st.session_state: st.session_state.trading_running = False
    
    # Containers para os 3 Gráficos (Para não recriar na tela)
    container_global = st.empty()
    container_commodities = st.empty()
    container_local = st.empty()
    container_arbitrage = st.empty()
    
    # --- TEXTO EDUCATIVO (IA) ---
    st.markdown("---")
    with st.expander("📚 LEITURA DE CENÁRIO (IA INTELLIGENCE FLOW)", expanded=True):
        st.markdown("""
        **ANÁLISE DE CONTEXTO PARA WDO (DÓLAR FUTURO):**
        
        1. **Cenário Global (Risk-On/Off):** Monitore o **DXY** e **Treasuries (US10Y)**. Se ambos sobem, pressão de alta no WDO (Dólar forte no mundo). Se **S&P500** cai forte, indica aversão ao risco (Risk-Off), impulsionando WDO.
        2. **Commodities (Brasil):** O Brasil é exportador. Alta em **Petróleo** e **Minério** traz dólares, pressionando WDO para baixo. Queda nessas commodities pressiona WDO para cima.
        3. **Risco Local (Fiscal/Juros):** Monitore o **DI Futuro**. Se DI descola do US10Y e sobe sozinho, é Risco Brasil (Fiscal), explodindo o WDO.
        """)

    # --- LOOP DE SIMULAÇÃO ---
    if st.session_state.trading_running:
        # Gera dados UMA VEZ por ciclo de atualização simulada
        data = generate_macro_data(selected_asset)
        times = data['times']
        
        # 1. PAINEL GLOBAL
        fig_global = render_chart_panel("1. Cenário Global (DXY, S&P, US10Y)", times, data['price'], data['global'], selected_asset)
        container_global.plotly_chart(fig_global, use_container_width=True)
        
        # 2. PAINEL COMMODITIES
        fig_comm = render_chart_panel("2. Driver Commodities (Oil, Iron)", times, data['price'], data['commodities'], selected_asset)
        container_commodities.plotly_chart(fig_comm, use_container_width=True)
        
        # 3. PAINEL LOCAL
        fig_local = render_chart_panel("3. Risco Local (DI, Ibovespa)", times, data['price'], data['local'], selected_asset)
        container_local.plotly_chart(fig_local, use_container_width=True)
        
        # 4. MONITOR DE ARBITRAGEM (Só se for Petro ou Vale)
        if selected_asset in ["PETR4", "VALE3"]:
            last_local = data['price'][-1]
            last_adr = data['arbitrage']['ADR_USD'][-1]
            last_fx = data['arbitrage']['FX'][-1]
            
            # Fórmula: Paridade = ADR * FX
            parity = last_adr * last_fx
            spread = last_local - parity
            spread_pct = (spread / parity) * 100
            
            container_arbitrage.markdown(f"""
            <div style="background:#1e293b; padding:15px; border-radius:10px; border:1px solid #334155; margin-top:20px;">
                <h3 style="margin:0; color:#d2a106;">⚖️ ARBITRAGEM (ADR vs LOCAL)</h3>
                <div style="display:flex; justify-content:space-around; align-items:center; margin-top:10px;">
                    <div>
                        <span style="color:#94a3b8; font-size:0.8em;">PREÇO LOCAL (B3)</span><br>
                        <span style="font-size:1.5em; font-weight:bold;">R$ {last_local:.2f}</span>
                    </div>
                    <div>
                        <span style="color:#94a3b8; font-size:0.8em;">PARIDADE (ADR*FX)</span><br>
                        <span style="font-size:1.5em; font-weight:bold;">R$ {parity:.2f}</span>
                    </div>
                    <div style="text-align:right;">
                        <span style="color:#94a3b8; font-size:0.8em;">SPREAD / DIVERGÊNCIA</span><br>
                        <span style="font-size:2em; font-weight:bold; color:{'#ef4444' if abs(spread_pct)>0.5 else '#22c55e'};">
                            {spread_pct:+.2f}%
                        </span>
                    </div>
                </div>
                <div style="font-size:0.8em; color:#64748b; margin-top:5px; text-align:center;">
                    Fórmula: Spread = (Preço B3 - (Preço ADR × Dólar)) / Paridade
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        time.sleep(1) # Atualização a cada segundo
        st.rerun() # Garante o refresh limpo

# Função de compatibilidade OBRIGATÓRIA para o app.py não quebrar
def show_desk():
    render_trading_desk()
