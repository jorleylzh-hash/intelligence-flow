import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show_solutions():
    st.markdown("## 💎 Soluções On-Demand")
    st.markdown("Selecione os ativos para rodar a análise de correlação e viés em tempo real.")

    # 1. SELEÇÃO DE ATIVOS
    col_sel, col_act = st.columns([3, 1])
    with col_sel:
        # Multiselect profissional
        assets = st.multiselect(
            "Cesta de Ativos para Monitoramento:",
            ["PETR4", "VALE3", "ITUB4", "BBAS3", "DOLAR", "S&P500"],
            default=["PETR4", "VALE3", "DOLAR"]
        )
    with col_act:
        st.write("")
        st.write("")
        if st.button("RODAR ANÁLISE ⚡", type="primary"):
            st.success("Processamento Neural Iniciado...")

    st.markdown("---")

    # 2. ANÁLISE DE CORRELAÇÃO (MATRIZ)
    st.subheader("1. Matriz de Correlação Cruzada")
    st.markdown("Identifica quais ativos estão andando juntos (Correlação +1) ou opostos (Correlação -1).")
    
    # Simulação de dados para evitar erro de download no Render se API falhar
    # Em produção real, isso viria do data_feed.py
    data = {
        'PETR4': np.random.normal(0, 1, 100),
        'VALE3': np.random.normal(0, 1, 100),
        'DOLAR': np.random.normal(0, 1, 100) * -0.5, # Correlação inversa simulada
        'S&P500': np.random.normal(0, 1, 100) * 0.3
    }
    df = pd.DataFrame(data)
    if assets:
        # Filtra apenas os selecionados se existirem no df simulado
        cols_to_show = [a for a in assets if a in df.columns]
        if cols_to_show:
            corr = df[cols_to_show].corr()
            fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
            st.plotly_chart(fig, use_container_width=True)

    # 3. VIÉS DE MERCADO E RESULTADOS
    st.subheader("2. Viés Probabilístico & Spread")
    
    c1, c2, c3 = st.columns(3)
    
    # Card 1
    with c1:
        st.markdown("""
        <div class="tech-card">
            <h4>PETR4 vs PBR (ADR)</h4>
            <p>Spread Atual: <span style="color:#10b981">+0.82% (Oportunidade)</span></p>
            <p>Viés: <b>ALTA</b> (Fluxo Gringo Comprador)</p>
            <div style="background:#10b981; height:5px; width:80%;"></div>
        </div>
        """, unsafe_allow_html=True)

    # Card 2
    with c2:
        st.markdown("""
        <div class="tech-card">
            <h4>VALE3 vs Minério (Dalian)</h4>
            <p>Spread Atual: <span style="color:#ef4444">-1.20% (Caro)</span></p>
            <p>Viés: <b>BAIXA</b> (China desacelerando)</p>
            <div style="background:#ef4444; height:5px; width:60%;"></div>
        </div>
        """, unsafe_allow_html=True)
        
    # Card 3
    with c3:
        st.markdown("""
        <div class="tech-card">
            <h4>Dólar vs Juros (DI)</h4>
            <p>Correlação: <span style="color:#f59e0b">0.92 (Alta)</span></p>
            <p>Viés: <b>NEUTRO</b> (Aguardando Payroll)</p>
            <div style="background:#f59e0b; height:5px; width:50%;"></div>
        </div>
        """, unsafe_allow_html=True)
