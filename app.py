import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="INTELLIGENCE FLOW | AUDIT KERNEL", layout="wide", page_icon="🌪️")

# --- CSS PERSONALIZADO (Design Institucional) ---
st.markdown("""
<style>
    .stApp { background-color: #0c0a09; color: #e7e5e4; }
    
    /* Métricas Principais */
    div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; font-size: 24px; color: #10b981; }
    div[data-testid="stMetricLabel"] { font-family: 'Inter', sans-serif; font-size: 14px; color: #a8a29e; }
    
    /* Estilo do Memorial de Cálculo */
    .memorial-box { 
        background-color: #1c1917; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 3px solid #3b82f6;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        margin-bottom: 10px;
    }
    .math-val { color: #60a5fa; font-weight: bold; }
    .result-val { color: #facc15; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- DICIONÁRIO DE ATIVOS ---
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

# --- INTERFACE ---
st.title("🌪️ INTELLIGENCE FLOW")
st.caption("PYTHON KERNEL V3.0 | MEMORIAL DE CÁLCULO INTEGRADO")

placeholder = st.empty()

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

            # --- CÁLCULOS PRINCIPAIS ---
            # Petrobras
            pbr_adr = data['PBR_ADR']['price']
            dolar = data['USDBRL']['price']
            pbr_fair = (pbr_adr * dolar) / 2
            pbr_spot = data['PETR4']['price']
            pbr_gap = ((pbr_fair / (pbr_spot or 1)) - 1) * 100

            # Vale
            vale_adr = data['VALE_ADR']['price']
            vale_fair = vale_adr * dolar
            vale_spot = data['VALE3']['price']
            vale_gap = ((vale_fair / (vale_spot or 1)) - 1) * 100

            # Score
            ewz_chg = data['EWZ']['change']
            spx_chg = data['SPX']['change']
            tnx_chg = data['TNX']['change']
            score = (ewz_chg * 2) + spx_chg - tnx_chg

            # --- VISUALIZAÇÃO PRINCIPAL ---
            st.markdown("### ⚔️ MONITOR DE ARBITRAGEM")
            ac1, ac2, ac3 = st.columns(3)
            
            with ac1:
                st.subheader("PETROBRAS (PETR4)")
                col_a, col_b = st.columns(2)
                col_a.metric("Preço Justo (NY)", f"R$ {pbr_fair:.2f}")
                col_b.metric("Preço Tela (B3)", f"R$ {pbr_spot:.2f}")
                st.metric("GAP DE OPORTUNIDADE", f"{pbr_gap:.2f}%", delta_color="inverse")

            with ac2:
                st.subheader("VALE (VALE3)")
                col_a, col_b = st.columns(2)
                col_a.metric("Preço Justo (NY)", f"R$ {vale_fair:.2f}")
                col_b.metric("Preço Tela (B3)", f"R$ {vale_spot:.2f}")
                st.metric("GAP DE OPORTUNIDADE", f"{vale_gap:.2f}%", delta_color="inverse")
                
            with ac3:
                st.subheader("SENTIMENTO (SCORE)")
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

            # --- AQUI ESTÁ O MEMORIAL DE CÁLCULO ---
            with st.expander("🧮 MEMORIAL DE CÁLCULO (AUDITORIA EM TEMPO REAL)", expanded=False):
                
                tab1, tab2, tab3 = st.tabs(["🛢️ PETROBRAS", "⛏️ VALE", "🌡️ SCORE MACRO"])
                
                with tab1:
                    st.markdown("##### FÓRMULA DE PARIDADE:")
                    st.latex(r'''Preço_{Justo} = \frac{ADR_{US\$} \times Câmbio_{R\$}}{2}''')
                    
                    st.markdown(f"""
                    <div class="memorial-box">
                    1. COTAÇÃO NY (PBR): <span class="math-val">${pbr_adr:.2f}</span><br>
                    2. DÓLAR (USDBRL): <span class="math-val">R${dolar:.3f}</span><br>
                    3. FATOR DE CONVERSÃO: <b>2</b> (1 ADR = 2 Ações ON)<br>
                    ---------------------------------------<br>
                    CÁLCULO: ({pbr_adr:.2f} * {dolar:.3f}) / 2 = <span class="result-val">R$ {pbr_fair:.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if pbr_gap > 0.5:
                        st.info("ANÁLISE: O ativo está BARATO no Brasil em relação a NY. Pressão de COMPRA.")
                    elif pbr_gap < -0.5:
                        st.error("ANÁLISE: O ativo está CARO no Brasil em relação a NY. Pressão de VENDA.")
                    else:
                        st.warning("ANÁLISE: Preço equilibrado (Arbitragem fechada).")

                with tab2:
                    st.markdown("##### FÓRMULA DE PARIDADE:")
                    st.latex(r'''Preço_{Justo} = ADR_{US\$} \times Câmbio_{R\$}''')
                    
                    st.markdown(f"""
                    <div class="memorial-box">
                    1. COTAÇÃO NY (VALE): <span class="math-val">${vale_adr:.2f}</span><br>
                    2. DÓLAR (USDBRL): <span class="math-val">R${dolar:.3f}</span><br>
                    3. FATOR DE CONVERSÃO: <b>1</b> (1 ADR = 1 Ação ON)<br>
                    ---------------------------------------<br>
                    CÁLCULO: {vale_adr:.2f} * {dolar:.3f} = <span class="result-val">R$ {vale_fair:.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)

                with tab3:
                    st.markdown("##### FÓRMULA DO FLUXO AGREGADO:")
                    st.latex(r'''Score = (EWZ\% \times 2) + SPX\% - TNX\%''')
                    
                    st.markdown(f"""
                    <div class="memorial-box">
                    1. EWZ (BRASIL EM NY): <span class="math-val">{ewz_chg:+.2f}%</span> (Peso x2 = {ewz_chg*2:+.2f})<br>
                    2. S&P 500 (GLOBAL): <span class="math-val">{spx_chg:+.2f}%</span><br>
                    3. TREASURIES (RISCO): <span class="math-val">{tnx_chg:+.2f}%</span> (Sinal Invertido)<br>
                    ---------------------------------------<br>
                    CÁLCULO: ({ewz_chg*2:+.2f}) + ({spx_chg:+.2f}) - ({tnx_chg:+.2f}) = <span class="result-val">{score:+.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.caption("*Nota: O TNX entra subtraindo pois Juros altos são ruins para Bolsa.")

    time.sleep(15)
