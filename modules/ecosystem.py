import streamlit as st
import streamlit.components.v1 as components

def show_ecosystem():
    st.markdown("## 💠 Metodologia Integrada (Conceito & Visualização)")
    st.markdown("Explore nossos pilares operacionais. Selecione uma aba para visualizar a tecnologia aplicada.")
    
    st.markdown("---")
    
    # ABAS INTERATIVAS
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SMC & Liquidez", "🕯️ Price Action Puro", "⚡ Market Making (DOM)", "📅 Macro Drivers"])
    
    # 1. SMC (SMART MONEY CONCEPTS)
    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.info("💡 **Conceito:** O gráfico não mostra linhas, mostra onde o dinheiro institucional 'descansa'. Order Blocks e FVG são ímãs de preço.")
        with c2:
            st.caption("Visualização: Gráfico Avançado com Indicadores de Volume")
            # Widget Gráfico Avançado (Simulando SMC com Candles)
            components.html("""
            <div class="tradingview-widget-container">
              <div id="tradingview_smc"></div>
              <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
              <script type="text/javascript">
              new TradingView.widget(
              {
              "width": "100%",
              "height": 400,
              "symbol": "BMFBOVESPA:PETR4",
              "interval": "5",
              "timezone": "America/Sao_Paulo",
              "theme": "dark",
              "style": "1",
              "locale": "br",
              "toolbar_bg": "#f1f3f6",
              "enable_publishing": false,
              "hide_side_toolbar": false,
              "allow_symbol_change": true,
              "studies": ["Volume@tv-basicstudies"],
              "container_id": "tradingview_smc"
              }
              );
              </script>
            </div>
            """, height=400)

    # 2. PRICE ACTION
    with tab2:
        st.caption("Visualização: Ação do Preço Pura (Candlestick Analysis)")
        components.html("""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
          {
          "symbols": [
            ["IBOV", "BMFBOVESPA:IBOV|1D"],
            ["Dólar", "FX_IDC:USDBRL|1D"],
            ["S&P 500", "FOREXCOM:SPXUSD|1D"]
          ],
          "chartOnly": false,
          "width": "100%",
          "height": 400,
          "locale": "br",
          "colorTheme": "dark",
          "autosize": false,
          "showVolume": false,
          "hideDateRanges": false,
          "scalePosition": "right",
          "scaleMode": "Normal",
          "fontFamily": "-apple-system, BlinkMacSystemFont, Trebuchet MS, Roboto, Ubuntu, sans-serif",
          "fontSize": "10",
          "noTimeScale": false,
          "valuesTracking": "1",
          "changeMode": "price-and-percent",
          "chartType": "candlestick"
          }
          </script>
        </div>
        """, height=400)

    # 3. MARKET MAKING & DOM
    with tab3:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.info("💡 **Conceito:** O Market Maker provê liquidez. O DOM (Depth of Market) mostra as intenções de compra e venda antes da execução.")
        with c2:
            st.caption("Visualização: Simulação de Fluxo/Forex Cross Rates")
            components.html("""
            <div class="tradingview-widget-container">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-forex-cross-rates.js" async>
              {
              "width": "100%",
              "height": 400,
              "currencies": [
                "EUR",
                "USD",
                "JPY",
                "GBP",
                "CHF",
                "AUD",
                "CAD",
                "BRL"
              ],
              "isTransparent": true,
              "colorTheme": "dark",
              "locale": "br"
              }
              </script>
            </div>
            """, height=400)

    # 4. MACRO DRIVERS
    with tab4:
        st.caption("Visualização: Calendário Econômico (Drivers de Volatilidade)")
        components.html("""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
          {
          "colorTheme": "dark",
          "isTransparent": true,
          "width": "100%",
          "height": "400",
          "locale": "br",
          "importanceFilter": "0,1",
          "currencyFilter": "USD,BRL,EUR"
          }
          </script>
        </div>
        """, height=400)
