import streamlit as st
import modules.data_feed as data_feed # <--- Importando o novo motor
import requests

def load_lottie(url):
    # Função mantida caso queira voltar com animações futuras, 
    # mas o CSS puro é mais seguro para o Render.
    return None 

# --- VISUAL ---
def apply_css():
    st.markdown("""
    <style>
        .live-dot { height: 10px; width: 10px; background-color: #10b981; border-radius: 50%; display: inline-block; box-shadow: 0 0 5px #10b981; }
        .ticker-card { background: rgba(30, 41, 59, 0.6); padding: 15px; border-radius: 8px; border: 1px solid #334155; text-align: center; }
        .news-card { background: rgba(15, 23, 42, 0.8); border-left: 4px solid #334155; padding: 15px; margin-bottom: 15px; border-radius: 4px; transition: all 0.3s; }
        .news-card:hover { transform: translateX(5px); background: rgba(30, 41, 59, 0.9); }
    </style>
    """, unsafe_allow_html=True)

def show_landing_page():
    apply_css()

    # HERO
    st.markdown("""
    <div style="text-align: center; padding: 60px 0;">
        <h1 style="font-size: 3.5rem; color: #f8fafc;">INTELLIGENCE FLOW</h1>
        <p style="color: #60a5fa; font-weight: bold; letter-spacing: 2px;">DATA DRIVEN TRADING</p>
        <div style="font-size:0.8rem; color:#94a3b8; margin-top:10px;">
            <span class="live-dot"></span> CONEXÃO API: BRAPI (B3) • TWELVE (GLOBAL) • ALPHA (AI)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === TICKER HÍBRIDO (B3 + GLOBAL) ===
    # Busca dados (Se não tiver chave configurada, retorna None)
    b3_data = data_feed.get_b3_tickers()
    global_data = data_feed.get_global_tickers()

    cols = st.columns(4)
    col_idx = 0
    
    # Renderiza B3
    if b3_data:
        for symbol, (price, change) in b3_data.items():
            if col_idx < 4:
                color = "#10b981" if change >= 0 else "#ef4444"
                with cols[col_idx]:
                    st.markdown(f"""
                    <div class="ticker-card">
                        <div style="color:#94a3b8; font-size:0.8rem;">{symbol}</div>
                        <div style="color:#fff; font-weight:bold; font-size:1.2rem;">R$ {price:.2f}</div>
                        <div style="color:{color}; font-size:0.8rem;">{change:+.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                col_idx += 1
    
    # Renderiza Global (Se sobrar espaço)
    if global_data:
        for symbol, (price, change) in global_data.items():
            if col_idx < 4:
                with cols[col_idx]:
                    st.markdown(f"""
                    <div class="ticker-card">
                        <div style="color:#94a3b8; font-size:0.8rem;">{symbol}</div>
                        <div style="color:#fff; font-weight:bold; font-size:1.2rem;">{price:.2f}</div>
                        <div style="color:#64748b; font-size:0.8rem;">Global</div>
                    </div>
                    """, unsafe_allow_html=True)
                col_idx += 1

    if not b3_data and not global_data:
        st.warning("⚠️ Sistema em modo Offline. Configure as chaves de API em 'modules/data_feed.py' para ver cotações reais.")

    st.markdown("---")

    # === MÓDULO IA REAIS (ALPHA VANTAGE) ===
    st.subheader("🤖 Intelligence AI: Análise de Sentimento (Alpha Vantage)")
    
    ai_news = data_feed.get_ai_news_sentiment()
    
    if ai_news:
        for news in ai_news:
            st.markdown(f"""
            <div class="news-card" style="border-left-color: {news['color']};">
                <div style="display:flex; justify-content:space-between;">
                    <span style="font-size:0.8rem; color:#94a3b8;">FONTE: {news['source']}</span>
                    <span style="background:{news['color']}; color:white; padding:2px 8px; font-size:0.7rem; border-radius:4px; font-weight:bold;">{news['label']} (Score: {news['score']})</span>
                </div>
                <div style="color:white; font-weight:600; margin-top:5px;">{news['title']}</div>
                <div style="margin-top:5px;"><a href="{news['url']}" target="_blank" style="color:#60a5fa; font-size:0.8rem; text-decoration:none;">Ler notícia completa ↗</a></div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Fallback visual se não tiver API Key ainda
        st.info("Aguardando conexão com Alpha Vantage Neural Engine... (Adicione sua API Key)")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # === TEXTOS INSTITUCIONAIS (Mantidos para rolar a página) ===
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Hipótese dos Mercados Eficientes")
        st.markdown("Nossa IA processa as notícias acima para capturar ineficiências antes que o preço de tela reaja, explorando a latência cognitiva dos participantes humanos.")
    with c2:
        st.markdown("### Full Disclosure & Compliance")
        st.markdown("Todos os dados são obtidos via APIs públicas e oficiais (B3/Nasdaq), garantindo integridade e conformidade com as normas regulatórias.")
