import streamlit as st
import streamlit.components.v1 as components
import modules.data_feed as data_feed

# Função Visual de Status
def render_status_pill(name, status):
    color = "#10b981" if status else "#ef4444" 
    text = "ONLINE" if status else "OFFLINE"
    pulse = "animation: pulse 2s infinite;" if status else ""
    
    st.markdown(f"""
    <style>
    @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }} 70% {{ box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }} }}
    </style>
    <div style="display:inline-block; margin:5px 10px; padding:6px 15px; border:1px solid {color}; border-radius:20px; background:rgba(15, 23, 42, 0.8); {pulse}">
        <span style="color:{color}; font-weight:bold; font-size:0.85rem; letter-spacing:1px;">● {name}: {text}</span>
    </div>
    """, unsafe_allow_html=True)

def show_landing_page():
    # HERO SECTION
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 20px 0;">
        <h1 style="color: #fff; text-shadow: 0 0 40px rgba(37, 99, 235, 0.6); font-size: 3.2rem; margin-bottom: 10px;">INTELLIGENCE FLOW</h1>
        <p style="color: #94a3b8; font-size: 1.1rem; letter-spacing: 3px; font-weight: 300;">INSTITUTIONAL GRADE DATA ECOSYSTEM</p>
    </div>
    """, unsafe_allow_html=True)

    # === STATUS DAS APIS ===
    b3_ok = True if data_feed.get_b3_tickers() else False
    nyse_ok = True if data_feed.get_global_tickers() else False
    ai_ok = True
    
    st.markdown("<div style='text-align:center; margin-bottom:30px; display:flex; justify-content:center; flex-wrap:wrap;'>", unsafe_allow_html=True)
    render_status_pill("B3 FEED (BRAPI)", b3_ok)
    render_status_pill("NYSE FEED (TWELVE)", nyse_ok)
    render_status_pill("NEURAL CORE (ALPHA)", ai_ok)
    st.markdown("</div>", unsafe_allow_html=True)

    # WIDGET 1: TICKER TAPE (FITA DE COTAÇÕES)
    # Configurado EXATAMENTE com os ativos pedidos
    components.html("""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      {
      "symbols": [
        {"proName": "FOREXCOM:SPXUSD", "title": "S&P 500 Fut"},
        {"proName": "TVC:DXY", "title": "DXY (Dólar Global)"},
        {"proName": "NYSE:PBR", "title": "Petrobras ADR (NY)"},
        {"proName": "BMFBOVESPA:WIN1!", "title": "WIN Futuro"},
        {"proName": "BMFBOVESPA:WDO1!", "title": "Dólar Futuro"},
        {"proName": "BMFBOVESPA:VALE3", "title": "Vale S.A."}
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

    # WIDGET 2: MONITORAMENTO ESTRATÉGICO (Separado em Abas)
    st.markdown("### 📡 Radar de Mercado (60fps)")
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
      "height": "550",
      "plotLineColorGrowing": "rgba(16, 185, 129, 1)",
      "plotLineColorFalling": "rgba(239, 68, 68, 1)",
      "gridLineColor": "rgba(240, 243, 250, 0)",
      "scaleFontColor": "rgba(106, 109, 120, 1)",
      "belowLineFillColorGrowing": "rgba(16, 185, 129, 0.12)",
      "belowLineFillColorFalling": "rgba(239, 68, 68, 0.12)",
      "belowLineFillColorGrowingBottom": "rgba(41, 98, 255, 0)",
      "belowLineFillColorFallingBottom": "rgba(41, 98, 255, 0)",
      "symbolActiveColor": "rgba(41, 98, 255, 0.12)",
      "tabs": [
        {
          "title": "🌎 Ativos Globais (Drivers)",
          "symbols": [
            { "s": "FOREXCOM:SPXUSD", "d": "S&P 500 Fut (EUA)" },
            { "s": "TVC:DXY", "d": "Índice Dólar (DXY)" },
            { "s": "NYSE:PBR", "d": "Petrobras ADR (NY)" },
            { "s": "NYSE:VALE", "d": "Vale ADR (NY)" }
          ]
        },
        {
          "title": "🇧🇷 Ativos Locais (B3)",
          "symbols": [
            { "s": "BMFBOVESPA:WIN1!", "d": "Índice Futuro (WIN)" },
            { "s": "BMFBOVESPA:WDO1!", "d": "Dólar Futuro (WDO)" },
            { "s": "BMFBOVESPA:VALE3", "d": "Vale ON" },
            { "s": "BMFBOVESPA:PETR4", "d": "Petrobras PN" }
          ]
        },
        {
          "title": "🛢️ Commodities Base",
          "symbols": [
            { "s": "TVC:UKOIL", "d": "Petróleo Brent" },
            { "s": "COMEX:GC1!", "d": "Ouro Futuro" }
          ]
        }
      ]
      }
      </script>
    </div>
    """, height=550)
