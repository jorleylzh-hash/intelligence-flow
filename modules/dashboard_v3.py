import streamlit as st
import modules.data_feed as data_feed
import plotly.graph_objects as go

# --- FUNÇÃO VISUAL DE STATUS API ---
def render_api_status(name, status):
    """
    Status: 0=OFF (Vermelho), 1=CONECTANDO (Azul), 2=ON (Verde)
    """
    if status == 2:
        color = "#10b981" # Verde
        text = "CONECTADO"
        anim = "box-shadow: 0 0 10px #10b981;"
    elif status == 1:
        color = "#3b82f6" # Azul
        text = "NEGOCIANDO"
        anim = "animation: pulse 2s infinite;"
    else:
        color = "#ef4444" # Vermelho
        text = "OFFLINE"
        anim = ""
        
    st.markdown(f"""
    <div style="display:inline-block; background:{color}22; border:1px solid {color}; padding:5px 15px; border-radius:20px; margin-right:10px; {anim}">
        <span style="height:8px; width:8px; background-color:{color}; border-radius:50%; display:inline-block; margin-right:5px;"></span>
        <span style="color:{color}; font-weight:bold; font-size:0.75rem;">{name}: {text}</span>
    </div>
    """, unsafe_allow_html=True)

def show_landing_page():
    
    # === HERO SECTION ===
    st.markdown("""
    <div style="text-align: center; padding: 60px 0;">
        <h1 style="font-size: 3.5rem; letter-spacing: -2px; color: #fff;">INTELLIGENCE FLOW</h1>
        <p style="color: #94a3b8; font-size: 1.2rem;">ARBITRAGEM INSTITUCIONAL & ANÁLISE DE FLUXO</p>
    </div>
    """, unsafe_allow_html=True)

    # === STATUS DAS CONEXÕES (VERDE/AZUL/VERMELHO) ===
    st.markdown("<div style='text-align:center; margin-bottom:40px;'>", unsafe_allow_html=True)
    
    # Lógica simples para definir cor baseada se tem dados ou não
    b3_ok = 2 if data_feed.get_b3_tickers() else 0
    glob_ok = 2 if data_feed.get_global_tickers() else 0
    ai_ok = 1 # IA deixamos sempre azul (processando) ou verde se tiver chave
    
    c1, c2, c3 = st.columns(3)
    with c1: render_api_status("B3 FEED (BRAPI)", b3_ok)
    with c2: render_api_status("NYSE FEED (TWELVE)", glob_ok)
    with c3: render_api_status("NEURAL CORE (ALPHA)", ai_ok)
    
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ==================================================
    # 📚 CONTEÚDO EDUCACIONAL (PEDIDO DO USUÁRIO)
    # ==================================================

    # BLOCO 1: FUNDAMENTOS DO FLUXO
    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.markdown("### 1. Dinâmica do Preço & HME")
        st.markdown("""
        <div class="concept-card">
            <div class="concept-title">Hipótese dos Mercados Eficientes (HME)</div>
            A HME diz que o preço reflete tudo instantaneamente. Nós provamos o contrário.
            Entre a execução de uma ordem massiva em Nova York e o ajuste na B3, existe um <b>Gap Temporal</b>.
            É nesse milissegundo de ineficiência que nossa arbitragem atua.
        </div>
        <div class="concept-card">
            <div class="concept-title">Smart Money Concepts (SMC)</div>
            Não operamos suportes e resistências visuais. Operamos <b>Zonas de Liquidez</b>.
            Onde estão os Stops do varejo? É lá que o Institucional vai buscar liquidez para montar posição.
            Mapeamos Order Blocks e FVG (Fair Value Gaps).
        </div>
        """, unsafe_allow_html=True)

    with c_right:
        st.markdown("### 2. A Matemática da Arbitragem")
        st.markdown("""
        <div class="concept-card" style="border-left-color: #10b981;">
            <div class="concept-title">Spread B3 vs NYSE</div>
            Como um Market Maker vende R$ 5 Milhões de PETR4 sem derrubar o preço?
            <br><br>
            1. Ele vende <b>ADRs (PBR)</b> em Nova York ocultamente (Dark Pools).<br>
            2. Isso gera um deságio lá fora.<br>
            3. Robôs HFT detectam a distorção e vendem Brasil para fechar o Spread.
            <br><br>
            Nossa ferramenta monitora essa correlação em tempo real.
        </div>
        <div class="concept-card" style="border-left-color: #f59e0b;">
            <div class="concept-title">Market Making & Liquidez</div>
            O Market Maker não quer direção, ele quer <b>Volume</b>. 
            Se ele precisa vender 1 milhão de contratos, ele primeiro puxa o preço para cima (induzindo compra do varejo) 
            para ter liquidez de venda no topo. Isso é <b>Distribuição</b>.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # BLOCO 2: MACRO & OPÇÕES
    st.subheader("3. Visão Macro e Derivativos")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("""
        <div class="concept-card">
            <div class="concept-title">Gamma Exposure (Opções)</div>
            O mercado de Opções move o mercado à vista. Quando há muito Gamma Positivo, 
            os Market Makers operam contra a tendência para fazer hedge, travando o preço.
            Em Gamma Negativo, a volatilidade explode.
        </div>
        """, unsafe_allow_html=True)
        
    with col_b:
        st.markdown("""
        <div class="concept-card">
            <div class="concept-title">Corelação de Ativos</div>
            O IBOV não anda sozinho. Ele é escravo do:
            <ul>
                <li><b>EEM:</b> ETF de Emergentes</li>
                <li><b>DXY:</b> Força do Dólar Global</li>
                <li><b>Treasuries 10Y:</b> Juros Americanos</li>
            </ul>
            Se o Juro sobe lá, o dinheiro sai daqui.
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown("""
        <div class="concept-card">
            <div class="concept-title">Agenda Econômica (Drivers)</div>
            Ignorar o calendário é suicídio.
            <ul>
                <li><b>Payroll:</b> Define o juro nos EUA.</li>
                <li><b>COPOM:</b> Define o juro no Brasil.</li>
                <li><b>Triple Witching:</b> Vencimento triplo de opções.</li>
            </ul>
            O sistema alerta alta volatilidade nesses dias.
        </div>
        """, unsafe_allow_html=True)

    # === MÓDULO IA (NOTÍCIAS) ===
    st.markdown("---")
    st.subheader("🤖 Neural Core: Análise de Notícias")
    
    news = data_feed.get_ai_news_sentiment()
    if news:
        for item in news:
            st.markdown(f"""
            <div style="background:#1e293b; padding:15px; margin-bottom:10px; border-left:4px solid {item['color']}; border-radius:4px;">
                <div style="font-size:0.8rem; color:#94a3b8;">{item['source']} • SENTIMENTO: <span style="color:{item['color']}">{item['label']}</span></div>
                <div style="color:white; font-weight:bold;">{item['title']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aguardando conexão Neural (Configure a chave Alpha Vantage em data_feed.py)...")
