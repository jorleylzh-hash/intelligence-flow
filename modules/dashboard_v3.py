import streamlit as st
import yfinance as yf
import pandas as pd

# --- CSS DE ALTO NÍVEL (Dark Mode + Glassmorphism) ---
def apply_premium_styles():
    st.markdown("""
    <style>
        /* Imagem de Fundo (Abstrato Tech) */
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1639322537228-f710d846310a?q=80&w=2600&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        
        /* Máscara escura para ler o texto */
        .stApp::before {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85);
            z-index: -1;
        }

        /* Tipografia */
        h1, h2, h3 { color: #fff !important; font-family: 'Helvetica Neue', sans-serif; }
        p, li { color: #cbd5e1 !important; font-size: 1.1rem; line-height: 1.6; }

        /* Container de Vidro (Glassmorphism) */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            transition: transform 0.3s ease;
        }
        .glass-card:hover { transform: translateY(-5px); border-color: #3b82f6; }

        /* Destaques de Texto */
        .highlight { color: #60a5fa; font-weight: bold; }
        .success { color: #34d399; font-weight: bold; }
        .danger { color: #f87171; font-weight: bold; }

        /* Métricas */
        div[data-testid="stMetricValue"] { color: #fff !important; font-size: 1.8rem !important; }
        div[data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_simple_data():
    # Busca rápida de dados para o ticker
    tickers = {'S&P500': '^GSPC', 'Dólar (DXY)': 'DX-Y.NYB', 'Petróleo': 'BZ=F', 'Vale (NY)': 'VALE'}
    data = yf.download(list(tickers.values()), period="2d", progress=False)['Close']
    
    # Tratamento seguro de MultiIndex
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
        
    results = {}
    for name, ticker in tickers.items():
        if ticker in data.columns:
            try:
                # Pega o último valor válido
                val = data[ticker].dropna().iloc[-1]
                prev = data[ticker].dropna().iloc[-2]
                delta = ((val - prev)/prev)*100
                results[name] = (val, delta)
            except:
                results[name] = (0.0, 0.0)
        else:
            results[name] = (0.0, 0.0)
    return results

def show_landing_page():
    apply_premium_styles()
    
    # 1. HERO SECTION (Impacto)
    st.markdown("""
    <div style="text-align: center; padding: 60px 0;">
        <h1 style="font-size: 3.5rem; font-weight: 800; background: -webkit-linear-gradient(45deg, #3b82f6, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            INTELLIGENCE FLOW
        </h1>
        <p style="font-size: 1.5rem; color: #e2e8f0; max-width: 800px; margin: 0 auto;">
            Monitoramento Institucional de Fluxo, Arbitragem e Assimetria de Mercado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. TICKER TAPE (Dados)
    vals = get_simple_data()
    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    keys = list(vals.keys())
    
    for i, col in enumerate(cols):
        name = keys[i]
        val, delta = vals[name]
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; text-align:center; border:1px solid #333;">
                <div style="font-size:0.9rem; color:#aaa;">{name}</div>
                <div style="font-size:1.4rem; color:#fff; font-weight:bold;">{val:.2f}</div>
                <div style="font-size:0.9rem; color:{'#4ade80' if delta > 0 else '#f87171'};">{delta:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. CONTEÚDO EDUCACIONAL (LAYOUT DE CARDS)
    
    # BLOCO 1: CORRELAÇÃO B3 vs NYSE
    st.markdown("## 🌐 B3 vs. NYSE: A Dinâmica do Fluxo")
    st.markdown("""
    <div class="glass-card">
        <h3>Quem move o preço?</h3>
        <p>
            O Brasil é um passageiro no trem global. O motorista é Nova York (NYSE).<br>
            Nossa plataforma monitora o <span class="highlight">EWZ (ETF do Brasil nos EUA)</span>. 
            Muitas vezes, os movimentos começam lá fora 10 a 15 minutos antes de impactar o IBOVESPA aqui.
            <br><br>
            <ul>
                <li><span class="success">Correlação Positiva (+):</span> Se S&P500 e Commodities sobem, Brasil tende a subir.</li>
                <li><span class="danger">Correlação Negativa (-):</span> Se Dólar (DXY) e Juros Americanos sobem, Brasil tende a cair (fuga de capital).</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # BLOCO 2: ARBITRAGEM E GAP
    st.markdown("## ⚡ Arbitragem & Gaps de Preço")
    c_left, c_right = st.columns(2)
    
    with c_left:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <h3>O que é Arbitragem?</h3>
            <p>
                Ativos como <b>Petrobras (PETR4)</b> e <b>Vale (VALE3)</b> são negociados em dois lugares ao mesmo tempo: São Paulo e Nova York.
                <br><br>
                Matematicamente, o preço deve ser idêntico (convertido pelo Dólar).
                Quando há diferença, robôs de alta frequência (HFT) compram onde está barato e vendem onde está caro.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c_right:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <h3>O Gap de Lucro</h3>
            <p>
                Chamamos de <span class="highlight">GAP DE ARBITRAGEM</span> a diferença momentânea entre o preço teórico e o preço real.
                <br><br>
                <b>Exemplo:</b> Se a Petrobras sobe 2% em NY e o Dólar está estável, a PETR4 no Brasil tem a "obrigação" matemática de subir 2%.
                Se ela subiu apenas 0.5%, existe um <b>Gap de 1.5%</b> para capturar.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 4. CTA (CHAMADA PARA AÇÃO)
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 40px;">
        <h2>Pronto para operar com dados institucionais?</h2>
        <p>Acesse a Mesa de Operações para visualizar os Gaps em tempo real.</p>
        <br>
        <div style="color: #64748b; font-size: 0.9rem;">Intelligence Flow Solutions © 2026</div>
    </div>
    """, unsafe_allow_html=True)
