import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_lottie import st_lottie
import requests

# --- 1. CONFIGURAÇÃO VISUAL & CSS (Fundo Cinza Suave + Contraste Alto) ---
def apply_landing_css():
    st.markdown("""
    <style>
        /* FUNDO GERAL: Cinza 'Ardósia' muito suave (conforto visual) */
        .stApp { background-color: #F1F5F9; }
        
        /* FONTES: Escuras para leitura perfeita */
        h1, h2, h3 { color: #0f172a !important; font-family: 'Segoe UI', sans-serif; font-weight: 700; }
        p, li { color: #334155 !important; font-size: 1.15rem; line-height: 1.7; }
        
        /* HERO SECTION: Gradiente Azul Institucional */
        .hero-section {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 80px 20px;
            text-align: center;
            border-radius: 0 0 40px 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            margin-bottom: 50px;
            color: white !important;
        }
        .hero-title {
            font-size: 3.5rem; color: #fff !important; margin-bottom: 15px; text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        .hero-sub { color: #cbd5e1 !important; font-size: 1.3rem; max-width: 800px; margin: 0 auto; }
        
        /* CARDS BRANCOS (Para destacar do fundo cinza) */
        .content-card {
            background: #ffffff;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border-left: 6px solid #3b82f6; /* Detalhe azul */
            margin-bottom: 30px;
            transition: transform 0.3s;
        }
        .content-card:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); }
        
        /* DESTAQUES PNL (Negrito e Cor) */
        .pain-point { color: #dc2626; font-weight: bold; }
        .pleasure-point { color: #16a34a; font-weight: bold; }
        .blue-highlight { color: #2563eb; font-weight: bold; }

        /* TICKER TAPE (Dados Reais) */
        .ticker-box {
            background: white; border-radius: 8px; padding: 15px; text-align: center;
            border: 1px solid #e2e8f0; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNÇÕES DE DADOS E ASSETS ---
def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

@st.cache_data(ttl=300)
def get_market_teaser():
    # Dados reais para provar "Veracidade"
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

# --- 3. A NARRATIVA (PÁGINA) ---
def show_landing_page():
    apply_landing_css()
    
    # Animações (Visual)
    anim_analise = load_lottie("https://assets3.lottiefiles.com/packages/lf20_qp1q7mct.json")
    anim_speed = load_lottie("https://assets5.lottiefiles.com/packages/lf20_w51pcehl.json")

    # === SEÇÃO 1: HERO (IMPACTO & PROMESSA) ===
    # PNL: Foco no resultado final (Clareza)
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">INTELLIGENCE FLOW</h1>
        <p class="hero-sub">
            Pare de operar gráficos cegos. Comece a operar o <b>Fluxo Institucional</b>.
            <br>A única plataforma que conecta a B3 à NYSE em tempo real.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # === SEÇÃO 2: PROVA SOCIAL (DADOS REAIS) ===
    # PNL: Gatilho da "Verdade". Mostramos dados ao vivo logo de cara.
    teaser = get_market_teaser()
    if teaser:
        st.markdown("<h3 style='text-align:center; margin-bottom:20px;'>📡 Monitoramento Global Agora</h3>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        cols = [c1, c2, c3]
        for i, (name, (val, chg)) in enumerate(teaser.items()):
            color = "#16a34a" if chg > 0 else "#dc2626"
            with cols[i]:
                st.markdown(f"""
                <div class="ticker-box">
                    <div style="font-size:0.9rem; color:#64748b; font-weight:600;">{name}</div>
                    <div style="font-size:1.6rem; color:#0f172a; font-weight:bold;">{val:.2f}</div>
                    <div style="color:{color}; font-weight:bold;">{chg:+.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-top: 1px solid #cbd5e1;'><br>", unsafe_allow_html=True)

    # === SEÇÃO 3: A DOR (AGITAÇÃO) ===
    # PNL: Tocar na ferida do trader (Loss inexplicável)
    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.markdown("""
        <div style="padding: 20px;">
            <h2>🚫 O Erro Invisível</h2>
            <p>
                Você já abriu uma compra perfeita no gráfico de 5 minutos, o candle era de força, os indicadores estavam verdes... 
                e de repente o mercado <span class="pain-point">virou contra você violentamente?</span>
                <br><br>
                Isso não foi azar. Foi fluxo.
                <br><br>
                Enquanto você olhava para o <b>Win Futuro</b>, os robôs de HFT estavam vendendo o <b>EWZ em Nova York</b> 2 minutos antes.
                Você estava operando o passado. Eles operavam o futuro.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with c_right:
        if anim_analise:
            st_lottie(anim_analise, height=350, key="anim1")

    # === SEÇÃO 4: A SOLUÇÃO (BENEFÍCIOS POR PERFIL) ===
    st.markdown("<br><h2 style='text-align:center;'>A Vantagem Intelligence Flow</h2><br>", unsafe_allow_html=True)

    # Card 1: Day Trade
    st.markdown("""
    <div class="content-card">
        <h3>⚡ Para o Day Trader (M5)</h3>
        <p>
            Imagine ter um radar que avisa <b>"Perigo à frente"</b> antes do preço cair.
            <br><br>
            Monitoramos Gaps de Arbitragem entre PETR4 (Brasil) e PBR (EUA). Quando o spread abre, existe uma força magnética que puxa o preço.
            <br>
            <span class="pleasure-point">✅ Resultado:</span> Você para de entrar em rompimentos falsos e começa a operar junto com os robôs gringos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Card 2: Swing Trade
    st.markdown("""
    <div class="content-card" style="border-left-color: #10b981;">
        <h3>📅 Para o Swing Trader (Posição)</h3>
        <p>
            Segurança patrimonial exige visão macro. Não adianta a VALE3 estar "barata" se o Minério na China perdeu o fundo.
            <br><br>
            Nossa plataforma cruza Juros Americanos (Treasuries) com Commodities.
            <br>
            <span class="pleasure-point">✅ Resultado:</span> Você só se posiciona quando o Cenario Macro valida a sua análise técnica. Proteção total.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # === SEÇÃO 5: TECNOLOGIA ===
    c_tec1, c_tec2 = st.columns([1, 1.5])
    with c_tec1:
        if anim_speed:
            st_lottie(anim_speed, height=250, key="anim2")
    with c_tec2:
        st.markdown("""
        <div style="padding-top: 40px;">
            <h3>🤖 Tecnologia Proprietária</h3>
            <p>
                Não usamos dados atrasados de corretoras comuns. Possuímos conexão via API de baixa latência.
                <br><br>
                <ul>
                    <li>Algoritmos de Paridade em Tempo Real.</li>
                    <li>Cálculo de 'Preço Justo' via Dólar e Juros.</li>
                    <li>Infraestrutura 100% em Nuvem (Sempre online).</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # === SEÇÃO 6: CTA (CHAMADA PARA AÇÃO) ===
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #1e293b; color: white; padding: 50px; border-radius: 20px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <h2 style="color:white !important;">A informação é a sua maior vantagem.</h2>
        <p style="color:#cbd5e1 !important; margin-bottom: 30px;">
            Não deixe para operar amanhã com as ferramentas de ontem.
        </p>
        <p style="font-size: 0.9rem; background: #3b82f6; padding: 10px 20px; border-radius: 30px; display: inline-block;">
            👉 Acesse a <b>Área do Trader</b> no menu lateral para iniciar
        </p>
    </div>
    <br><br>
    """, unsafe_allow_html=True)

    # Rodapé
    st.markdown("<div style='text-align:center; color:#94a3b8;'>Intelligence Flow Solutions © 2026 • Curitiba/PR • Paranaguá/PR</div>", unsafe_allow_html=True)
