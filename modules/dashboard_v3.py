import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time
import requests
from streamlit_lottie import st_lottie

# --- FUNÇÃO PARA CARREGAR ANIMAÇÕES LOTTIE ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- URLs DAS ANIMAÇÕES (Touro, Urso, Radar) ---
ANIMATIONS = {
    "bull": "https://lottie.host/96a60472-e28a-4d7a-8742-5cb0f9188e99/l0pW75zWlG.json", # Touro
    "bear": "https://lottie.host/46497332-95e0-4966-993d-d7967b55f696/P5nI8S4z2L.json", # Urso
    "neutral": "https://lottie.host/8b456108-8e6f-4099-8051-544490d6d532/t5p2iqC9rM.json" # Radar Tech
}

# --- BANCO DE DADOS DE CONTEXTO (A "WIKIPEDIA" DO TRADER) ---
ASSET_INFO = {
    "WIN": {
        "name": "MINI ÍNDICE (FUTURO)",
        "desc": "Derivativo do Ibovespa. Representa a expectativa futura da carteira teórica de ações do Brasil.",
        "specs": {"tick": "R$ 0,20 (5 pts)", "margin": "R$ 100,00 (Aprox)", "vol": "Alta"},
        "context": [
            "1. A formação do preço depende das Blue Chips (VALE3, PETR4, ITUB4).",
            "2. PETR4 e VALE3 seguem suas ADRs (PBR e VALE) negociadas em Nova York.",
            "3. O fluxo dessas ADRs depende do Dólar (DXY) e dos Juros Americanos (Treasuries).",
            "4. RESUMO: Se Juros EUA sobem -> Dólar sobe -> Commodities caem -> WIN cai."
        ]
    },
    "WDO": {
        "name": "MINI DÓLAR (FUTURO)",
        "desc": "Contrato futuro de taxa de câmbio de Reais por Dólar dos EUA.",
        "specs": {"tick": "R$ 5,00 (0.5 pts)", "margin": "R$ 150,00 (Aprox)", "vol": "Média/Alta"},
        "context": [
            "1. Correlação direta com os Juros Futuros (DI) locais.",
            "2. Sensível ao DXY (Dólar contra moedas fortes no mundo).",
            "3. Funciona como proteção (Hedge) para carteiras de ações.",
            "4. RESUMO: Risco Fiscal Brasil ou Juros EUA altos -> WDO sobe."
        ]
    }
}

# --- CSS FUTURISTA ---
def apply_cyber_styles():
    st.markdown("""
    <style>
        .cyber-card {
            background: rgba(16, 185, 129, 0.05);
            border: 1px solid #10b981;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
            margin-bottom: 10px;
        }
        .cyber-card-red {
            background: rgba(239, 68, 68, 0.05);
            border: 1px solid #ef4444;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
            margin-bottom: 10px;
        }
        .tech-text { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #a8a29e; }
        .big-number { font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def show_dashboard():
    apply_cyber_styles()
    
    # Carrega animações
    lottie_bull = load_lottieurl(ANIMATIONS["bull"])
    lottie_bear = load_lottieurl(ANIMATIONS["bear"])
    lottie_radar = load_lottieurl(ANIMATIONS["neutral"])

    # --- SELETOR DE MISSÃO (ATIVO) ---
    col_sel1, col_sel2, col_sel3 = st.columns([1,2,1])
    with col_sel2:
        selected_asset = st.selectbox("SELECIONE O ATIVO PARA ANÁLISE TÁTICA:", ["WIN", "WDO"], index=0)

    # --- MOTOR DE DADOS ---
    def get_market_data():
        TICKERS = {
            'USDBRL': 'BRL=X', 'SPX': '^GSPC', 'EWZ': 'EWZ', 'TNX': '^TNX', 
            'VALE_ADR': 'VALE', 'PBR_ADR': 'PBR', 'PETR4': 'PETR4.SA', 'VALE3': 'VALE3.SA'
        }
        try:
            txt = " ".join(list(TICKERS.values()))
            data = yf.download(txt, period="2d", interval="1d", progress=False)['Close']
            
            # Cálculo seguro de variação
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

    placeholder = st.empty()

    while True:
        data = get_market_data()
        
        if data:
            with placeholder.container():
                
                # --- CÁLCULO DO VIÉS (O CÉREBRO) ---
                # Score simples: EWZ + SPX - TNX (Se juros sobem, bolsa cai)
                score = (data['EWZ']['chg'] * 2) + data['SPX']['chg'] - data['TNX']['chg']
                
                # Define Sentimento
                sentiment = "NEUTRO"
                anim = lottie_radar
                color_class = "cyber-card"
                text_color = "#a8a29e" # Cinza
                
                if score > 0.3:
                    sentiment = "COMPRADOR (BULLISH)"
                    anim = lottie_bull
                    color_class = "cyber-card"
                    text_color = "#10b981" # Verde
                elif score < -0.3:
                    sentiment = "VENDEDOR (BEARISH)"
                    anim = lottie_bear
                    color_class = "cyber-card-red"
                    text_color = "#ef4444" # Vermelho

                # --- LAYOUT PRINCIPAL (2 COLUNAS) ---
                c_left, c_right = st.columns([1, 2])
                
                # === COLUNA DA ESQUERDA: O AVATAR ===
                with c_left:
                    st.markdown(f"<div class='{color_class}' style='text-align: center;'>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:{text_color}; margin:0;'>{sentiment}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p class='tech-text'>SCORE DE FLUXO: {score:.2f}</p>", unsafe_allow_html=True)
                    
                    # A Animação mágica
                    st_lottie(anim, height=200, key=f"anim_{time.time()}")
                    
                    st.markdown("---")
                    # Dados do Ativo Selecionado
                    info = ASSET_INFO[selected_asset]
                    st.markdown(f"**{info['name']}**")
                    st.markdown(f"💰 Tick: `{info['specs']['tick']}`")
                    st.markdown(f"🛡️ Margem: `{info['specs']['margin']}`")
                    st.markdown("</div>", unsafe_allow_html=True)

                # === COLUNA DA DIREITA: A NEURAL NETWORK (CONTEXTO) ===
                with c_right:
                    st.markdown(f"### 🧠 LÓGICA DE PRECIFICAÇÃO: {selected_asset}")
                    
                    # 1. Pipeline Visual (Setas)
                    if selected_asset == "WIN":
                        st.markdown("""
                        <div style="display:flex; justify-content:space-between; align-items:center; background:#1c1917; padding:10px; border-radius:8px; margin-bottom:15px;">
                            <div style="text-align:center;"><span style="font-size:20px;">🇺🇸</span><br><span style="font-size:10px; color:#ef4444;">TREASURIES</span></div>
                            <div style="color:#555;">➜</div>
                            <div style="text-align:center;"><span style="font-size:20px;">💵</span><br><span style="font-size:10px; color:#3b82f6;">DÓLAR</span></div>
                            <div style="color:#555;">➜</div>
                            <div style="text-align:center;"><span style="font-size:20px;">📉</span><br><span style="font-size:10px; color:#facc15;">ADRS (NY)</span></div>
                            <div style="color:#555;">➜</div>
                            <div style="text-align:center; border: 1px solid #10b981; padding: 5px; border-radius: 5px;"><span style="font-size:20px;">🇧🇷</span><br><span style="font-size:10px; color:#10b981;">WIN (IBOV)</span></div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style="display:flex; justify-content:space-between; align-items:center; background:#1c1917; padding:10px; border-radius:8px; margin-bottom:15px;">
                            <div style="text-align:center;"><span style="font-size:20px;">🇺🇸</span><br><span style="font-size:10px; color:#ef4444;">TREASURIES</span></div>
                            <div style="color:#555;">➜</div>
                            <div style="text-align:center;"><span style="font-size:20px;">🌎</span><br><span style="font-size:10px; color:#3b82f6;">DXY GLOBAL</span></div>
                            <div style="color:#555;">➜</div>
                            <div style="text-align:center;"><span style="font-size:20px;">📈</span><br><span style="font-size:10px; color:#facc15;">J. FUTUROS (DI)</span></div>
                            <div style="color:#555;">➜</div>
                            <div style="text-align:center; border: 1px solid #10b981; padding: 5px; border-radius: 5px;"><span style="font-size:20px;">💲</span><br><span style="font-size:10px; color:#10b981;">WDO (DÓLAR)</span></div>
                        </div>
                        """, unsafe_allow_html=True)

                    # 2. Explicação Contextual (Expansível)
                    with st.expander("📚 ENTENDER O CONTEXTO MACRO (CLIQUE)", expanded=True):
                        for item in ASSET_INFO[selected_asset]["context"]:
                            st.caption(item)
                    
                    st.divider()

                    # 3. Dados Reais de Correlação
                    st.markdown("#### 📡 DADOS DE IMPACTO")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("TREASURIES", f"{data['TNX']['chg']:.2f}%", help="Juros EUA 10 Anos")
                    c2.metric("EWZ (BRAZIL)", f"{data['EWZ']['chg']:.2f}%", help="ETF do Brasil em NY")
                    if selected_asset == "WIN":
                        c3.metric("ADR VALE", f"{data['VALE_ADR']['chg']:.2f}%")
                        c4.metric("ADR PETRO", f"{data['PBR_ADR']['chg']:.2f}%")
                    else:
                        c3.metric("DÓLAR SPOT", f"{data['USDBRL']['chg']:.2f}%")
                        c4.metric("S&P 500", f"{data['SPX']['chg']:.2f}%")

        time.sleep(15)
