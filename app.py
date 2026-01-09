import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

#Configuração da Página
st.set_page_config(page_title="INTELLIGENCE FLOW | PYTHON KERNEL", layout="wide", page_icon="🌪️")

# Estilo CSS
st.markdown("""
<style>
    .stApp { background-color: #0c0a09; color: #e7e5e4; }
    div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; font-size: 24px; color: #10b981; }
    div[data-testid="stMetricLabel"] { font-family: 'Inter', sans-serif; font-size: 14px; color: #a8a29e; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DOS ATIVOS ---
TICKERS = {
    'USDBRL': 'BRL=X',
    'SPX': '^GSPC',
    'EWZ': 'EWZ',
    'TNX': '^TNX',
    'BRENT': 'BZ=F',
    'VALE_ADR': 'VALE',
    'PBR_ADR': 'PBR',
    'ITUB_ADR': 'ITUB',
    'PETR4': 'PETR4.SA',
    'VALE3': 'VALE3.SA',
    'ITUB4': 'ITUB4.SA'
}

# --- MOTOR DE DADOS ---
def get_data():
    tickers_list = " ".join(list(TICKERS.values()))
    # Tenta baixar dados. Se falhar, retorna vazio para não quebrar o app.
    try:
        data = yf.download(tickers_list, period="2d", interval="1d", progress=False)['Close']
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None
    
    market_state = {}
    for name, symbol in TICKERS.items():
        try:
            # Garante que temos dados suficientes
            if len(data) > 0 and symbol in data.columns:
                current = float(data[symbol].iloc[-1])
                # Tenta pegar o anterior, se não existir (feriado), repete o atual
                prev = float(data[symbol].iloc[-2]) if len(data) > 1 else current
                
                change = ((current - prev) / prev) * 100 if prev != 0 else 0
                market_state[name] = {'price': current, 'change': change}
            else:
                market_state[name] = {'price': 0.0, 'change': 0.0}
        except:
            market_state[name] = {'price': 0.0, 'change': 0.0}
    return market_state

# --- INTERFACE ---
st.title("🌪️ INTELLIGENCE FLOW")
st.caption("PYTHON KERNEL V2.0 | STABLE CONNECTION")

# Container Principal que será atualizado
placeholder = st.empty()

# Loop Principal
while True:
    data = get_data()
    
    if data:
        with placeholder.container():
            # 1. MACRO DRIVERS
            st.markdown("### 🌐 MACRO DRIVERS")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("USDBRL", f"R$ {data['USDBRL']['price']:.3f}", f"{data['USDBRL']['change']:.2f}%")
            c2.metric("S&P 500", f"{data['SPX']['price']:.0f}", f"{data['SPX']['change']:.2f}%")
            c3.metric("EWZ (BRAZIL)", f"${data['EWZ']['price']:.2f}", f"{data['EWZ']['change']:.2f}%")
            c4.metric("TNX (10Y)", f"{data['TNX']['price']:.2f}%", f"{data['TNX']['change']:.2f}%")
            c5.metric("BRENT", f"${data['BRENT']['price']:.2f}", f"{data['BRENT']['change']:.2f}%")

            st.divider()

            # 2. ARBITRAGEM
            st.markdown("### ⚔️ ARBITRAGEM & SPREAD")
            
            pbr_fair = (data['PBR_ADR']['price'] * data['USDBRL']['price']) / 2
            pbr_gap = ((pbr_fair / (data['PETR4']['price'] or 1)) - 1) * 100
            
            vale_fair = data['VALE_ADR']['price'] * data['USDBRL']['price']
            vale_gap = ((vale_fair / (data['VALE3']['price'] or 1)) - 1) * 100

            ac1, ac2, ac3 = st.columns(3)
            
            with ac1:
                st.subheader("PETROBRAS")
                col_a, col_b = st.columns(2)
                col_a.metric("ADR (Fair)", f"R$ {pbr_fair:.2f}", f"{data['PBR_ADR']['change']:.2f}%")
                col_b.metric("B3 (Spot)", f"R$ {data['PETR4']['price']:.2f}", f"{data['PETR4']['change']:.2f}%")
                st.metric("GAP", f"{pbr_gap:.2f}%", delta_color="inverse")

            with ac2:
                st.subheader("VALE")
                col_a, col_b = st.columns(2)
                col_a.metric("ADR (Fair)", f"R$ {vale_fair:.2f}", f"{data['VALE_ADR']['change']:.2f}%")
                col_b.metric("B3 (Spot)", f"R$ {data['VALE3']['price']:.2f}", f"{data['VALE3']['change']:.2f}%")
                st.metric("GAP", f"{vale_gap:.2f}%", delta_color="inverse")
                
            with ac3:
                st.subheader("FLUXO AGREGADO")
                score = (data['EWZ']['change'] * 2) + data['SPX']['change'] - data['TNX']['change']
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    gauge = {
                        'axis': {'range': [-5, 5]},
                        'bar': {'color': "#10b981" if score > 0 else "#ef4444"},
                        'steps': [
                            {'range': [-5, 0], 'color': "rgba(239, 68, 68, 0.1)"},
                            {'range': [0, 5], 'color': "rgba(16, 185, 129, 0.1)"}
                        ]
                    }
                ))
                fig.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
                
                # A CORREÇÃO ESTÁ AQUI: ADICIONAMOS UMA KEY ÚNICA
                st.plotly_chart(fig, use_container_width=True, key=f"pulse_{time.time()}")

    # Atualiza a cada 15 segundos para não sobrecarregar
    time.sleep(15)