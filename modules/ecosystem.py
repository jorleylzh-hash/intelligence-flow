import streamlit as st

def show_ecosystem():
    st.markdown("## 💠 O Ecossistema Intelligence Flow")
    st.markdown("Integração de dados massivos, matemática financeira e comportamento institucional.")
    
    st.markdown("---")

    # 1. MEMORIAL DE CÁLCULO
    st.subheader("1. Memorial de Cálculo (Algoritmo de Paridade)")
    st.markdown("Nossa vantagem competitiva reside na identificação matemática de distorções de preço.")
    
    col_math, col_desc = st.columns([1, 1])
    
    with col_math:
        st.markdown("""
        <div class="math-block">
        <b>FÓRMULA MESTRA DE ARBITRAGEM (ADR):</b><br><br>
        $$ P_{Fair} = (P_{ADR} \\times FX_{Fut}) + Spread_{Risco} $$
        <br><br>
        <b>CÁLCULO DO GAP (%):</b><br><br>
        $$ Gap_{\\%} = \\left( \\frac{P_{B3} - P_{Fair}}{P_{B3}} \\right) \\times 100 $$
        </div>
        """, unsafe_allow_html=True)
        
    with col_desc:
        st.markdown("""
        <div class="tech-card">
            <b>Legenda das Variáveis:</b><br>
            <ul>
                <li><b>P(ADR):</b> Preço da ação em Nova York (ex: PBR).</li>
                <li><b>FX(Fut):</b> Dólar Futuro ajustado pelos Juros (Cupom Cambial).</li>
                <li><b>Spread(Risco):</b> Custo de oportunidade e Risco Brasil (CDS).</li>
            </ul>
            <br>
            Se o Gap for maior que <b>0.5%</b> (descontadas as taxas), o robô executa a arbitragem.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. CONCEITOS INTEGRADOS
    st.subheader("2. Metodologia Integrada")
    
    # Abas para organizar muito conteúdo
    tab1, tab2, tab3, tab4 = st.tabs(["SMC & HME", "Price Action", "Market Makers", "Opções & Macro"])
    
    with tab1:
        st.markdown("#### Hipótese dos Mercados Eficientes (HME) vs Realidade")
        st.info("A HME afirma que é impossível bater o mercado pois ele é eficiente. Nós provamos que o mercado é eficiente no LONGO prazo, mas ineficiente no CURTO prazo (M5/H1).")
        st.markdown("#### Smart Money Concepts (SMC)")
        st.write("Não operamos linhas de tendência. Operamos onde o dinheiro institucional está 'preso'. Caçamos zonas de Stop Hunt e Order Blocks.")

    with tab2:
        st.markdown("#### Price Action Institucional")
        st.write("A leitura pura do candle, ignorando indicadores atrasados (RSI, MACD). O foco é Volume e Spread do Candle (VSA - Volume Spread Analysis).")

    with tab3:
        st.markdown("#### A Lógica do Market Maker")
        st.write("O Market Maker precisa de liquidez. Para vender 1 milhão de lotes, ele precisa que 1 milhão de varejistas queiram comprar. Por isso ele 'puxa' o preço para induzir euforia antes de desovar sua posição (Distribuição).")

    with tab4:
        st.markdown("#### Opções (Greeks)")
        st.write("O mercado de derivativos é a cauda que balança o cachorro. O posicionamento em Gamma dos Dealers dita a volatilidade do ativo à vista.")
        st.markdown("#### Macroeconomia")
        st.write("Monitoramos Payroll, CPI, Fomc e Copom. O dinheiro respeita a taxa de juros.")
