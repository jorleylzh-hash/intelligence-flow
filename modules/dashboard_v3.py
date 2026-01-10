import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_lottie import st_lottie
import requests

# --- CONFIGURAÇÃO VISUAL ---
def apply_landing_css():
    st.markdown("""
    <style>
        /* 1. Força Fundo Claro */
        .stApp { background-color: #F1F5F9; }
        
        /* 2. CORREÇÃO CRÍTICA: Força texto escuro em TUDO (sobrepõe Dark Mode do usuário) */
        h1, h2, h3, h4, h5, h6, p, div, span, li {
            color: #0f172a !important; /* Azul Escuro Quase Preto */
        }
        
        /* Exceção: Textos dentro do Header Azul e Botões devem ser brancos */
        .hero-section h1, .hero-section p, .hero-section div {
            color: #ffffff !important;
        }
        
        /* Hero Section */
        .hero-section {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 80px 20px;
            text-align: center;
            border-radius: 0 0 40px 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            margin-bottom: 50px;
        }
        .hero-title { font-size: 3.5rem; font-weight: 800; margin-bottom: 15px; }
        .hero-sub { font-size: 1.3rem; max-width: 800px; margin: 0 auto; opacity: 0.9; }
        
        /* Cards */
        .content-card {
            background: #ffffff;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border-left: 6px solid #3b82f6;
            margin-bottom: 30px;
        }
        
        /* Ticker Box */
        .ticker-box {
            background: white; border-radius: 8px; padding: 15px; text-align: center;
            border: 1px solid #e2e8f0;
        }
    </style>
    """, unsafe_allow_html=True)

# ... (Mantenha o resto das funções load_lottie e get_market_teaser iguais) ...
# Vou replicar a função principal para garantir que você tenha o código completo:

def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

@st.cache_data(ttl=300)
def get_market_teaser():
    tickers = {'S&P 500': '^GSPC', 'Dólar DXY': 'DX-Y.NYB', 'EWZ (Brasil)': 'EWZ'}
    try:
        data = yf.download(list(tickers.values()), period="2d", progress=False)['Close']
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.droplevel(1)
        results = {}
        for name, ticker in tickers.items():
            if ticker in data.columns:
                val = data[ticker].dropna().iloc[-1]
                prev = data[ticker].dropna().iloc[-2]
                chg = ((val-prev)/prev)*100
                results[name] = (val, chg)
        return results
    except: return None

def show_landing_page():
    apply_landing_css()
    
    anim_analise = load_lottie("https://assets3.lottiefiles.com/packages/lf20_qp1q7mct.json")
    
    # HERO
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">INTELLIGENCE FLOW</h1>
        <p class="hero-sub">
            Pare de operar gráficos cegos. Comece a operar o <b>Fluxo Institucional</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # DADOS
    teaser = get_market_teaser()
    if teaser:
        st.markdown("<h3 style='text-align:center; margin-bottom:20px;'>📡 Monitoramento Global</h3>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        cols = [c1, c2, c3]
        for i, (name, (val, chg)) in enumerate(teaser.items()):
            color = "#16a34a" if chg > 0 else "#dc2626"
            with cols[i]:
                st.markdown(f"""
                <div class="ticker-box">
                    <div style="font-size:0.9rem; color:#64748b !important;">{name}</div>
                    <div style="font-size:1.6rem; font-weight:bold;">{val:.2f}</div>
                    <div style="color:{color} !important; font-weight:bold;">{chg:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # DOR & SOLUÇÃO
    c_left, c_right = st.columns([1, 1])
    with c_left:
        st.markdown("""
        <div style="padding: 20px;">
            <h2>🚫 O Erro Invisível</h2>
            <p>
                Você já abriu uma compra perfeita no gráfico de 5 minutos e o mercado virou contra você?
                <br><br>
                Isso não foi azar. Enquanto você olhava o gráfico, os robôs estavam vendendo o <b>EWZ em Nova York</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c_right:
        if anim_analise:
            st_lottie(anim_analise, height=300, key="anim_main")

    # CTA
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #1e293b; padding: 40px; border-radius: 20px; text-align: center;">
        <h2 style="color:white !important;">Pronto para o próximo nível?</h2>
        <p style="color:#cbd5e1 !important;">Acesse a Área do Trader no menu.</p>
    </div>
    """, unsafe_allow_html=True)
