import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# --- 1. FUNÇÕES AUXILIARES ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=2)
        return r.json() if r.status_code == 200 else None
    except: return None

# CACHE DE DADOS (COM A CORREÇÃO DE THREADS)
@st.cache_data(ttl=300)
def get_market_teaser():
    tickers = {'S&P 500': '^GSPC', 'Dólar DXY': 'DX-Y.NYB', 'EWZ (Brasil)': 'EWZ'}
    try:
        # --- AQUI ESTÁ A CORREÇÃO (threads=False) ---
        # Isso impede que o Render trave o banco de dados
        data = yf.download(list(tickers.values()), period="2d", progress=False, threads=False)['Close']
        
        if isinstance(data.columns, pd.MultiIndex): 
            data.columns = data.columns.droplevel(1)
            
        results = {}
        for name, ticker in tickers.items():
            if ticker in data.columns:
                series = data[ticker].dropna()
                if len(series) >= 2:
                    val = series.iloc[-1]
                    prev = series.iloc[-2]
                    chg = ((val-prev)/prev)*100
                    results[name] = (val, chg)
        return results
    except Exception as e:
        return None

# --- 2. PÁGINA PRINCIPAL ---
def show_landing_page():
    
    # Animações
    anim_network = load_lottie("https://assets5.lottiefiles.com/packages/lf20_w51pcehl.json")

    # === HERO SECTION ===
    st.markdown("""
    <div style="text-align: center; padding: 60px 0;">
        <h1 style="font-size: 3.5rem; letter-spacing: -2px; margin-bottom: 10px; color: #f8fafc;">
            INTELLIGENCE FLOW
        </h1>
        <p style="font-size: 1.2rem; color: #94a3b8; max-width: 800px; margin: 0 auto;">
            Ecossistema Institucional de Arbitragem, Macroeconomia e Inteligência Artificial.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # === TICKER TAPE (DADOS AO VIVO) ===
    # Agora com a proteção contra erros
    teaser = get_market_teaser()
    if teaser:
        cols = st.columns(len(teaser))
        for i, (name, (val, chg)) in enumerate(teaser.items()):
            color = "#10b981" if chg > 0 else "#ef4444"
            with cols[i]:
                st.markdown(f"""
                <div style="text-align:center; background:rgba(255,255,255,0.05); padding:10px; border-radius:8px;">
                    <span style="color:#cbd5e1; font-size:0.8rem;">{name}</span><br>
                    <span style="color:#fff; font-weight:bold; font-size:1.2rem;">{val:.2f}</span>
                    <span style="color:{color}; font-size:0.9rem; margin-left:5px;">{chg:+.2f}%</span>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # === CONTEÚDO EDUCACIONAL (HME, SMC, ETC) ===
    
    # 1. HME vs Realidade
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.subheader("1. HME e a Ineficiência do Preço")
        st.markdown("""
        A **Hipótese dos Mercados Eficientes (Fama, 1970)** sugere que o preço reflete todas as informações instantaneamente. 
        Nós discordamos. Em timeframes curtos (M5), o mercado é **Ineficiente e Emocional**.
        <br><br>
        A Intelligence Flow explora essa falha (Delay de Arbitragem).
        """, unsafe_allow_html=True)
    with c2:
         if anim_network:
            st_lottie(anim_network, height=200, key="net_anim")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Memorial de Cálculo
    st.subheader("2. Memorial de Cálculo: A Matemática da Arbitragem")
    col_math, col_desc = st.columns([1, 1.5])
    
    with col_math:
        st.markdown("""
        <div class="math-box" style="font-family:'Courier New'; background:rgba(0,0,0,0.3); padding:15px; border-left:3px solid #f59e0b; color:#fbbf24;">
        <b>Paridade Teórica:</b><br><br>
        $$P_{Justo} = (P_{NY} \\times FX_{Dolar}) + Spread$$
        <br><br>
        <b>Gap Operacional:</b><br>
        $$Gap_{\%} = \\frac{P_{Tela} - P_{Justo}}{P_{Tela}}$$
        </div>
        """, unsafe_allow_html=True)
        
    with col_desc:
        st.markdown("""
        Se o preço de tela da **Petrobras (PETR4)** no Brasil é **R$ 35,00**, mas o nosso cálculo aponta que, convertido de Nova York, ela deveria custar **R$ 35,20**:
        <br>
        1. Existe um **GAP de R$ 0,20**.
        2. O robô HFT compra no Brasil (Barato).
        3. O sistema alerta a oportunidade na Área do Trader.
        """)

    st.markdown("---")

    # 3. Módulo IA
    st.subheader("3. Módulo Intelligence AI 🤖")
    st.markdown("Simulação de processamento de notícias via NLP (Natural Language Processing).")
    
    c_news1, c_news2 = st.columns(2)
    with c_news1:
        st.markdown("""
        <div style="border:1px solid #334155; padding:15px; border-radius:10px; background:rgba(15, 23, 42, 0.6);">
            <div style="font-size:0.8rem; color:#94a3b8;">REUTERS • 10:04</div>
            <div style="color:white; font-weight:bold;">Fed Chairman Powell hints at rate cut</div>
            <br><span style="background:#16a34a; color:white; padding:2px 8px; font-size:0.7rem;">BULLISH USD</span>
        </div>
        """, unsafe_allow_html=True)

    with c_news2:
        st.markdown("""
        <div style="border:1px solid #334155; padding:15px; border-radius:10px; background:rgba(15, 23, 42, 0.6);">
            <div style="font-size:0.8rem; color:#94a3b8;">BLOOMBERG • 10:02</div>
            <div style="color:white; font-weight:bold;">Iron Ore futures drop 2% in Dalian</div>
            <br><span style="background:#dc2626; color:white; padding:2px 8px; font-size:0.7rem;">BEARISH VALE3</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
