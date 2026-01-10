import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import plotly.graph_objects as go
import numpy as np

# --- 1. FUNÇÕES AUXILIARES & CACHE ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=2)
        return r.json() if r.status_code == 200 else None
    except: return None

@st.cache_data(ttl=300)
def get_market_teaser():
    tickers = {'S&P 500 Fut': 'ES=F', 'Dólar DXY': 'DX-Y.NYB', 'Treasuries 10Y': '^TNX', 'Bitcoin': 'BTC-USD'}
    try:
        # FIX: threads=False MANTIDO para estabilidade no Render
        data = yf.download(list(tickers.values()), period="2d", progress=False, threads=False)['Close']
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.droplevel(1)
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
    except: return None

# --- 2. CONTEÚDO INSTITUCIONAL (LONG SCROLL) ---
def show_landing_page():
    # Animações Conceituais
    anim_network = load_lottie("https://assets5.lottiefiles.com/packages/lf20_w51pcehl.json")
    anim_chart = load_lottie("https://assets10.lottiefiles.com/packages/lf20_qmfs6c3i.json")

    # =========================================
    # SEÇÃO 1: HERO (A Proposta)
    # =========================================
    st.markdown("""
    <div style="text-align: center; padding: 80px 0 40px 0;">
        <h1 style="font-size: 4.5rem; letter-spacing: -2px; margin-bottom: 20px; background: -webkit-linear-gradient(180deg, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            INTELLIGENCE FLOW
        </h1>
        <h2 style="color: #60a5fa !important; margin-bottom: 30px;">
            Onde a Liquidez Global encontra a Execução de Alta Frequência.
        </h2>
        <p style="font-size: 1.3rem; color: #cbd5e1; max-width: 900px; margin: 0 auto; line-height: 1.8;">
            Somos um ecossistema proprietário que decodifica o rastro do dinheiro institucional antes que ele mova o preço na tela do varejo.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =========================================
    # SEÇÃO 2: MONITORAMENTO GLOBAL (Dados Reais)
    # =========================================
    teaser = get_market_teaser()
    if teaser:
        st.markdown("<p style='text-align:center; font-size:0.9rem; color:#64748b; margin-bottom:10px;'>DRIVERS GLOBAIS EM TEMPO REAL</p>", unsafe_allow_html=True)
        cols = st.columns(len(teaser))
        for i, (name, (val, chg)) in enumerate(teaser.items()):
            color = "#10b981" if chg > 0 else "#ef4444"
            with cols[i]:
                st.markdown(f"""
                <div style="text-align:center; background:rgba(30, 41, 59, 0.5); padding:15px; border-radius:12px; border:1px solid #334155;">
                    <span style="color:#94a3b8; font-size:0.8rem; font-weight:600;">{name}</span><br>
                    <span style="color:#fff; font-weight:bold; font-size:1.4rem;">{val:,.2f}</span><br>
                    <span style="color:{color}; font-size:0.9rem; font-weight:bold;">{chg:+.2f}%</span>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#1e293b;'><br>", unsafe_allow_html=True)

    # =========================================
    # SEÇÃO 3: A TESE CENTRAL (HME vs Realidade)
    # =========================================
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.subheader("1. A Falácia do Mercado Eficiente")
        st.markdown("""
        A teoria acadêmica (HME) diz que o preço atual reflete toda a informação disponível. <span class="highlight-blue">Nós provamos o contrário todos os dias.</span>
        <br><br>
        Em timeframes intradiários (HFT/M5), o mercado é ineficiente, fragmentado e emocional. Existe um **delay mensurável** entre um grande fluxo de venda em Nova York (ADR) e a reação do preço na B3 (Ação Local).
        <br><br>
        A Intelligence Flow vive nesse delay.
        """, unsafe_allow_html=True)
    with c2:
         if anim_network:
            st_lottie(anim_network, height=250, key="net_anim")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # =========================================
    # SEÇÃO 4: SMART MONEY CONCEPTS (SMC) - NOVO!
    # =========================================
    st.subheader("2. Decodificando o 'Smart Money' (Institucional)")
    st.markdown("""
    O varejo busca padrões gráficos (bandeiras, triângulos). O Institucional busca **Liquidez**.
    Nossos algoritmos não rastreiam o preço, eles rastreiam onde as grandes ordens estão repousando.
    """)

    c_smc1, c_smc2, c_smc3 = st.columns(3)
    with c_smc1:
        st.markdown("""
        <div class="tech-box">
            <h4 style="color:#60a5fa !important;">🛑 Liquidity Grabs (Stop Hunts)</h4>
            <p style="font-size:0.95rem;">
                Identificamos movimentos rápidos acima de topos anteriores feitos apenas para acionar stops de varejo e capturar liquidez antes da reversão real.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c_smc2:
        st.markdown("""
        <div class="tech-box">
            <h4 style="color:#60a5fa !important;">📦 Order Blocks (Blocos de Ordens)</h4>
            <p style="font-size:0.95rem;">
                Mapeamos zonas onde grandes players institucionais deixaram rastro de agressão. O preço tende a voltar a essas zonas para "recarregar".
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c_smc3:
        st.markdown("""
        <div class="tech-box">
            <h4 style="color:#60a5fa !important;">⚡ Imbalance (FVG)</h4>
            <p style="font-size:0.95rem;">
                Vazios de liquidez deixados por movimentos agressivos. O mercado tem uma tendência natural de retornar para preencher esses gaps.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#1e293b;'><br>", unsafe_allow_html=True)

    # =========================================
    # SEÇÃO 5: MATEMÁTICA DA ARBITRAGEM (Memorial)
    # =========================================
    st.subheader("3. O 'Motor' Quantitativo: Memorial de Cálculo")
    st.markdown("Não há 'feeling'. Há apenas matemática financeira aplicada em baixa latência.")

    c_math1, c_math2 = st.columns([1.2, 1])
    with c_math1:
        st.markdown("""
        <div style="font-family:'Courier New', monospace; background:rgba(15, 23, 42, 0.8); padding:25px; border-left:4px solid #f59e0b; color:#fbbf24; border-radius:8px;">
        <span style="color:#94a3b8;">// Cálculo do Preço Justo Teórico (Paridade)</span><br><br>
        $$P_{Justo (BRL)} = (P_{ADR (USD)} \\times FX_{Futuro}) + Custo_{Carry}$$
        <br>
        <span style="color:#94a3b8;">// Cálculo do Spread Operacional (Gap)</span><br><br>
        $$Spread_{\\%} = \\left( \\frac{P_{Tela (B3)} - P_{Justo}}{P_{Tela (B3)}} \\right) \\times 100$$
        <br><br>
        <span style="color:#ef4444;">IF Spread > 0.7% THEN Signal = "VENDA ARBITRADA"</span><br>
        <span style="color:#10b981;">IF Spread < -0.7% THEN Signal = "COMPRA ARBITRADA"</span>
        </div>
        """, unsafe_allow_html=True)
    with c_math2:
        st.markdown("""
        <div style="padding:20px;">
            <h4>A Lógica da Convergência</h4>
            <p>
                Se a PETR4 está R$ 40,00 na B3, mas nosso modelo matemático diz que o "Preço Justo" (baseado em NY e Dólar) é R$ 40,50, existe uma <b>oportunidade de R$ 0,50 livre de risco direcional</b>.
                <br><br>
                Os robôs HFT compram o ativo "barato" e vendem o "caro", lucrando no fechamento do spread.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # =========================================
    # SEÇÃO 6: CONTEXTO MACRO (O Semáforo) - NOVO!
    # =========================================
    st.subheader("4. O 'Semáforo' Macro: Risk On / Risk Off")
    st.markdown("""
    Nenhum sinal técnico importa se o cenário macroeconômico for ignorado. Monitoramos o fluxo global de capital.
    """)

    c_macro1, c_macro2 = st.columns(2)
    with c_macro1:
        st.markdown("""
        <div class="tech-box" style="border-left: 4px solid #ef4444;">
            <h4>🔥 Cenário Risk-Off (Fuga de Capital)</h4>
            <p>
                Quando os <b>Juros Americanos (Treasuries 10Y)</b> sobem e o <b>Dólar Global (DXY)</b> se fortalece, o capital institucional sai de mercados emergentes (Brasil).
                <br><br>
                <span style="color:#ef4444; font-weight:bold;">Ação do Sistema:</span> Bloqueia sinais de compra em Bolsa, prioriza vendas e proteção em Dólar.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c_macro2:
        st.markdown("""
        <div class="tech-box" style="border-left: 4px solid #10b981;">
            <h4>🟢 Cenário Risk-On (Apetite a Risco)</h4>
            <p>
                Quando o Fed sinaliza corte de juros e o DXY cai, a liquidez global busca retorno em ativos de risco e commodities.
                <br><br>
                <span style="color:#10b981; font-weight:bold;">Ação do Sistema:</span> Libera sinais de compra em Beta alto (Small Caps, Tech) e Commodities.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#1e293b;'><br>", unsafe_allow_html=True)

    # =========================================
    # SEÇÃO 7: MÓDULO IA (NLP)
    # =========================================
    st.subheader("5. Intelligence AI: Processamento de Linguagem Natural")
    st.markdown("Nossa IA lê manchetes globais em milissegundos para medir o sentimento do mercado antes do humano.")
    
    c_ai1, c_ai2 = st.columns([1, 2])
    with c_ai1:
        st.markdown("""
        <div class="tech-box">
            <p style="font-size:0.9rem; color:#94a3b8; margin-bottom:5px;">BLOOMBERG TERMINAL • 10:01:45</p>
            <p style="color:#fff; font-weight:600;">"OPEC+ surprises market with deeper voluntary oil output cuts extending into Q3"</p>
            <div style="margin-top:10px;">
                <span style="background:#10b981; color:#0f172a; padding:3px 8px; font-size:0.75rem; font-weight:bold; border-radius:4px;">SENTIMENTO: BULLISH PETR4 (+8.2)</span>
            </div>
        </div>
        <div class="tech-box">
             <p style="font-size:0.9rem; color:#94a3b8; margin-bottom:5px;">REUTERS • 09:59:12</p>
            <p style="color:#fff; font-weight:600;">"China's manufacturing PMI contracts for third consecutive month, missing estimates"</p>
            <div style="margin-top:10px;">
                <span style="background:#ef4444; color:#fff; padding:3px 8px; font-size:0.75rem; font-weight:bold; border-radius:4px;">SENTIMENTO: BEARISH VALE3 (-6.5)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c_ai2:
        if anim_chart:
            st_lottie(anim_chart, height=300, key="ai_anim")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # =========================================
    # SEÇÃO 8: CTA FINAL
    # =========================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 60px; border-radius: 20px; text-align: center; border:1px solid #334155; box-shadow: 0 20px 40px -10px rgba(0,0,0,0.5);">
        <h2 style="color:white !important; font-size: 2.5rem;">Otimize sua Execução.</h2>
        <p style="color:#cbd5e1 !important; font-size: 1.2rem; max-width:700px; margin: 0 auto 30px auto;">
            Não opere contra as máquinas. Opere com a informação que elas usam.
            Acesse o terminal e visualize o fluxo institucional agora.
        </p>
    </div>
    <br><br><br>
    """, unsafe_allow_html=True)
