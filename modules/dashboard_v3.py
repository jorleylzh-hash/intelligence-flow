import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_lottie import st_lottie
import requests
from streamlit_lightweight_charts import renderLightweightCharts

# --- 1. CONFIGURAÇÃO E CSS (SCROLL REVEAL) ---
def apply_life_css():
    st.markdown("""
    <style>
        /* Fundo limpo e moderno */
        .stApp { background-color: #f8fafc; }
        
        h1, h2, h3 { font-family: 'Inter', sans-serif; color: #0f172a; }
        
        /* Classe para animação de entrada (Scroll Reveal) */
        .reveal {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.8s ease-out;
        }
        .reveal.active {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* Cards Profissionais */
        .pro-card {
            background: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
            transition: transform 0.3s;
        }
        .pro-card:hover { transform: translateY(-5px); border-color: #3b82f6; }
        
        /* Hero Section com Gradiente Sutil */
        .hero {
            background: radial-gradient(circle at top right, #e0f2fe 0%, #fff 40%);
            padding: 60px 20px;
            border-bottom: 1px solid #e2e8f0;
            text-align: center;
        }
    </style>
    
    <script>
        function reveal() {
            var reveals = document.querySelectorAll(".reveal");
            for (var i = 0; i < reveals.length; i++) {
                var windowHeight = window.innerHeight;
                var elementTop = reveals[i].getBoundingClientRect().top;
                var elementVisible = 150;
                if (elementTop < windowHeight - elementVisible) {
                    reveals[i].classList.add("active");
                }
            }
        }
        window.addEventListener("scroll", reveal);
        reveal(); // Rodar uma vez ao carregar
    </script>
    """, unsafe_allow_html=True)

# --- 2. DADOS E GRÁFICOS (TRADINGVIEW ENGINE) ---
@st.cache_data(ttl=300)
def get_candle_data():
    # Pega dados reais da PETR4 para o gráfico profissional
    df = yf.download("PETR4.SA", period="1mo", interval="1d", progress=False)
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.droplevel(1)
    
    # Formata para o padrão TradingView (Lista de Dicionários)
    candles = []
    for index, row in df.iterrows():
        color = '#26a69a' if row['Close'] >= row['Open'] else '#ef5350'
        candles.append({
            "time": index.strftime('%Y-%m-%d'),
            "open": row['Open'],
            "high": row['High'],
            "low": row['Low'],
            "close": row['Close']
        })
    return candles

def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# --- 3. PÁGINA PRINCIPAL ---
def show_landing_page():
    apply_life_css()
    
    # Carregar Animações
    # Pessoas analisando dados (Corporate)
    anim_analyst = load_lottie("https://assets3.lottiefiles.com/packages/lf20_qp1q7mct.json") 
    # Mercado Financeiro
    anim_market = load_lottie("https://assets4.lottiefiles.com/packages/lf20_hzy33r2p.json")

    # === SEÇÃO 1: HERO (IMPACTO) ===
    st.markdown("""
    <div class="hero reveal active">
        <h1 style="font-size: 3.5rem; font-weight: 800; color: #1e293b; margin-bottom: 10px;">
            INTELLIGENCE <span style="color:#3b82f6;">FLOW</span>
        </h1>
        <p style="font-size: 1.25rem; color: #64748b; max-width: 700px; margin: 0 auto;">
            Onde a tecnologia de alta frequência encontra a análise macroeconômica.
            Identifique assimetrias de mercado antes que elas apareçam no gráfico.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # === SEÇÃO 2: O GRÁFICO 60FPS (O "WOW" FACTOR) ===
    st.markdown("<br>", unsafe_allow_html=True)
    c_chart_desc, c_chart_view = st.columns([1, 2])
    
    with c_chart_desc:
        st.markdown("""
        <div class="pro-card reveal">
            <h3 style="color:#3b82f6;">⚡ Visão Institucional</h3>
            <p style="color:#475569; line-height:1.6;">
                Esqueça gráficos estáticos. Nossa plataforma utiliza renderização <b>Canvas 60fps</b> 
                para entregar a mesma experiência das mesas de Wall Street.
                <br><br>
                <ul>
                    <li>Candles Interativos</li>
                    <li>Zoom & Pan Suave</li>
                    <li>Crosshair de Precisão</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_chart_view:
        # RENDERIZAÇÃO DO GRÁFICO TRADINGVIEW
        candles = get_candle_data()
        if candles:
            chartOptions = {
                "layout": {"backgroundColor": "#FFFFFF", "textColor": "#333"},
                "grid": {"vertLines": {"color": "#f0f3fa"}, "horzLines": {"color": "#f0f3fa"}},
                "height": 400
            }
            series = [{
                "type": 'Candlestick',
                "data": candles,
                "options": {
                    "upColor": '#26a69a', "downColor": '#ef5350',
                    "borderVisible": False, "wickUpColor": '#26a69a', "wickDownColor": '#ef5350'
                }
            }]
            # Componente especial (requer streamlit-lightweight-charts no requirements.txt)
            renderLightweightCharts([{"chart": chartOptions, "series": series}], key='pro_chart')

    st.markdown("---")

    # === SEÇÃO 3: AMBIENTE CORPORATIVO (Animação + Imagens) ===
    st.markdown("<div style='text-align:center; margin: 40px 0;'><h2 class='reveal'>Ecossistema de Alta Performance</h2></div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        # Animação Lottie (Pessoa trabalhando)
        if anim_analyst:
            st_lottie(anim_analyst, height=350, key="analyst")
            
    with c2:
        st.markdown("""
        <div class="pro-card reveal" style="margin-top: 40px;">
            <h3>🧠 Inteligência Humana & Artificial</h3>
            <p style="color:#64748b;">
                Não somos apenas algoritmos. A Intelligence Flow combina:
                <br><br>
                <b>1. Análise Quantitativa:</b> Robôs varrendo milhares de ativos.
                <br>
                <b>2. Curadoria Humana:</b> Traders experientes filtrando o ruído.
                <br><br>
                O resultado? Sinais limpos, confiáveis e executáveis.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # === SEÇÃO 4: CTA ===
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="reveal" style="text-align: center; background: #1e293b; padding: 50px; border-radius: 20px; color: white;">
        <h2>Pronto para operar como um Institucional?</h2>
        <p style="color: #cbd5e1; margin-bottom: 20px;">Acesse a Área do Trader e visualize os sinais agora.</p>
    </div>
    """, unsafe_allow_html=True)
