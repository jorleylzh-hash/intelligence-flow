import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd

# --- FUNÇÃO DE DADOS (Mantida para o Ticker) ---
@st.cache_data(ttl=300)
def get_market_data():
    tickers = {'S&P500': '^GSPC', 'DXY': 'DX-Y.NYB', 'BRENT': 'BZ=F', 'EWZ': 'EWZ'}
    try:
        data = yf.download(list(tickers.values()), period="2d", progress=False)['Close']
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.droplevel(1)
        results = {}
        for name, ticker in tickers.items():
            if ticker in data.columns:
                val = data[ticker].dropna().iloc[-1]
                prev = data[ticker].dropna().iloc[-2]
                results[name] = (val, ((val-prev)/prev)*100)
            else: results[name] = (0.0, 0.0)
        return results
    except: return None

# --- A MÁGICA DO FRONTEND (HTML/JS/CSS) ---
def get_animated_timeline_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;600&display=swap');
        
        body { background-color: transparent; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        
        /* LINHA DO TEMPO (Timeline Central) */
        .timeline {
            position: relative;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 0;
        }
        .timeline::after {
            content: '';
            position: absolute;
            width: 4px;
            background-color: #3b82f6;
            top: 0;
            bottom: 0;
            left: 50%;
            margin-left: -2px;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
        }

        /* CONTAINER DO CARD */
        .container {
            padding: 10px 40px;
            position: relative;
            background-color: inherit;
            width: 50%;
            opacity: 0; /* Invisível no início */
            transition: all 1s ease;
        }
        
        .left { left: -60px; transform: translateX(-100px); }
        .right { left: 50%; transform: translateX(100px); }
        
        /* Quando visível (Classe adicionada pelo JS) */
        .visible { opacity: 1; transform: translateX(0); }

        /* BOLINHA NO MEIO */
        .container::after {
            content: '';
            position: absolute;
            width: 20px;
            height: 20px;
            right: -11px;
            background-color: #0f172a;
            border: 4px solid #3b82f6;
            top: 25px;
            border-radius: 50%;
            z-index: 1;
            transition: background 0.3s;
        }
        .right::after { left: -9px; }
        .container:hover::after { background-color: #60a5fa; box-shadow: 0 0 20px #3b82f6; }

        /* O CARD EM SI */
        .content {
            padding: 25px;
            background: rgba(20, 25, 40, 0.9);
            border: 1px solid #334155;
            border-radius: 12px;
            position: relative;
            cursor: pointer;
            transition: transform 0.3s, border 0.3s;
            backdrop-filter: blur(10px);
        }
        .content:hover {
            transform: scale(1.02);
            border-color: #3b82f6;
        }

        /* TEXTOS */
        h2 { margin: 0 0 10px 0; color: #fff; font-size: 1.2rem; }
        p { margin: 0; color: #94a3b8; font-size: 0.95rem; line-height: 1.5; }

        /* ÁREA DE ANIMAÇÃO OCULTA */
        .anim-box {
            height: 0;
            overflow: hidden;
            transition: height 0.5s ease;
            margin-top: 0;
            border-top: 1px solid transparent;
        }
        
        /* Quando Clicado (Expandido) */
        .content.active .anim-box {
            height: 120px; /* Altura da animação */
            margin-top: 15px;
            border-top: 1px solid #334155;
            padding-top: 15px;
        }
        
        /* --- ANIMAÇÕES CSS PURAS (Micro-Interações) --- */
        
        /* 1. SPREAD / DIVERGÊNCIA */
        .spread-anim {
            width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; gap: 10px;
        }
        .bar { width: 10px; height: 50px; background: #3b82f6; border-radius: 4px; transition: 0.5s; }
        .content.active .bar-1 { animation: divergeUp 1s infinite alternate; background: #10b981; }
        .content.active .bar-2 { animation: divergeDown 1s infinite alternate; background: #ef4444; }
        
        @keyframes divergeUp { 0% { height: 40px; transform: translateY(0); } 100% { height: 80px; transform: translateY(-10px); } }
        @keyframes divergeDown { 0% { height: 40px; transform: translateY(0); } 100% { height: 80px; transform: translateY(10px); } }

        /* 2. GAP CLOSING (ARBITRAGEM) */
        .gap-anim { position: relative; width: 100%; height: 60px; }
        .line { position: absolute; height: 4px; width: 80%; background: #64748b; top: 30px; left: 10%; }
        .ball { width: 15px; height: 15px; border-radius: 50%; position: absolute; top: 24px; }
        .ball-1 { left: 10%; background: #ef4444; }
        .ball-2 { right: 10%; background: #10b981; }
        
        .content.active .ball-1 { animation: smashRight 1s forwards; }
        .content.active .ball-2 { animation: smashLeft 1s forwards; }
        
        @keyframes smashRight { to { left: 48%; } }
        @keyframes smashLeft { to { right: 48%; } }

    </style>
    </head>
    <body>

    <div class="timeline">
    
        <div class="container left">
            <div class="content" onclick="this.classList.toggle('active')">
                <h2>🌎 1. O Fluxo Macro Global</h2>
                <p>Tudo começa nos EUA. Juros (Treasuries) e Dólar (DXY) definem a direção. Se o Dólar sobe lá, a liquidez seca aqui.</p>
                <div style="font-size:0.8rem; color:#60a5fa; margin-top:10px;">👇 Clique para ver a Correlação</div>
                <div class="anim-box">
                    <div style="text-align:center; color:#fff; margin-bottom:5px;">S&P500 vs IBOV</div>
                    <div class="spread-anim">
                        <div class="bar bar-1"></div>
                        <div class="bar bar-2"></div>
                    </div>
                </div>
            </div>
        </div>

        <div class="container right">
            <div class="content" onclick="this.classList.toggle('active')">
                <h2>⚖️ 2. Assimetria de Preço</h2>
                <p>Identificamos quando o ativo no Brasil (PETR4) ignora o movimento do ativo espelho em NY (PBR). Isso gera um GAP.</p>
                <div style="font-size:0.8rem; color:#60a5fa; margin-top:10px;">👇 Clique para fechar o GAP</div>
                <div class="anim-box">
                    <div style="text-align:center; color:#fff; margin-bottom:15px;">Fechamento de Arbitragem</div>
                    <div class="gap-anim">
                        <div class="line"></div>
                        <div class="ball ball-1"></div>
                        <div class="ball ball-2"></div>
                    </div>
                </div>
            </div>
        </div>

        <div class="container left">
            <div class="content" onclick="this.classList.toggle('active')">
                <h2>🚀 3. Execução HFT</h2>
                <p>Nossa mesa proprietária atua exatamente no fechamento desse spread. Latência zero e execução precisa.</p>
                <div style="font-size:0.8rem; color:#60a5fa; margin-top:10px;">👇 Clique para simular trade</div>
                 <div class="anim-box">
                    <div style="display:flex; justify-content:space-around; align-items:center; height:100%;">
                        <div style="color:#10b981; font-weight:bold; font-size:1.2rem;">BUY NY</div>
                        <div style="font-size:1.5rem;">⚡</div>
                        <div style="color:#ef4444; font-weight:bold; font-size:1.2rem;">SELL B3</div>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <script>
        // O CÓDIGO JS QUE FAZ OS CARDS APARECEREM AO ROLAR (Scroll Observer)
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        });

        // Manda o observador vigiar todos os containers
        document.querySelectorAll('.container').forEach(box => {
            observer.observe(box);
        });
    </script>

    </body>
    </html>
    """

# --- FUNÇÃO PRINCIPAL ---
def show_landing_page():
    # Estilos Básicos do Streamlit (Fundo e Texto)
    st.markdown("""
    <style>
        .stApp { background-color: #020617; }
        h1 { color: #fff; font-family: sans-serif; }
    </style>
    """, unsafe_allow_html=True)

    # 1. HEADER
    st.markdown("""
    <div style="text-align:center; padding: 50px 20px;">
        <h1 style="font-size: 3rem; background: -webkit-linear-gradient(45deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            INTELLIGENCE FLOW
        </h1>
        <p style="color: #94a3b8; font-size: 1.2rem;">Dinâmica de Mercado & Arbitragem Institucional</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. TICKER TAPE (DADOS REAIS PYTHON)
    data = get_market_data()
    if data:
        c1, c2, c3, c4 = st.columns(4)
        cols = [c1, c2, c3, c4]
        for i, (name, (val, chg)) in enumerate(data.items()):
            cols[i].markdown(f"""
            <div style="background:#0f172a; border:1px solid #1e293b; border-radius:8px; padding:10px; text-align:center;">
                <div style="color:#64748b; font-size:0.8rem;">{name}</div>
                <div style="color:#f8fafc; font-weight:bold; font-size:1.2rem;">{val:.2f}</div>
                <div style="color:{'#22c55e' if chg>0 else '#ef4444'}; font-size:0.9rem;">{chg:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. A LINHA DO TEMPO INTERATIVA (IFRAME)
    # Altura fixa calculada para caber os cards (scrolling acontece dentro da página ou no iframe)
    components.html(get_animated_timeline_html(), height=800, scrolling=True)

    # 4. FOOTER
    st.markdown("<div style='text-align:center; color:#334155; padding:30px;'>Intelligence Flow © 2026</div>", unsafe_allow_html=True)
