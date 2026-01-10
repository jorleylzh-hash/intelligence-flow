import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time

# --- MÓDULO VISUAL (SOMENTE FUNÇÃO) ---
def show_dashboard():
    
    # Exibe quem está logado
    if 'username' in st.session_state:
        st.caption(f"INTELLIGENCE FLOW | SYSTEM V3.1 | OPERATOR: {st.session_state.username}")

    # --- MOTOR DE DADOS ---
    def get_data_internal():
        TICKERS = {
            'USDBRL': 'BRL=X', 'SPX': '^GSPC', 'EWZ': 'EWZ', 'TNX': '^TNX', 'BRENT': 'BZ=F',
            'VALE_ADR': 'VALE', 'PBR_ADR': 'PBR', 'ITUB_ADR': 'ITUB',
            'PETR4': 'PETR4.SA', 'VALE3': 'VALE3.SA', 'ITUB4': 'ITUB4.SA'
        }
        # Baixa dados (Silent Mode)
        try:
            tickers_list = " ".join(list(TICKERS.values()))
            data = yf.download(tickers_list, period="2d", interval="1d", progress=False)['Close']
        except: return None
        
        market = {}
        # Processamento
        for name, symbol in TICKERS.items():
            try:
                if len(data) > 0 and symbol in data.columns:
                    curr = float(data[symbol].iloc[-1])
                    prev = float(data[symbol].iloc[-2]) if len(data) > 1 else curr
                    chg = ((curr - prev) / prev) * 100 if prev != 0 else 0
                    market[name] = {'price': curr, 'change': chg}
                else: market[name] = {'price': 0.0, 'change': 0.0}
            except: market[name] = {'price': 0.0, 'change': 0.0}
        return market

    # Container para atualização
    placeholder = st.empty()

    # LOOP INFINITO (ATUALIZAÇÃO)
    while True:
        data = get_data_internal()
        
        if data:
            with placeholder.container():
                # 1. MACRO
                st.markdown("### 🌐 MACRO DRIVERS")
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("USDBRL", f"R$ {data['USDBRL']['price']:.3f}", f"{data['USDBRL']['change']:.2f}%")
                c2.metric("S&P 500", f"{data['SPX']['price']:.0f}", f"{data['SPX']['change']:.2f}%")
                c3.metric("EWZ", f"${data['EWZ']['price']:.2f}", f"{data['EWZ']['change']:.2f}%")
                c4.metric("TNX", f"{data['TNX']['price']:.2f}%", f"{data['TNX']['change']:.2f}%")
                c5.metric("BRENT", f"${data['BRENT']['price']:.2f}", f"{data['BRENT']['change']:.2f}%")
                
                st.divider()
                
                # 2. ARBITRAGEM
                # Cálculos
                pbr_fair = (data['PBR_ADR']['price'] * data['USDBRL']['price']) / 2
                pbr_gap = ((pbr_fair / (data['PETR4']['price'] or 1)) - 1) * 100
                vale_fair = data['VALE_ADR']['price'] * data['USDBRL']['price']
                vale_gap = ((vale_fair / (data['VALE3']['price'] or 1)) - 1) * 100
                score = (data['EWZ']['change'] * 2) + data['SPX']['change'] - data['TNX']['change']

                st.markdown("### ⚔️ MONITOR DE ARBITRAGEM")
                ac1, ac2, ac3 = st.columns(3)
                with ac1:
                    st.metric("PETR4 GAP", f"{pbr_gap:.2f}%", f"Fair: R$ {pbr_fair:.2f}")
                with ac2:
                    st.metric("VALE3 GAP", f"{vale_gap:.2f}%", f"Fair: R$ {vale_fair:.2f}")
                with ac3:
                    # Gráfico
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number", value = score,
                        gauge = {'axis': {'range': [-5, 5]}, 'bar': {'color': "#10b981" if score > 0 else "#ef4444"}}
                    ))
                    fig.update_layout(height=150, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
                    st.plotly_chart(fig, use_container_width=True, key=f"g_{time.time()}") # Key única para evitar erro
        
        time.sleep(15)
