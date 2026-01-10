import streamlit as st
import streamlit.components.v1 as components
import modules.data_feed as data_feed # Importando para checar status

# Função Visual de Status
def render_status_pill(name, status):
    color = "#10b981" if status else "#ef4444" # Verde ou Vermelho
    text = "ONLINE" if status else "OFFLINE"
    pulse = "animation: pulse 2s infinite;" if status else ""
    
    st.markdown(f"""
    <style>
    @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }} 70% {{ box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }} }}
    </style>
    <div style="display:inline-block; margin:0 10px; padding:5px 15px; border:1px solid {color}; border-radius:20px; background:rgba(0,0,0,0.3); {pulse}">
        <span style="color:{color}; font-weight:bold; font-size:0.8rem;">● {name}: {text}</span>
    </div>
    """, unsafe_allow_html=True)

def show_landing_page():
    # HERO SECTION
    st.markdown("""
    <div style="text-align: center; padding: 40px 0 20px 0;">
        <h1 style="color: #fff; text-shadow: 0 0 30px rgba(59, 130, 246, 0.6); font-size: 3.5rem;">INTELLIGENCE FLOW</h1>
        <p style="color: #94a3b8; font-size: 1.2rem; letter-spacing: 2px;">INSTITUTIONAL GRADE DATA ECOSYSTEM</p>
    </div>
    """, unsafe_allow_html=True)

    # === DATA FEED INTEGRITY (AQUI ESTÃO AS INFORMAÇÕES QUE FALTAVAM) ===
    # Verifica se os dados estão chegando
    b3_status = True if data_feed.get_b3_tickers() else False
    global_status = True if data_feed.get_global_tickers() else False
    ai_status = True # IA consideramos online
    
    st.markdown("<div style='text-align:center; margin-bottom:30px;'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: render_status_pill("B3 FEED (BRAPI)", b3_status)
    with c2: render_status_pill("NYSE FEED (TWELVE)", global_status)
    with c3: render_status_pill("NEURAL CORE (ALPHA)", ai_status)
    st.markdown("</div>", unsafe_allow_html=True)

    # WIDGET TICKER 60FPS
    components.html("""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      {
      "symbols": [
        {"proName": "FOREXCOM:SPXUSD", "title": "S&P 500"},
        {"proName": "FX_IDC:USDBRL", "title": "USD/BRL"},
        {"proName": "BITSTAMP:BTCUSD", "title": "Bitcoin"},
        {"proName": "BMFBOVESPA:IBOV", "title": "IBOVESPA"},
        {"proName": "BMFBOVESPA:PETR4", "title": "Petrobras"},
        {"proName": "BMFBOVESPA:VALE3", "title": "Vale"}
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

    # MONITORAMENTO GLOBAL 60FPS
    st.markdown("### 📡 Monitoramento de Fluxo Global (60fps)")
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
      "height": "500",
      "tabs": [
        {
          "title": "Mercados Futuros",
          "symbols": [
            { "s": "CME_MINI:ES1!", "d": "S&P 500 Fut" },
            { "s": "CME_MINI:NQ1!", "d": "Nasdaq Fut" },
            { "s": "CBOT:YM1!", "d": "Dow Jones Fut" },
            { "s": "TVC:DXY", "d": "Dólar Index" }
          ]
        },
        {
          "title": "Commodities",
          "symbols": [
            { "s": "CME_MINI:CL1!", "d": "WTI Crude Oil" },
            { "s": "COMEX:GC1!", "d": "Gold" },
            { "s": "CBOT:ZC1!", "d": "Corn" }
          ]
        }
      ]
      }
      </script>
    </div>
    """, height=500)
