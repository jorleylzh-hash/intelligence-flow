import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# --- CONFIGURAÇÃO DE IMAGENS (LINKS REAIS) ---
IMG_WIN = "https://images.unsplash.com/photo-1611974765270-ca1258634369?q=80&w=1000&auto=format&fit=crop" # Bolsa / Touro
IMG_WDO = "https://images.unsplash.com/photo-1580519542036-c47de6196ba5?q=80&w=1000&auto=format&fit=crop" # Dólar / Money
IMG_OIL = "https://images.unsplash.com/photo-1518458028785-8fbcd101ebb9?q=80&w=1000&auto=format&fit=crop" # Petróleo

# --- ESTILIZAÇÃO CSS AVANÇADA ---
def apply_pro_styles():
    st.markdown("""
    <style>
        /* Card com Imagem de Fundo e Texto Sobreposto */
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
        
        /* Overlay Escuro para ler o texto */
        .overlay {
            background: linear-gradient(0deg, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.4) 100%);
            height: 100%;
            width: 100%;
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
        }
        
        .card-title { font-size: 22px; font-weight: bold; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.8); margin: 0;}
        .card-desc { font-size: 12px; color: #d1d5db; margin-top: 5px; font-weight: 500; }
        .badge { background-color: #10b981; color: black; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; width: fit-content; }
        
        /* Layout Geral */
        .stMetric { background-color: #1c1917; padding: 10px; border-radius: 8px; border: 1px solid #292524; }
    </style>
    """, unsafe_allow_html=True)

# --- CÁLCULO DE VWAP INTRADAY ---
def calculate_vwap(df):
    try:
        df['Typical_Price'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['VP'] = df['Typical_Price'] * df['Volume']
        # VWAP acumulada do dia
        df['VWAP'] = df['VP'].cumsum() / df['Volume'].cumsum()
        return df
    except:
        return df

# --- MOTOR DE DADOS ---
def get_intraday_data(ticker):
    # Baixa dados de 1 dia com intervalo de 5 minutos para gráfico
    try:
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        return calculate_vwap(df)
    except:
        return pd.DataFrame()

def get_live_quotes():
    TICKERS = {
        'USDBRL': 'BRL=X', 'SPX': '^GSPC', 'EWZ': 'EWZ', 'TNX': '^TNX', 'BRENT': 'BZ=F',
        'PETR4': 'PETR4.SA', 'VALE3': 'VALE3.SA', 'PBR': 'PBR', 'VALE': 'VALE'
    }
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
            else:
                res[k] = {'price': 0.0, 'chg': 0.0}
        return res
    except: return None

# --- PLOTAGEM DO GRÁFICO ---
def plot_technical_chart(symbol, df_data):
    if df_data.empty:
        return go.Figure()

    # Cria subplot com eixo secundário para Volume
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 1. Candles
    fig.add_trace(go.Candlestick(
        x=df_data.index,
        open=df_data['Open'], high=df_data['High'],
        low=df_data['Low'], close=df_data['Close'],
        name="Preço"
    ), secondary_y=True)

    # 2. VWAP (Linha Laranja Institucional)
    if 'VWAP' in df_data.columns:
        fig.add_trace(go.Scatter(
            x=df_data.index, y=df_data['VWAP'],
            mode='lines', name='VWAP (Institucional)',
            line=dict(color='#facc15', width=2)
        ), secondary_y=True)

    # 3. Volume Financeiro (Barras)
    colors = ['#ef4444' if row['Open'] - row['Close'] > 0 else '#10b981' for index, row in df_data.iterrows()]
    fig.add_trace(go.Bar(
        x=df_data.index, y=df_data['Volume'],
        name="Vol. Financeiro",
        marker_color=colors, opacity=0.3
    ), secondary_y=False)

    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", y=1.02, x=0)
    )
    # Eixo Y1 (Volume) ocult
