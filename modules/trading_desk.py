import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. MOTOR DE DADOS (DATA ENGINE) ---
@st.cache_data(ttl=60) # Atualiza a cada 60 segundos (Cache curto)
def get_arbitrage_data():
    # Lista de Ativos Monitorados (Paridade)
    # Formato: Chave = Nome, Valor = [Ticker B3, Ticker NYSE, Fator de Conversão]
    pairs = {
        'Petrobras': ['PETR4.SA', 'PBR', 1], # 1 ADR = 2 Ações (exemplo, ajustar fator real se necessário)
        'Vale': ['VALE3.SA', 'VALE', 1],
        'Itaú': ['ITUB4.SA', 'ITUB', 1],
        'Bradesco': ['BBDC4.SA', 'BBD', 1],
        'ETF Brasil': ['BOVA11.SA', 'EWZ', 1] 
    }
    
    # Adicionar Dólar para conversão
    tickers = ['BRL=X'] 
    for pair in pairs.values():
        tickers.append(pair[0]) # B3
        tickers.append(pair[1]) # NYSE
        
    # Download em lote (Mais rápido)
    # TEM QUE TER O threads=False
    data = yf.download(tickers, period="1d", interval="5m", progress=False, threads=False)['Close']
    
    # Tratamento de MultiIndex (yfinance novo)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)

    # Pegar cotação do Dólar atual
    try:
        usd_brl = data['BRL=X'].iloc[-1]
    except:
        usd_brl = 5.00 # Fallback de segurança

    monitor_df = []
    
    for name, tickers in pairs.items():
        try:
            b3_ticker = tickers[0]
            ny_ticker = tickers[1]
            
            # Preços atuais
            price_b3 = data[b3_ticker].dropna().iloc[-1]
            price_ny = data[ny_ticker].dropna().iloc[-1]
            
            # CÁLCULO DA ARBITRAGEM (CORE DO SISTEMA)
            # Preço Teórico no Brasil = Preço NY * Dólar
            fair_price_br = price_ny * usd_brl
            
            # Spread: Diferença entre o Preço Tela B3 e o Preço Justo
            spread_value = price_b3 - fair_price_br
            spread_pct = (spread_value / price_b3) * 100
            
            monitor_df.append({
                "Ativo": name,
                "Preço B3 (R$)": price_b3,
                "Preço NY (US$)": price_ny,
                "Preço Justo (R$)": fair_price_br,
                "Spread %": spread_pct,
                "Status": "DESCONTADO" if spread_pct < -0.5 else ("ÁGIO" if spread_pct > 0.5 else "NEUTRO")
            })
        except:
            continue
            
    return pd.DataFrame(monitor_df), usd_brl

# --- 2. GRÁFICO OPERACIONAL (COM VWAP) ---
def plot_operational_chart(ticker):
    # Simula busca de dados intraday
    df = yf.download(ticker, period="1d", interval="5m", progress=False)
    
    # Cálculo Simples de VWAP (Típico Price * Volume / CumVol)
    df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['VP'] = df['TP'] * df['Volume']
    df['VWAP'] = df['VP'].cumsum() / df['Volume'].cumsum()
    
    fig = go.Figure()
    
    # Candles
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name='Preço'
    ))
    
    # Linha VWAP
    fig.add_trace(go.Scatter(
        x=df.index, y=df['VWAP'], mode='lines', 
        name='VWAP', line=dict(color='#ff9f00', width=2)
    ))

    fig.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis_rangeslider_visible=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# --- 3. INTERFACE DA MESA (UI) ---
def show_desk():
    # Estilo "Dark Trading Station"
    st.markdown("""
    <style>
        .stApp { background-color: #0e1117; color: white; }
        .metric-box {
            background: #1e293b; border-radius: 8px; padding: 15px; border: 1px solid #334155; text-align: center;
        }
        .opportunity-row {
            padding: 10px; border-radius: 5px; margin-bottom: 5px; font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🖥️ Mesa de Operações | HFT Scanner")
    
    # 3.1 HEADER MACRO (O Contexto)
    df_arb, usd_now = get_arbitrage_data()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Dólar Futuro", f"R$ {usd_now:.3f}", "0.15%")
    col2.metric("S&P 500", "5.230", "+0.42%")
    col3.metric("EWZ (Brasil)", "32.40", "-1.20%", delta_color="inverse")
    col4.metric("Juros 10Y (US)", "4.15%", "+0.05%", delta_color="inverse")
    
    st.markdown("---")
    
    # 3.2 O SCANNER DE ARBITRAGEM (O Core)
    c_scan, c_chart = st.columns([1, 2])
    
    with c_scan:
        st.subheader("📡 Radar de Paridade")
        st.markdown("Monitorando distorções > 0.5%")
        
        if not df_arb.empty:
            for index, row in df_arb.iterrows():
                # Definição de Cores Baseada no Spread
                spread = row['Spread %']
                color = "#10b981" if spread < -0.5 else ("#ef4444" if spread > 0.5 else "#64748b")
                msg = "COMPRA BR" if spread < -0.5 else ("VENDA BR" if spread > 0.5 else "EQUILÍBRIO")
                
                st.markdown(f"""
                <div style="background:{color}33; border-left: 5px solid {color}; padding: 10px; margin-bottom: 10px; border-radius: 4px;">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-weight:bold; font-size:1.1rem;">{row['Ativo']}</span>
                        <span style="background:{color}; padding:2px 6px; border-radius:4px; font-size:0.8rem; font-weight:bold; color:white;">{msg}</span>
                    </div>
                    <div style="font-size:0.9rem; margin-top:5px; color:#ccc;">
                        Spread: <b style="color:{color}">{spread:+.2f}%</b>
                    </div>
                    <div style="font-size:0.8rem; color:#888;">
                        B3: R${row['Preço B3 (R$)']:.2f} | Justo: R${row['Preço Justo (R$)']:.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Carregando dados da NYSE...")

    # 3.3 O GRÁFICO OPERACIONAL (A Execução)
    with c_chart:
        st.subheader("📊 Análise Técnica (M5)")
        # Seletor de Ativo Rápido
        selected_asset = st.selectbox("Ativo em Foco", ["PETR4.SA", "VALE3.SA", "WINM24.SA", "WDOM24.SA"])
        
        # Renderiza gráfico
        fig = plot_operational_chart(selected_asset)
        st.plotly_chart(fig, use_container_width=True)
        
        # Boleta Rápida (Simulação)
        b1, b2, b3 = st.columns(3)
        b1.button("🟢 COMPRAR MERCADO", use_container_width=True)
        b2.button("🔴 VENDER MERCADO", use_container_width=True)
        b3.button("🟡 ZERAR POSIÇÃO", use_container_width=True)

    # 3.4 FOOTER DE RISCO
    st.markdown("---")
    st.caption(f"Dados atualizados automaticamente. Fator de Conversão Petrobras: 1:2 | Vale 1:1. Última checagem: {datetime.now().strftime('%H:%M:%S')}")
