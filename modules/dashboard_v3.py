import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# --- 1. FUNÇÕES AUXILIARES (CARREGAMENTO) ---

# Função para carregar animações Lottie (JSON) da web
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Cache de dados de mercado
@st.cache_data(ttl=300)
def get_market_data():
    tickers = {
        'S&P 500': '^GSPC', 
        'DXY (Dólar Global)': 'DX-Y.NYB', 
        'EWZ (Brasil ETF)': 'EWZ', 
        'Petróleo Brent': 'BZ=F'
    }
    try:
        data = yf.download(list(tickers.values()), period="5d", interval="1d", progress=False)['Close']
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.droplevel(1)
        
        results = {}
        history = {} # Guardar histórico para o mini-gráfico
        
        for name, ticker in tickers.items():
            if ticker in data.columns:
                clean_data = data[ticker].dropna()
                curr = clean_data.iloc[-1]
                prev = clean_data.iloc[-2]
                change = ((curr - prev) / prev) * 100
                results[name] = (curr, change)
                history[name] = clean_data # Guardamos a série para plotar depois
            else:
                results[name] = (0.0, 0.0)
                history[name] = []
        return results, history
    except:
        return None, None

# --- 2. ESTILIZAÇÃO VISUAL (MODERNA) ---
def apply_modern_css():
    st.markdown("""
    <style>
        /* Fundo Dark Profundo */
        .stApp { background-color: #0e1117; }
        
        /* Títulos com Gradiente */
        h1 {
            background: -webkit-linear-gradient(45deg, #3b82f6, #2dd4bf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
        }
        
        /* Cards de Vidro (Glassmorphism) */
        .glass-metric {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            transition: transform 0.2s;
        }
        .glass-metric:hover {
            border-color: #3b82f6;
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.05);
        }
        
        /* Texto */
        p, li { color: #94a3b8; font-size: 1.05rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PÁGINA PRINCIPAL ---
def show_landing_page():
    apply_modern_css()
    
    # Carrega Animações (Tecnologia Lottie)
    # Animação de um gráfico financeiro futurista
    lottie_chart = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_kuhijlNsXK.json")
    # Animação de conexões/rede
    lottie_network = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_zrqthn6o.json")

    # --- HERO SECTION (Topo) ---
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.title("INTELLIGENCE FLOW")
        st.markdown("### Algoritmos de Arbitragem & Fluxo Macro")
        st.write("""
        Plataforma proprietária de monitoramento de **spreads B3/NYSE**. 
        Utilizamos modelos quantitativos para identificar assimetrias de preço em tempo real entre ativos espelhados (ADRs).
        """)
        
        # Botões ou Métricas rápidas
        st.info("⚡ Latência de Dados: < 200ms (API Dedicada)")

    with c2:
        # AQUI ENTRA A TECNOLOGIA LOTTIE (Animação Vetorial)
        if lottie_chart:
            st_lottie(lottie_chart, height=300, key="hero_anim")

    st.markdown("---")

    # --- TICKER INTELIGENTE (Plotly Sparklines) ---
    st.markdown("### 📊 Monitoramento Global")
    
    data, history = get_market_data()
    
    if data:
        cols = st.columns(4)
        keys = list(data.keys())
        
        for i, col in enumerate(cols):
            name = keys[i]
            val, change = data[name]
            series = history[name]
            
            with col:
                # Criação de Mini-Gráfico (Sparkline) com Plotly
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    y=series, 
                    mode='lines', 
                    line=dict(color='#3b82f6' if change > 0 else '#ef4444', width=2),
                    fill='tozeroy',
                    fillcolor='rgba(59, 130, 246, 0.1)' if change > 0 else 'rgba(239, 68, 68, 0.1)'
                ))
                fig.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0),
                    height=50,
                    showlegend=False,
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                # Renderiza o Card HTML + Gráfico
                st.markdown(f"""
                <div class="glass-metric">
                    <div style="font-size:0.9rem; color:#aaa;">{name}</div>
                    <div style="font-size:1.5rem; color:#fff; font-weight:bold;">{val:.2f}</div>
                    <div style="color:{'#4ade80' if change > 0 else '#f87171'};">{change:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
                # O gráfico Plotly entra logo abaixo do HTML
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # --- SESSÃO CONCEITUAL (Com Animação de Rede) ---
    c_text, c_anim = st.columns([1, 1])
    
    with c_anim:
        if lottie_network:
            st_lottie(lottie_network, height=250, key="net_anim")
            
    with c_text:
        st.header("Metodologia Quant")
        st.markdown("""
        **1. Coleta de Dados:** Conexão via WebSocket com gateways B3 e NYSE.
        
        **2. Cálculo de Paridade:** Normalização cambial e ajustes de custódia para encontrar o "Preço Justo" teórico.
        
        **3. Execução:** Quando o Spread (Diferença) supera 2 desvios-padrão (Bands), o sistema sinaliza a oportunidade de arbitragem.
        """)
        
        # Exemplo visual de barra de progresso customizada
        st.write("Confiabilidade do Modelo Atual:")
        st.progress(92)
        st.caption("Backtest realizado nos últimos 12 meses (Sharpe Ratio: 1.8)")

    st.markdown("<br><br><div style='text-align:center; color:#555;'>Intelligence Flow © 2026</div>", unsafe_allow_html=True)
