import streamlit as st
import streamlit.components.v1 as components

def show_landing_page():
    # HERO SECTION
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="color: #fff; text-shadow: 0 0 20px rgba(59, 130, 246, 0.5);">INTELLIGENCE FLOW</h1>
        <p style="color: #94a3b8; font-size: 1.2rem;">ECOSSISTEMA INSTITUCIONAL DE ALTA FREQUÊNCIA</p>
    </div>
    """, unsafe_allow_html=True)

    # WIDGET 1: TICKER TAPE (60fps Scrolling)
    # Isso roda liso em qualquer dispositivo (TV, Celular)
    components.html("""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      {
      "symbols": [
        {"proName": "FOREXCOM:SPXUSD", "title": "S&P 500"},
        {"proName": "FOREXCOM:NSXUSD", "title": "US 100"},
        {"proName": "FX_IDC:USDBRL", "title": "USD/BRL"},
        {"proName": "BITSTAMP:BTCUSD", "title": "Bitcoin"},
        {"proName": "BMFBOVESPA:IBOV", "title": "IBOVESPA"}
      ],
      "showSymbolLogo": true,
      "colorTheme": "dark",
      "isTransparent": true,
      "displayMode": "adaptive",
      "locale": "br"
      }
      </script>
    </div>
    """, height=50)

    st.markdown("<br>", unsafe_allow_html=True)

    # WIDGET 2: GRÁFICO AVANÇADO (Market Overview)
    # Interativo, responsivo e em tempo real (simulado via widget)
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("### 📡 Monitoramento Global (HFT Feed)")
        components.html("""
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-overview.js" async>
          {
          "colorTheme": "dark",
          "dateRange": "12M",
          "showChart": true,
          "locale": "br",
          "largeChartUrl": "",
          "isTransparent": true,
          "showSymbolLogo": true,
          "showFloatingTooltip": true,
          "width": "100%",
          "height": "400",
          "plotLineColorGrowing": "rgba(41, 98, 255, 1)",
          "plotLineColorFalling": "rgba(41, 98, 255, 1)",
          "gridLineColor": "rgba(240, 243, 250, 0)",
          "scaleFontColor": "rgba(106, 109, 120, 1)",
          "belowLineFillColorGrowing": "rgba(41, 98, 255, 0.12)",
          "belowLineFillColorFalling": "rgba(41, 98, 255, 0.12)",
          "belowLineFillColorGrowingBottom": "rgba(41, 98, 255, 0)",
          "belowLineFillColorFallingBottom": "rgba(41, 98, 255, 0)",
          "symbolActiveColor": "rgba(41, 98, 255, 0.12)",
          "tabs": [
            {
              "title": "Índices",
              "symbols": [
                { "s": "FOREXCOM:SPXUSD" },
                { "s": "FOREXCOM:NSXUSD" },
                { "s": "FOREXCOM:DJI" },
                { "s": "INDEX:DXY" }
              ],
              "originalTitle": "Indices"
            },
            {
              "title": "Commodities",
              "symbols": [
                { "s": "CME_MINI:CL1!" },
                { "s": "COMEX:GC1!" }
              ],
              "originalTitle": "Futures"
            }
          ]
          }
          </script>
        </div>
        """, height=400)

    with c2:
        st.markdown("### 📊 Inteligência de Mercado")
        st.markdown("""
        <div class="tech-card">
            <h4 style="color:#60a5fa">Dinâmica de Liquidez</h4>
            <p>Monitoramos o fluxo oculto (Dark Pools) que antecede o movimento de preço na tela.</p>
        </div>
        <div class="tech-card">
            <h4 style="color:#10b981">Conectividade</h4>
            <p>Latência ultrabaixa entre B3 (São Paulo) e NYSE (Nova York).</p>
        </div>
        <div class="tech-card">
            <h4 style="color:#f59e0b">Players</h4>
            <p>Rastreamento de Market Makers institucionais (UBS, JPM, GS).</p>
        </div>
        """, unsafe_allow_html=True)
