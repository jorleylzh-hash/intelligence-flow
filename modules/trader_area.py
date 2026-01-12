import streamlit as st
import time
import plotly.graph_objects as go
from modules import data_feed

ATIVOS_PADRAO = ["WDO$N", "WIN$N", "PETR4", "VALE3"]

def render_trader_area():
    st.markdown("## ⚡ Intelligence Flow | Live")

    st.sidebar.markdown("### Status da Rede")
    st.sidebar.info("🔗 Sincronização Automática Ativa")

    ativo_atual = st.selectbox("Ativo Operacional", ATIVOS_PADRAO)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Cotação")
        metric_placeholder = st.empty()
    with col2:
        chart_placeholder = st.empty()

    while True:
        dados_dict = data_feed.get_data_hibrido([ativo_atual])
        dado = dados_dict.get(ativo_atual)

        if dado and dado['preco'] > 0:
            metric_placeholder.metric(label=ativo_atual, value=f"{dado['preco']:.2f}")
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = dado['preco'],
                gauge = {
                    'axis': {'range': [dado['bid']-5, dado['ask']+5]}, 
                    'bar': {'color': "#66fcf1"}
                }
            ))
            fig.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20))
            
            # --- A CORREÇÃO ESTÁ AQUI EMBAIXO ---
            # Adicionamos key=f"{time.time()}" para garantir que cada gráfico seja único
            chart_placeholder.plotly_chart(
                fig, 
                use_container_width=True, 
                key=f"chart_{time.time()}"
            )
            
        else:
            metric_placeholder.warning("Sincronizando...")
            
        time.sleep(1)
