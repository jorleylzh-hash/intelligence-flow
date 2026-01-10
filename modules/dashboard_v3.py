import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_lottie import st_lottie
import requests

# --- ASSETS ---
def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# --- CONTEÚDO EDUCACIONAL PROFUNDO ---
def show_landing_page():
    # Animações Conceituais
    anim_network = load_lottie("https://assets5.lottiefiles.com/packages/lf20_w51pcehl.json")
    anim_ai = load_lottie("https://lottie.host/embed/9a6d0c7d-8b3e-4d4e-9f3e-8b3e4d4e9f3e/simulated.json") # Placeholder genérico

    # 1. HERO: A PROPOSTA DE VALOR
    st.markdown("""
    <div style="text-align: center; padding: 60px 0;">
        <h1 style="font-size: 4rem; letter-spacing: -2px; margin-bottom: 10px; background: -webkit-linear-gradient(45deg, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            INTELLIGENCE FLOW
        </h1>
        <p style="font-size: 1.4rem; color: #94a3b8; max-width: 800px; margin: 0 auto;">
            Ecossistema Institucional de Arbitragem, Macroeconomia e Inteligência Artificial.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. FUNDAMENTAÇÃO TEÓRICA (LONG SCROLL)
    
    # === BLOCO A: Hipótese dos Mercados Eficientes (HME) vs Realidade ===
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("1. HME e a Ineficiência do Preço")
        st.markdown("""
        A **Hipótese dos Mercados Eficientes (Fama, 1970)** sugere que o preço reflete todas as informações. 
        Nós discordamos. Em timeframes curtos (M5), o mercado é **Ineficiente e Emocional**.
        <br><br>
        A Intelligence Flow explora essa falha. Enquanto o varejo reage à notícia atrasada, nossos algoritmos capturam o fluxo antes que a informação seja precificada no gráfico.
        """, unsafe_allow_html=True)
    with c2:
        st.info("💡 **Tese:** O preço não é a verdade. O Fluxo (Volume + Agressão) é a verdade. O preço é apenas a sombra do fluxo.")

    st.markdown("<br>", unsafe_allow_html=True)

    # === BLOCO B: Full and Fair Disclosure & Price Action ===
    st.subheader("2. Full Disclosure & Price Action Institucional")
    st.markdown("""
    Pelo princípio do *Full and Fair Disclosure*, a informação deve ser pública. Mas a **velocidade** de acesso não é igual.
    <br><br>
    O Price Action clássico ensina suporte e resistência. O **Price Action Institucional** monitora onde a liquidez está repousando.
    Utilizamos o conceito de que o preço busca liquidez (Stop Hunts) antes de tomar direção.
    """, unsafe_allow_html=True)

    st.markdown("---")

    # === BLOCO C: MEMORIAL DE CÁLCULO (ARBITRAGEM) ===
    st.subheader("3. Memorial de Cálculo: A Matemática da Arbitragem")
    st.markdown("Como nossos robôs encontram dinheiro onde ninguém vê?")
    
    col_math, col_desc = st.columns([1, 1.5])
    
    with col_math:
        st.markdown("""
        <div class="math-box">
        <b>Fórmula da Paridade Teórica:</b><br><br>
        $$P_{Justo} = (P_{NY} \\times FX_{Dolar}) + Spread$$
        <br><br>
        <b>Onde:</b><br>
        $P_{NY}$ = Preço do ADR (EUA)<br>
        $FX$ = Taxa de Câmbio (Dólar Futuro)<br>
        $Spread$ = Custo de Carry + Risco Brasil
        </div>
        """, unsafe_allow_html=True)
        
    with col_desc:
        st.markdown("""
        Se o preço de tela da **Petrobras (PETR4)** no Brasil é **R$ 35,00**, mas o nosso cálculo aponta que, convertido de Nova York, ela deveria custar **R$ 35,20**:
        <br><br>
        1. Existe um **GAP de R$ 0,20**.
        2. O robô HFT compra no Brasil (Barato).
        3. Vende o Futuro Sintético.
        4. Lucra a diferença na convergência (Fechamento do Gap).
        """)

    st.markdown("---")

    # === BLOCO D: SMART MONEY CONCEPTS (SMC) ===
    st.subheader("4. SMC: Rastreando o 'Dinheiro Esperto'")
    st.markdown("""
    O Smart Money (Bancos Centrais, Hedge Funds) deixa pegadas. Não operamos rompimentos de linha de tendência. Operamos:
    * **Order Blocks:** Zonas onde grandes ordens institucionais ficaram pendentes.
    * **Imbalance (FVG):** Vazios de liquidez que o preço precisa preencher.
    * **Liquidity Grabs:** Quando o mercado rompe um topo apenas para estopar o varejo e cair.
    """)
    
    st.markdown("---")

    # === BLOCO E: MÓDULO IA & NOTÍCIAS (NOVIDADE) ===
    st.subheader("5. Módulo Intelligence AI 🤖")
    st.markdown("Nossa IA processa manchetes globais e atribui um 'Score de Impacto' em milissegundos.")
    
    # Simulação de Dashboard de IA
    st.markdown("#### 📡 Feed de Notícias em Tempo Real (Processado por NLP)")
    
    c_news1, c_news2, c_news3 = st.columns(3)
    
    with c_news1:
        st.markdown("""
        <div style="border:1px solid #334155; padding:15px; border-radius:10px; background:rgba(0,0,0,0.2);">
            <div style="font-size:0.8rem; color:#94a3b8;">10:04:12 • REUTERS</div>
            <div style="color:white; font-weight:bold;">Fed Chairman Powell hints at rate cut in Q3</div>
            <br>
            <span style="background:#16a34a; color:white; padding:2px 8px; font-size:0.8rem;">BULLISH USD</span>
            <span style="color:#16a34a; float:right;">Score: +8.4</span>
        </div>
        """, unsafe_allow_html=True)

    with c_news2:
        st.markdown("""
        <div style="border:1px solid #334155; padding:15px; border-radius:10px; background:rgba(0,0,0,0.2);">
            <div style="font-size:0.8rem; color:#94a3b8;">10:02:45 • BLOOMBERG</div>
            <div style="color:white; font-weight:bold;">Iron Ore futures drop 2% in Dalian Exchange</div>
            <br>
            <span style="background:#dc2626; color:white; padding:2px 8px; font-size:0.8rem;">BEARISH VALE3</span>
            <span style="color:#dc2626; float:right;">Score: -6.1</span>
        </div>
        """, unsafe_allow_html=True)
        
    with c_news3:
        st.markdown("""
        <div style="border:1px solid #334155; padding:15px; border-radius:10px; background:rgba(0,0,0,0.2);">
            <div style="font-size:0.8rem; color:#94a3b8;">09:55:10 • ESTADÃO</div>
            <div style="color:white; font-weight:bold;">Ministério da Fazenda anuncia nova meta fiscal</div>
            <br>
            <span style="background:#f59e0b; color:black; padding:2px 8px; font-size:0.8rem;">VOLATILITY</span>
            <span style="color:#f59e0b; float:right;">Score: 5.0</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br><br>", unsafe_allow_html=True)
