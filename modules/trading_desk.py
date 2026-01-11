import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

def show_desk():
    # Cabeçalho da Mesa
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("## ⚡ Terminal de Execução HFT")
        st.caption("Conexão DMA (Direct Market Access) • Latência: 12ms")
    with c2:
        st.markdown(f"<div style='text-align:right; color:#10b981; font-weight:bold;'>SISTEMA ATIVO<br>{datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Layout Principal: Gráfico Operacional + Boleta
    col_chart, col_order = st.columns([3, 1])

    with col_chart:
        # Widget Gráfico Profissional (TradingView) - Substitui o gráfico lento do yfinance
        components.html("""
        <div class="tradingview-widget-container">
          <div id="tradingview_chart"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget(
          {
          "width": "100%",
          "height": 500,
          "symbol": "BMFBOVESPA:WIN1!",
          "interval": "1",
          "timezone": "America/Sao_Paulo",
          "theme": "dark",
          "style": "1",
          "locale": "br",
          "enable_publishing": false,
          "hide_side_toolbar": false,
          "allow_symbol_change": true,
          "details": true,
          "studies": [
            "VbPFixed@tv-basicstudies"
          ],
          "container_id": "tradingview_chart"
          }
          );
          </script>
        </div>
        """, height=500)

    with col_order:
        st.markdown("### 🛒 Boleta Rápida")
        
        # Simulação de Boleta
        ativo = st.selectbox("Ativo", ["WIN1!", "WDO1!", "PETR4", "VALE3"])
        lote = st.number_input("Lotes", min_value=1, value=1)
        
        c_compra, c_venda = st.columns(2)
        with c_compra:
            if st.button("COMPRA", type="primary", use_container_width=True):
                st.toast(f"Ordem de COMPRA enviada: {ativo} ({lote}x)", icon="🟢")
        with c_venda:
            if st.button("VENDA", type="primary", use_container_width=True):
                st.toast(f"Ordem de VENDA enviada: {ativo} ({lote}x)", icon="🔴")
        
        st.markdown("---")
        
        # Livro de Ofertas Visual (DOM Simulado)
        st.markdown("###### 📊 Depth of Market (DOM)")
        st.markdown("""
        <div style="font-size:0.8rem; background:#0f172a; padding:10px; border-radius:5px;">
            <div style="display:flex; justify-content:space-between; color:#ef4444;">
                <span>128.550</span> <span>540k</span>
            </div>
            <div style="display:flex; justify-content:space-between; color:#ef4444;">
                <span>128.545</span> <span>120k</span>
            </div>
            <div style="display:flex; justify-content:space-between; color:#ef4444; font-weight:bold; border-bottom:1px solid #333;">
                <span>128.540</span> <span>85k</span>
            </div>
            <div style="display:flex; justify-content:space-between; color:#10b981; font-weight:bold; border-top:1px solid #333;">
                <span>128.535</span> <span>230k</span>
            </div>
            <div style="display:flex; justify-content:space-between; color:#10b981;">
                <span>128.530</span> <span>450k</span>
            </div>
            <div style="display:flex; justify-content:space-between; color:#10b981;">
                <span>128.525</span> <span>890k</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Painel Inferior: Posições
    st.markdown("### 📋 Posições em Aberto")
    
    # Tabela Estilizada
    data = {
        "Ativo": ["WIN1!", "PETR4"],
        "Lado": ["COMPRA", "VENDA"],
        "Preço Médio": [128450, 38.40],
        "Preço Atual": [128535, 38.35],
        "P&L (R$)": [170.00, 50.00]
    }
    df = pd.DataFrame(data)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "P&L (R$)": st.column_config.NumberColumn(
                "Resultado",
                format="R$ %.2f"
            )
        }
    )
