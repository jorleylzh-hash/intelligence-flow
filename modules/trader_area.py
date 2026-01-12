import streamlit as st
import time
import plotly.graph_objects as go
from modules import data_feed

# Lista de ativos (pode ajustar conforme seus contratos)
ATIVOS_PADRAO = ["WDO$N", "WIN$N", "PETR4", "VALE3"]

def render_trader_area():
    st.markdown("## ⚡ Intelligence Flow | Nuvem Conectada")

    # --- CONFIGURAÇÃO DA PONTE (SIDEBAR) ---
    st.sidebar.header("📡 Conexão Remota")
    
    # O CAMPO MÁGICO ONDE VOCÊ COLA O LINK
    url_ngrok = st.sidebar.text_input(
        "Link do Ngrok (Ponte):", 
        placeholder="https://...ngrok-free.dev",
        help="https://unlisted-bailee-biyearly.ngrok-free.dev"
    )

    if url_ngrok:
        st.sidebar.success("Conectado à Ponte! 🟢")
    else:
        st.sidebar.warning("Cole o link para ver dados reais.")

    st.markdown("---")

    # --- SELEÇÃO DO ATIVO ---
    ativo_atual = st.selectbox("Ativo Operacional", ATIVOS_PADRAO)

    # --- LAYOUT VISUAL ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Cotação")
        metric_placeholder = st.empty()
        spread_placeholder = st.empty()

    with col2:
        st.markdown("### Gráfico Intraday")
        chart_placeholder = st.empty()

    # --- LOOP DE DADOS ---
    while True:
        # Busca dados passando a URL que você digitou
        dados_dict = data_feed.get_data_hibrido([ativo_atual], url_ponte=url_ngrok)
        dado = dados_dict.get(ativo_atual)

        if dado and dado['preco'] > 0:
            # 1. Atualiza Preço
            metric_placeholder.metric(
                label=f"{ativo_atual}",
                value=f"{dado['preco']:.2f}",
                delta=f"Vol: {dado.get('volume',0)}"
            )
            
            # 2. Atualiza Spread/Origem
            cor_spread = "green" if dado['spread'] <= 1.0 else "red"
            spread_placeholder.markdown(
                f"""
                **Fonte:** {dado['origem']}  
                **Spread:** :{cor_spread}[{dado['spread']:.1f} pts]  
                Bid: {dado['bid']} | Ask: {dado['ask']}
                """
            )

            # 3. Atualiza Gráfico
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = dado['preco'],
                title = {'text': "Fluxo Real Time"},
                gauge = {
                    'axis': {'range': [dado['bid']-5, dado['ask']+5]},
                    'bar': {'color': "#66fcf1"},
                    'bgcolor': "#0e1117"
                }
            ))
            fig.update_layout(height=250, margin=dict(t=30, b=20, l=20, r=20), paper_bgcolor="#0e1117", font={'color': "white"})
            chart_placeholder.plotly_chart(fig, use_container_width=True)

        else:
            metric_placeholder.error("Sem sinal...")
            spread_placeholder.info("Verifique se o Link está correto e o MT5 aberto.")

        time.sleep(1)
