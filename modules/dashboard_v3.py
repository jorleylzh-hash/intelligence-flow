import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# --- 1. CONFIGURAÇÃO VISUAL (BANK GRADE UI) ---
def apply_bank_grade_css():
    st.markdown("""
    <style>
        /* Fundo Geral - Cinza Gelo (Profissional e Leve) */
        .stApp { background-color: #f0f2f6; }
        
        /* Tipografia */
        h1, h2, h3 { 
            color: #0f172a; /* Azul Quase Preto */
            font-family: 'Segoe UI', Helvetica, sans-serif;
            font-weight: 600;
        }
        
        /* Cards (Widgets) - Estilo Bancário */
        .bank-card {
            background-color: #ffffff;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border-top: 4px solid #0047AB; /* Azul Cobalto (Confiança) */
            margin-bottom: 20px;
            transition: transform 0.2s;
        }
        .bank-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }

        /* Métricas */
        .metric-label { font-size: 0.85rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }
        .metric-value { font-size: 1.8rem; color: #0f172a; font-weight: 700; }
        .metric-delta-pos { color: #059669; font-weight: 600; font-size: 0.9rem; background: #ecfdf5; padding: 2px 8px; border-radius: 4px; }
        .metric-delta-neg { color: #dc2626; font-weight: 600; font-size: 0.9rem; background: #fef2f2; padding: 2px 8px; border-radius: 4px; }

        /* Cabeçalho Institucional */
        .hero-header {
            background: linear-gradient(135deg, #003366 0%, #0047AB 100%);
            padding: 40px;
            border-radius: 0 0 20px 20px;
            color: white;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,51,102,0.2);
        }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DADOS DE MERCADO ---
@st.cache_data(ttl=300)
def get_market_data():
    tickers = {
        'S&P 500': '^GSPC', 
        'Dólar (DXY)': 'DX-Y.NYB', 
        'Treasuries 10Y': '^TNX', 
        'Petróleo Brent': 'BZ=F'
    }
    try:
        data = yf.download(list(tickers.values()), period="5d", interval="1d", progress=False)['Close']
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.droplevel(1)
        
        results = {}
        charts = {}
        for name, ticker in tickers.items():
            if ticker in data.columns:
                series = data[ticker].dropna()
                curr = series.iloc[-1]
                prev = series.iloc[-2]
                change = ((curr - prev) / prev) * 100
                results[name] = (curr, change)
                charts[name] = series
            else:
                results[name] = (0.0, 0.0)
                charts[name] = []
        return results, charts
    except:
        return None, None

def plot_mini_chart(series, color_line):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=series, mode='lines', 
        line=dict(color=color_line, width=2),
        fill='tozeroy', fillcolor=f"rgba{color_line[3:-1]}, 0.1)" # Truque para cor transparente
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), height=60,
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    return fig

# --- 3. PÁGINA PRINCIPAL ---
def show_landing_page():
    apply_bank_grade_css()

    # HERO SECTION (Institucional e Seguro)
    st.markdown("""
    <div class="hero-header">
        <h1 style="color:white; margin:0;">INTELLIGENCE FLOW</h1>
        <p style="color:#e2e8f0; font-size:1.1rem; margin-top:10px;">
            Soluções de Inteligência Financeira e Arbitragem Quantitativa.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # VISÃO GERAL DE MERCADO (Mais informativo)
    st.markdown("### 📊 Panorama Global")
    st.markdown("Monitoramento em tempo real dos principais drivers de liquidez mundial.")
    
    data, charts = get_market_data()
    
    if data:
        cols = st.columns(4)
        keys = list(data.keys())
        
        for i, col in enumerate(cols):
            name = keys[i]
            val, chg = data[name]
            series = charts[name]
            color = "#059669" if chg >= 0 else "#dc2626" # Verde ou Vermelho Institucional
            
            with col:
                st.markdown(f"""
                <div class="bank-card" style="padding: 15px; margin-bottom:10px;">
                    <div class="metric-label">{name}</div>
                    <div style="display:flex; justify-content:space-between; align-items:baseline;">
                        <div class="metric-value">{val:.2f}</div>
                        <div class="{ 'metric-delta-pos' if chg >=0 else 'metric-delta-neg' }">{chg:+.2f}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                # Gráfico Limpo abaixo do card
                if len(series) > 0:
                    st.plotly_chart(plot_mini_chart(series, color), use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # ÁREA EXPLICATIVA (Abas para organizar informação sem poluir)
    st.markdown("### 💠 Nossa Metodologia")
    
    tab1, tab2, tab3 = st.tabs(["Fluxo Macro", "Arbitragem HFT", "Segurança"])
    
    with tab1:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("""
            <div class="bank-card">
                <h3>Correlação B3 vs NYSE</h3>
                <p style="color:#475569;">
                    Utilizamos algoritmos proprietários para rastrear o fluxo de capital estrangeiro. 
                    Monitoramos o spread entre o <b>EWZ (Brasil ETF)</b> e o IBOVESPA Futuro para antecipar tendências de curto prazo.
                    <br><br>
                    Nosso modelo identifica quando o mercado local diverge injustificadamente do cenário global (DXY e Treasuries).
                </p>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.info("ℹ️ **Sabia?** 60% do volume da B3 é capital estrangeiro. Quem não olha para fora, opera cego.")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="bank-card">
                <h3>Oportunidade de Arbitragem</h3>
                <p style="color:#475569;">
                    Ativos espelhados (ADRs) devem ter paridade matemática. 
                    Detectamos <b>Gaps de Preço</b> na casa dos milissegundos entre PETR4 (Brasil) e PBR (EUA).
                </p>
            </div>
            """, unsafe_allow_html=True)
        with c2:
             st.markdown("""
            <div class="bank-card">
                <h3>Execução de Alta Performance</h3>
                <p style="color:#475569;">
                    Nossa "Área do Trader" oferece visualização de baixa latência para captura desses spreads, 
                    com filtros de agressão e fluxo de ordens.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="bank-card" style="border-top-color: #059669;">
            <h3>Protocolos de Segurança</h3>
            <ul>
                <li style="color:#475569;">Dados criptografados ponta-a-ponta.</li>
                <li style="color:#475569;">Conexão via WebSocket seguro (WSS).</li>
                <li style="color:#475569;">Infraestrutura em nuvem com redundância.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # CTA (Chamada para Ação)
    st.markdown("<br>", unsafe_allow_html=True)
    c_cta1, c_cta2, c_cta3 = st.columns([1, 2, 1])
    with c_cta2:
        st.markdown("""
        <div style="text-align: center; background-color: #e0e7ff; padding: 30px; border-radius: 12px; border: 1px solid #c7d2fe;">
            <h3 style="color: #3730a3;">Acesso Institucional</h3>
            <p style="color: #4338ca;">Acesse a <b>Área do Trader</b> no menu lateral para visualizar os sinais em tempo real.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><div style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Intelligence Flow Solutions © 2026 • Termos de Uso • Privacidade</div>", unsafe_allow_html=True)
