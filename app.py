import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

#Configuração da Página (Modo Dark / Wide)
st.set_page_config(page_title="INTELLIGENCE FLOW | PYTHON KERNEL", layout="wide", page_icon="🌪️")

# Estilo CSS para ficar parecido com seu terminal anterior
st.markdown("""
<style>
    .stApp { background-color: #0c0a09; color: #e7e5e4; }
    div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; font-size: 24px; color: #10b981; }
    div[data-testid="stMetricLabel"] { font-family: 'Inter', sans-serif; font-size: 14px; color: #a8a29e; }
    .css-1d391kg { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DOS ATIVOS ---
# Tickers do Yahoo Finance (Funcionam 100%)
TICKERS = {
    'USDBRL': 'BRL=X',        # Dólar
    'SPX': '^GSPC',           # S&P 500
    'EWZ': 'EWZ',             # Brazil ETF
    'TNX': '^TNX',            # Treasury 10Y
    'BRENT': 'BZ=F',          # Brent Oil
    'VALE_ADR': 'VALE',       # Vale NYSE
    'PBR_ADR': 'PBR',         # Petrobras NYSE
    'ITUB_ADR': 'ITUB',       # Itaú NYSE
    'PETR4': 'PETR4.SA',      # Petrobras B3
    'VALE3': 'VALE3.SA',      # Vale B3
    'ITUB4': 'ITUB4.SA'       # Itaú B3
}

# --- MOTOR DE DADOS ---
def get_data():
    # Baixa dados de todos os tickers de uma vez (Muito rápido)
    tickers_list = " ".join(list(TICKERS.values()))
    data = yf.download(tickers_list, period="2d", interval="1d", progress=False)['Close']
    
    # Processa Variação %
    market_state = {}
    for name, symbol in TICKERS.items():
        try:
            current = data[symbol].iloc[-1] # Preço Hoje
            prev = data[symbol].iloc[-2]    # Fechamento Ontem
            change = ((current - prev) / prev) * 100
            market_state[name] = {'price': current, 'change': change}
        except:
            market_state[name] = {'price': 0.0, 'change': 0.0}
    return market_state

# --- INTERFACE ---
# Cabeçalho
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🌪️ INTELLIGENCE FLOW")
    st.caption("PYTHON KERNEL V1.0 | DIRECT DATA FEED")
with col_h2:
    st.metric("STATUS", "ONLINE", delta="LIVE FEED")

# Container Principal
placeholder = st.empty()

while True:
    with placeholder.container():
        # Busca Dados Frescos
        data = get_data()

        # 1. LINHA DE DRIVERS MACRO
        st.markdown("### 🌐 MACRO DRIVERS")
        c1, c2, c3, c4, c5 = st.columns(5)
        
        c1.metric("USDBRL", f"R$ {data['USDBRL']['price']:.3f}", f"{data['USDBRL']['change']:.2f}%")
        c2.metric("S&P 500", f"{data['SPX']['price']:.0f}", f"{data['SPX']['change']:.2f}%")
        c3.metric("EWZ (BRAZIL)", f"${data['EWZ']['price']:.2f}", f"{data['EWZ']['change']:.2f}%")
        c4.metric("TNX (10Y)", f"{data['TNX']['price']:.2f}%", f"{data['TNX']['change']:.2f}%")
        c5.metric("BRENT", f"${data['BRENT']['price']:.2f}", f"{data['BRENT']['change']:.2f}%")

        st.divider()

        # 2. SEÇÃO DE ARBITRAGEM (ADR x LOCAL)
        st.markdown("### ⚔️ ARBITRAGEM & SPREAD")
        
        # Calculando Spreads
        # Petrobras: ADR * Dolar / 2 (Pois 1 ADR = 2 Ações)
        pbr_fair = (data['PBR_ADR']['price'] * data['USDBRL']['price']) / 2
        pbr_gap = ((pbr_fair / data['PETR4']['price']) - 1) * 100
        
        # Vale: ADR * Dolar
        vale_fair = data['VALE_ADR']['price'] * data['USDBRL']['price']
        vale_gap = ((vale_fair / data['VALE3']['price']) - 1) * 100

        ac1, ac2, ac3 = st.columns(3)
        
        with ac1:
            st.subheader("PETROBRAS")
            col_a, col_b = st.columns(2)
            col_a.metric("ADR (Fair)", f"R$ {pbr_fair:.2f}", f"{data['PBR_ADR']['change']:.2f}% (NYSE)")
            col_b.metric("B3 (Spot)", f"R$ {data['PETR4']['price']:.2f}", f"{data['PETR4']['change']:.2f}%")
            st.metric("GAP ARBITRAGEM", f"{pbr_gap:.2f}%", delta_color="inverse")

        with ac2:
            st.subheader("VALE")
            col_a, col_b = st.columns(2)
            col_a.metric("ADR (Fair)", f"R$ {vale_fair:.2f}", f"{data['VALE_ADR']['change']:.2f}% (NYSE)")
            col_b.metric("B3 (Spot)", f"R$ {data['VALE3']['price']:.2f}", f"{data['VALE3']['change']:.2f}%")
            st.metric("GAP ARBITRAGEM", f"{vale_gap:.2f}%", delta_color="inverse")
            
        with ac3:
            st.subheader("FLUXO AGREGADO")
            # Gráfico de Pulso Simulado (Baseado nos dados reais)
            score = (data['EWZ']['change'] * 2) + data['SPX']['change'] - data['TNX']['change']
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                title = {'text': "SENTIMENTO MACRO"},
                gauge = {
                    'axis': {'range': [-5, 5]},
                    'bar': {'color': "#10b981" if score > 0 else "#ef4444"},
                    'steps': [
                        {'range': [-5, 0], 'color': "rgba(239, 68, 68, 0.1)"},
                        {'range': [0, 5], 'color': "rgba(16, 185, 129, 0.1)"}
                    ]
                }
            ))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)

        time.sleep(30) # Atualiza a cada 30 segundos