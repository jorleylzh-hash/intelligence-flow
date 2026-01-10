import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# --- CONFIGURAÇÃO DE IMAGENS ---
IMG_WIN = "https://images.unsplash.com/photo-1611974765270-ca1258634369?q=80&w=1000&auto=format&fit=crop"
IMG_WDO = "https://images.unsplash.com/photo-1580519542036-c47de6196ba5?q=80&w=1000&auto=format&fit=crop"
IMG_OIL = "https://images.unsplash.com/photo-1518458028785-8fbcd101ebb9?q=80&w=1000&auto=format&fit=crop"

# --- ESTILIZAÇÃO CSS ---
def apply_pro_styles():
    st.markdown("""
    <style>
        .context-card {
            position: relative;
            height: 200px;
            background-size: cover;
            background-position: center;
            border-radius: 12px;
            margin-bottom: 15px;
            overflow: hidden;
            border: 1px solid #333;
            transition: transform 0.3s;
        }
        .context-card:hover { transform: scale(1.02); border: 1px solid #10b981; }
        .overlay {
            background: linear-gradient(0deg, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.4) 100%);
            height: 100%; width: 100%; padding: 20px;
            display: flex; flex-direction: column; justify-content: flex-end;
        }
        .card-title { font-size: 22px; font-weight: bold; color: white; margin: 0;}
        .card-desc { font-size: 12px; color: #d1d5db; margin-top: 5px; }
        .badge { background-color: #10b981; color: black; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; width: fit-content; }
    </style>
    """, unsafe_allow_html=True)

# --- CÁLCULOS TÉCNICOS ---
def calculate_vwap(df):
    try:
        df['Typical_Price'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['VP'] = df['Typical_Price'] * df['Volume']
        df['VWAP'] = df['VP'].cumsum() / df['Volume'].cumsum()
        return df
    except: return df

def get_intraday_data(ticker):
    try:
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        return calculate_vwap(df)
    except: return pd.DataFrame()

def get_live_quotes():
    TICKERS = {'USDBRL': 'BRL=X', 'SPX': '^GSPC', 'TNX': '^TNX', 'BRENT': 'BZ=F', 'PETR4': 'PETR4.SA', 'VALE': 'VALE', 'PBR': 'PBR'}
    try:
        txt = " ".join(list(TICKERS.values()))
        data = yf.download(txt, period="2d", interval="1d", progress=False)['Close']
        res = {}
        for k, v in TICKERS.items():
            if len(data) > 0 and v in data.columns:
                curr = float(data[v].iloc[-1])
                prev = float(data[v].iloc[-2]) if len(data) > 1 else curr
                chg = ((curr - prev)/prev)*100 if prev != 0 else 0
                res[k] = {'price': curr, 'chg': chg}
            else: res[k] = {'price': 0.0, 'chg': 0.0}
        return res
    except: return None

def plot_technical_chart(symbol, df_data):
    if df_data.empty: return go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Candlestick(x=df_data.index, open=df_data['Open'], high=df_data['High'], low=df_data['Low'], close=df_data['Close'], name="Preço"), secondary_y=True)
    if 'VWAP' in df_data.columns:
        fig.add_trace(go.Scatter(x=df_data.index, y=df_data['VWAP'], mode='lines', name='VWAP', line=dict(color='#facc15', width=2)), secondary_y=True)
    colors = ['#ef4444' if r['Open'] - r['Close'] > 0 else '#10b981' for i, r in df_data.iterrows()]
    fig.add_trace(go.Bar(x=df_data.index, y=df_data['Volume'], name="Vol", marker_color=colors, opacity=0.3), secondary_y=False)
    fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), margin=dict(l=10,r=10,t=30,b=10), xaxis_rangeslider_visible=False, showlegend=False)
    fig.update_yaxes(showgrid=False, visible=False, secondary_y=False)
    fig.update_yaxes(showgrid=True, gridcolor='#333', secondary_y=True)
    return fig

# --- FUNÇÃO PRINCIPAL QUE O APP.PY ESTÁ PROCURANDO ---
def show_dashboard():
    apply_pro_styles()
    
    # Cabeçalho
    c1, c2 = st.columns([4,1])
    with c1: st.caption(f"📍 USER: {st.session_state.username}")
    with c2: 
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("🌪️ INTELLIGENCE FLOW")

    # CARDS CONTEXTUAIS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="context-card" style="background-image: url('{IMG_WIN}');"><div class="overlay"><div class="badge">WIN FUTURO</div><p class="card-title">IBOV</p><p class="card-desc">Correlação Alta: VALE3 e PETR4.</p></div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="context-card" style="background-image: url('{IMG_WDO}');"><div class="overlay"><div class="badge">WDO DÓLAR</div><p class="card-title">FX</p><p class="card-desc">Driver: Juros EUA (Treasuries).</p></div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="context-card" style="background-image: url('{IMG_OIL}');"><div class="overlay"><div class="badge">DRIVERS</div><p class="card-title">MACRO</p><p class="card-desc">Petróleo e Minério definem o tom.</p></div></div>""", unsafe_allow_html=True)

    # LOOP DE DADOS
    placeholder = st.empty()
    while True:
        quotes = get_live_quotes()
        if quotes:
            with placeholder.container():
                st.markdown("### 🌍 DRIVERS")
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("BRENT", f"${quotes['BRENT']['price']:.2f}", f"{quotes['BRENT']['chg']:.2f}%")
                m2.metric("VALE NY", f"${quotes['VALE']['price']:.2f}", f"{quotes['VALE']['chg']:.2f}%")
                m3.metric("US 10Y", f"{quotes['TNX']['price']:.2f}%", f"{quotes['TNX']['chg']:.2f}%")
                m4.metric("S&P 500", f"{quotes['SPX']['price']:.0f}", f"{quotes['SPX']['chg']:.2f}%")
                m5.metric("DÓLAR", f"R$ {quotes['USDBRL']['price']:.3f}", f"{quotes['USDBRL']['chg']:.2f}%")
                
                st.divider()
                st.markdown("### 📊 FLUXO PETROBRAS (VWAP)")
                df_petr = get_intraday_data('PETR4.SA')
                if not df_petr.empty:
                    fig = plot_technical_chart('PETR4', df_petr)
                    st.plotly_chart(fig, use_container_width=True, key=f"g_{time.time()}")
                else:
                    st.info("Aguardando abertura de mercado ou dados...")
        time.sleep(30)
