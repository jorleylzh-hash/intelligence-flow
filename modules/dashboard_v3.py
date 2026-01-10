import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# --- CONFIGURAÇÃO DE CACHE E DADOS (PERFORMANCE) ---
@st.cache_data(ttl=60, show_spinner=False)
def get_market_data():
    # Lista de Ativos Monitorados (Macro + Brasil)
    tickers = {
        'IBOV': '^BVSP', 'DÓLAR': 'BRL=X', 'S&P500': '^GSPC', 
        'DXY': 'DX-Y.NYB', 'TREASURIES 10Y': '^TNX', 
        'PETRÓLEO BRENT': 'BZ=F', 'MINÉRIO (VALE)': 'VALE',
        'PETR4': 'PETR4.SA', 'VALE3': 'VALE3.SA', 'EWZ': 'EWZ'
    }
    
    txt_tickers = " ".join(list(tickers.values()))
    try:
        data = yf.download(txt_tickers, period="2d", interval="1d", progress=False)['Close']
        
        # Tratamento para multi-index do yfinance novo
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)
            
        results = {}
        for name, ticker in tickers.items():
            if ticker in data.columns:
                curr = data[ticker].iloc[-1]
                prev = data[ticker].iloc[-2] if len(data) > 1 else curr
                change = ((curr - prev) / prev) * 100
                results[name] = {'price': curr, 'change': change}
            else:
                results[name] = {'price': 0.0, 'change': 0.0}
        return results
    except Exception as e:
        return None

# --- CSS PROFISSIONAL (O VISUAL "FANTASTIC") ---
def apply_corporate_styles():
    st.markdown("""
    <style>
        /* Fundo e Tipografia */
        .stApp { background-color: #0e1117; }
        h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 600; letter-spacing: -0.5px; }
        
        /* Hero Section */
        .hero-container {
            padding: 40px 20px;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-radius: 12px;
            border-left: 5px solid #3b82f6;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        }
        .hero-title { font-size: 32px; color: #f8fafc; margin-bottom: 10px; }
        .hero-subtitle { font-size: 16px; color: #94a3b8; max-width: 800px; line-height: 1.6; }

        /* Cards de Conceito (Grid) */
        .concept-card {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #334155;
            height: 100%;
            transition: transform 0.2s;
        }
        .concept-card:hover { border-color: #3b82f6; transform: translateY(-3px); }
        .card-header { color: #60a5fa; font-size: 14px; font-weight: bold; text-transform: uppercase; margin-bottom: 8px; }
        .card-body { color: #cbd5e1; font-size: 13px; line-height: 1.5; }
        
        /* Métricas de Arbitragem */
        .arb-metric { font-size: 24px; font-weight: bold; color: #fff; }
        .arb-label { font-size: 12px; color: #94a3b8; }
        .positive { color: #10b981; }
        .negative { color: #ef4444; }
        
        /* Divisores */
        hr { border-color: #334155; }
    </style>
    """, unsafe_allow_html=True)

# --- CONTEÚDO DA PÁGINA ---
def show_dashboard():
    apply_corporate_styles()
    
    # 1. HEADER INSTITUCIONAL
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">🌪️ INTELLIGENCE FLOW <span style="font-size:18px; color:#3b82f6; vertical-align:middle;">PLATFORM</span></div>
        <div class="hero-subtitle">
            Sistema proprietário de análise quantitativa e macroeconômica. 
            Monitoramento em tempo real da correlação entre <b>B3 (Brasil)</b> e <b>NYSE (EUA)</b>, 
            identificando assimetrias de preço através de paridade, fluxo cambial e drivers globais.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. DADOS AO VIVO (TICKER TAPE)
    data = get_market_data()
    if data:
        cols = st.columns(6)
        metrics = [
            ("S&P 500", data['S&P500']), ("DXY (Dólar Global)", data['DXY']), 
            ("US 10Y (Juros)", data['TREASURIES 10Y']), ("BRENT (Oil)", data['PETRÓLEO BRENT']),
            ("EWZ (Brasil ETF)", data['EWZ']), ("USD/BRL", data['DÓLAR'])
        ]
        
        for col, (label, val) in zip(cols, metrics):
            color = "normal" # O Streamlit colore sozinho baseado no delta
            col.metric(label, f"{val['price']:.2f}", f"{val['change']:.2f}%")
    
    st.divider()

    # 3. PAINEL EDUCACIONAL E ESTRATÉGICO
    st.subheader("📚 METODOLOGIA & FUNDAMENTOS OPERACIONAIS")
    
    tab1, tab2, tab3 = st.tabs(["🌎 MACRO ECONOMIA", "⚡ ARBITRAGEM & GAP", "🔄 CORRELAÇÕES"])

    with tab1:
        st.markdown("#### OS 10 PILARES DO MONITORAMENTO")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="concept-card">
                <div class="card-header">🇺🇸 O MERCADO AMERICANO (DRIVER)</div>
                <div class="card-body">
                    • <b>S&P500 & DOW JONES:</b> Indicam o apetite global a risco. Se eles caem, o mundo vende Brasil.<br>
                    • <b>TREASURIES 10Y:</b> A taxa livre de risco. Se o juro sobe nos EUA, o dinheiro sai de emergentes (Brasil) e volta para o Dólar.<br>
                    • <b>DXY:</b> A força do Dólar contra moedas fortes. DXY forte = Commodities fracas.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="concept-card">
                <div class="card-header">🇨🇳 COMMODITIES & BRASIL (REFLEXO)</div>
                <div class="card-body">
                    • <b>MINÉRIO (CHINA):</b> Move a VALE3. A Vale compõe grande parte do IBOV.<br>
                    • <b>PETRÓLEO BRENT:</b> Move a PETR4. Petrobras e Vale juntas ditam o rumo do índice.<br>
                    • <b>EWZ:</b> O ETF do Brasil em NY. É como os "gringos" veem o Brasil. Muitas vezes antecipa o movimento do IBOV em minutos.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("#### 🤖 A MATEMÁTICA DA ARBITRAGEM")
        col_text, col_math = st.columns([3, 2])
        
        with col_text:
            st.markdown("""
            **O que é Arbitragem de Alta Frequência?**
            
            Ativos como **Petrobras (PETR4)** e **Vale (VALE3)** são negociados simultaneamente no Brasil e em Nova York (ADRs).
            O preço não pode ser diferente nos dois lugares. Se houver diferença, robôs (HFTs) compram onde está barato e vendem onde está caro.
            
            **O Conceito de GAP:**
            Quando o preço teórico (Paridade) está acima do preço de tela, temos um GAP DE COMPRA. O mercado tende a fechar essa conta.
            """)
        
        with col_math:
            if data:
                # Cálculo da Paridade em Tempo Real
                petr_ny = 14.50 # Valor simulado se a API falhar ou PBR
                usd = data['DÓLAR']['price']
                petr_br = data['PETR4']['price']
                
                # Fórmula: (Preço NY * Dólar) = Preço Justo BR
                # Obs: PBR = 2 ações PETR4. Ajuste conforme necessário.
                # Aqui simplificado para didática: Supondo PBR representando paridade 1:1 ajustada
                
                fair_price = (petr_ny * usd) # Exemplo didático
                gap = ((fair_price / petr_br) - 1) * 100
                
                st.markdown(f"""
                <div class="concept-card" style="text-align: center;">
                    <div class="card-header">SIMULAÇÃO DE PARIDADE (Exemplo)</div>
                    <div class="arb-metric">R$ {fair_price:.2f}</div>
                    <div class="arb-label">Preço Justo Teórico</div>
                    <hr>
                    <div class="card-header">GAP ATUAL</div>
                    <div class="arb-metric {'positive' if gap > 0 else 'negative'}">{gap:.2f}%</div>
                    <div class="arb-label">{'Oportunidade de COMPRA' if gap > 0 else 'Oportunidade de VENDA'}</div>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        st.markdown("#### ⚖️ CORRELAÇÕES: O JOGO DOS PESOS")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.image("https://images.unsplash.com/photo-1611974765270-ca1258634369?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
            st.markdown("**CORRELAÇÃO POSITIVA (+)**")
            st.caption("Quando S&P500 sobe, IBOV tende a subir. Quando Commodities sobem, PETR4/VALE3 sobem.")
        
        with c2:
            st.image("https://images.unsplash.com/photo-1580519542036-c47de6196ba5?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
            st.markdown("**CORRELAÇÃO NEGATIVA (-)**")
            st.caption("Quando o Dólar (DXY) sobe no mundo, as bolsas emergentes caem. Dólar x Bolsa é uma gangorra.")
        
        with c3:
            st.image("https://images.unsplash.com/photo-1642543492481-44e81e3914a7?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
            st.markdown("**B3 vs NYSE**")
            st.caption("Quem manda? Pelo volume financeiro, NY costuma ditar a tendência. O Brasil segue o fluxo estrangeiro.")

    st.divider()
    
    # 4. FOOTER
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 12px; margin-top: 50px;">
        © 2026 INTELLIGENCE FLOW SOLUTIONS. Todos os dados possuem delay de 15 minutos (Free Tier).<br>
        Esta ferramenta é para fins educacionais e de análise de fluxo, não constituindo recomendação de investimento (CVM/SEC).
    </div>
    """, unsafe_allow_html=True)
