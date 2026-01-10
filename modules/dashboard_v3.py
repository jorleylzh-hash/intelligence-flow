import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- TECNOLOGIA VISUAL NOVA: CSS PURO (Sem JSON/Lottie) ---
def apply_css_animations():
    st.markdown("""
    <style>
        /* Animação de Pulso para Indicadores ao Vivo */
        @keyframes pulse-green {
            0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
            100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }
        
        .live-indicator {
            width: 12px;
            height: 12px;
            background-color: #10b981;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: pulse-green 2s infinite;
        }

        /* Card Institucional Moderno */
        .info-card {
            background: rgba(15, 23, 42, 0.6);
            border-left: 4px solid #3b82f6;
            padding: 20px;
            border-radius: 0 10px 10px 0;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600) # Cache aumentado para 10 min para evitar Database Lock
def get_market_teaser():
    tickers = {'S&P 500': '^GSPC', 'DXY': 'DX-Y.NYB', 'EWZ': 'EWZ'}
    try:
        # Threads False é OBRIGATÓRIO no Render
        data = yf.download(list(tickers.values()), period="2d", progress=False, threads=False)['Close']
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.droplevel(1)
        results = {}
        for name, ticker in tickers.items():
            if ticker in data.columns:
                series = data[ticker].dropna()
                if len(series) >= 2:
                    val = series.iloc[-1]
                    chg = ((val - series.iloc[-2])/series.iloc[-2])*100
                    results[name] = (val, chg)
        return results
    except: return None

def show_landing_page():
    apply_css_animations()

    # === HERO SECTION ===
    st.markdown("""
    <div style="text-align: center; padding: 60px 0;">
        <h1 style="font-size: 4rem; margin-bottom: 10px; color: #f8fafc;">
            INTELLIGENCE FLOW
        </h1>
        <p style="font-size: 1.2rem; color: #94a3b8; letter-spacing: 2px;">
            TRATAMENTO DE DADOS LTDA
        </p>
        <div style="margin-top: 20px;">
            <span class="live-indicator"></span><span style="color:#10b981; font-weight:bold;">SISTEMA OPERACIONAL • CONEXÃO B3/NYSE ESTÁVEL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === DADOS DE MERCADO ===
    teaser = get_market_teaser()
    if teaser:
        cols = st.columns(3)
        for i, (name, (val, chg)) in enumerate(teaser.items()):
            color = "#10b981" if chg > 0 else "#ef4444"
            with cols[i]:
                st.markdown(f"""
                <div style="text-align:center; background:rgba(255,255,255,0.05); padding:15px; border-radius:8px;">
                    <div style="color:#94a3b8; font-size:0.8rem;">{name}</div>
                    <div style="color:#fff; font-size:1.5rem; font-weight:bold;">{val:,.2f}</div>
                    <div style="color:{color};">{chg:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # === TESE INSTITUCIONAL (TEXTO RICO) ===
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("### 1. A Falácia do Mercado Eficiente")
        st.markdown("""
        <div class="info-card">
            A teoria acadêmica diz que o preço reflete tudo. A realidade do HFT (High Frequency Trading) diz o contrário.
            <br><br>
            Nossos algoritmos exploram a <b>latência informacional</b> entre Nova York e São Paulo. 
            Não operamos gráficos; operamos o fluxo financeiro que constrói o gráfico.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 2. Smart Money Concepts (SMC)")
        st.markdown("""
        <div class="info-card" style="border-left-color: #8b5cf6;">
            Rastreamos <b>Order Blocks</b> e <b>Ineficiências de Liquidez</b>. 
            Identificamos onde os grandes players institucionais posicionaram suas ordens passivas, 
            utilizando o princípio de <i>Full Disclosure</i> do fluxo de ordens.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        # Substituindo Lottie por um Elemento Visual CSS Puro
        st.markdown("""
        <div style="height:100%; display:flex; align-items:center; justify-content:center;">
            <div style="text-align:center; padding:20px; border:1px dashed #334155; border-radius:50%;">
                <h2 style="color:#3b82f6;">AI</h2>
                <p style="font-size:0.8rem;">NEURAL<br>CORE</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # === RODAPÉ COM DADOS REAIS DO PDF ===
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#64748b; font-size:0.8rem;">
        <b style="color:#cbd5e1;">INTELLIGENCE FLOW TRATAMENTO DE DADOS LTDA</b><br>
        CNPJ: 63.698.191/0001-27<br>
        Av. João Gualberto, 1721 - Conj 52, Andar 05 - Edif Vega Business<br>
        Juvevê - Curitiba/PR - CEP 80.030-001<br>
        <br>
        © 2026 Todos os direitos reservados.
    </div>
    """, unsafe_allow_html=True)
