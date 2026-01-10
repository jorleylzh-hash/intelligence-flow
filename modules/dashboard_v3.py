import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time

# --- AQUI ESTÁ O SEGREDO: TUDO DENTRO DA FUNÇÃO ---
def show_dashboard():
    
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
        try:
            data = yf.download(tickers_list, period="2d", interval="1d", progress=False)['Close']
        except Exception as e:
            return None
        
        market_state = {}
        for name, symbol in TICKERS.items():
            try:
                if len(data) > 0 and symbol in data.columns:
                    current = float(data[symbol].iloc[-1])
                    prev = float(data[symbol].iloc[-2]) if len(data) > 1 else current
                    change = ((current - prev) / prev) * 100 if prev != 0 else 0
                    market_state[name] = {'price': current, 'change': change}
                else:
                    market_state[name] = {'price': 0.0, 'change': 0.0}
            except:
                market_state[name] = {'price': 0.0, 'change': 0.0}
        return market_state

    # --- INTERFACE VISUAL ---
    # (Note: Removemos o set_page_config daqui pois já está no app.py)
    
    st.caption("INTELLIGENCE FLOW | SYSTEM V3.0 | LIVE MODE")
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

                # --- CÁLCULOS ---
                pbr_fair = (data['PBR_ADR']['price'] * data['USDBRL']['price']) / 2
                pbr_gap = ((pbr_fair / (data['PETR4']['price'] or 1)) - 1) * 100
                
                vale_fair = data['VALE_ADR']['price'] * data['USDBRL']['price']
                vale_gap = ((vale_fair / (data['VALE3']['price'] or 1)) - 1) * 100

                # Score Macro
                score = (data['EWZ']['change'] * 2) + data['SPX']['change'] - data['TNX']['change']

                # --- VISUALIZAÇÃO ---
                st.markdown("### ⚔️ MONITOR DE ARBITRAGEM")
                ac1, ac2, ac3 = st.columns(3)
                
                with ac1:
                    st.subheader("PETROBRAS")
                    col_a, col_b = st.columns(2)
                    col_a.metric("Preço Justo (NY)", f"R$ {pbr_fair:.2f}")
                    col_b.metric("Preço Tela (B3)", f"R$ {data['PETR4']['price']:.2f}")
                    st.metric("GAP", f"{pbr_gap:.2f}%", delta_color="inverse")

                with ac2:
                    st.subheader("VALE")
                    col_a, col_b = st.columns(2)
                    col_a.metric("Preço Justo (NY)", f"R$ {vale_fair:.2f}")
                    col_b.metric("Preço Tela (B3)", f"R$ {data['VALE3']['price']:.2f}")
                    st.metric("GAP", f"{vale_gap:.2f}%", delta_color="inverse")
                    
                with ac3:
                    st.subheader("SENTIMENTO")
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = score,
                        gauge = {
                            'axis': {'range': [-5, 5]},
                            'bar': {'color': "#10b981" if score > 0 else "#ef4444"},
                            'steps': [
                                {'range': [-5, 0], 'color': "rgba(239, 68, 68, 0.2)"},
                                {'range': [0, 5], 'color': "rgba(16, 185, 129, 0.2)"}
                            ]
                        }
                    ))
                    fig.update_layout(height=180, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
                    st.plotly_chart(fig, use_container_width=True, key=f"pulse_{time.time()}")

        time.sleep(15)
