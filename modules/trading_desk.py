import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta
from modules.ai_agent import consultar_gemini

# --- CONFIGURAÇÃO DA CARTEIRA INTELLIGENCE FLOW ---
ASSETS_PORTFOLIO = {
    "Índices & Futuros": ["WING26", "WDOX25", "IVVB11"],
    "Blue Chips (Drivers)": ["PETR4", "VALE3", "ITUB4", "BBDC4"],
    "High Alpha": ["PRIO3", "WEGE3", "BBAS3"]
}

# --- LÓGICA DE CORRELAÇÃO AVANÇADA ---
def get_correlations(ticker):
    """
    Define os drivers que compõem o preço justo de cada ativo.
    """
    if ticker == "WING26":
        return [
            {"name": "S&P 500 (Global)", "weight": 0.4, "color": "#ffff00"}, # Amarelo
            {"name": "VALE3 (Commodity)", "weight": 0.3, "color": "#d2a106"}, # Dourado Escuro
            {"name": "WDO (Câmbio)", "weight": -0.3, "color": "#ff3333"}     # Vermelho (Correlação Inversa)
        ]
    elif ticker == "PETR4":
        return [{"name": "Brent Oil (Londres)", "weight": 0.8, "color": "#00ff00"}] # Verde
    elif ticker == "VALE3":
        return [{"name": "Iron Ore (Dalian)", "weight": 0.8, "color": "#ff00ff"}]   # Magenta
    elif ticker == "WDOX25":
        return [{"name": "DXY (Global Dollar)", "weight": 0.7, "color": "#00ccff"}] # Azul
    else:
        return [{"name": "Setor/Benchmark", "weight": 0.5, "color": "#cccccc"}]

def generate_complex_intraday_data(ticker, points=120):
    """
    Gera dados sintéticos sofisticados. Para o WING26, gera seus componentes 
    para criar um 'Preço Justo' realista.
    """
    np.random.seed(int(time.time()))
    
    # Preço Base Inicial
    base_price = 132000 if ticker == "WING26" else (5800 if ticker == "WDOX25" else 30.00)
    
    # Gera a curva do Ativo Principal (Random Walk com Volatilidade)
    volatility = 0.0008 # Volatilidade intradiária
    returns = np.random.normal(0, volatility, points)
    price_curve = base_price * (1 + returns).cumprod()
    
    # Gera dados para os Drivers
    drivers = get_correlations(ticker)
    drivers_data = {}
    
    # Calcula o "Fair Value" (Preço Justo Teórico) baseado nos drivers
    # Começa igual ao preço, mas varia diferente para criar oportunidades de arbitragem
    fair_value_curve = price_curve.copy()
    
    for drv in drivers:
        # O Driver segue o ativo mas tem "vida própria" (ruído)
        noise = np.random.normal(0, volatility * 1.5, points)
        
        # Se peso negativo (ex: Dólar vs Índice), inverte o movimento
        direction = 1 if drv['weight'] > 0 else -1
        
        # Cria a curva do driver
        drv_curve = (price_curve * (1 + noise)) 
        
        # Normaliza para porcentagem para plotar junto (Base 0)
        drv_pct = ((drv_curve - drv_curve[0]) / drv_curve[0]) * 100 * direction
        
        drivers_data[drv['name']] = {
            "data": drv_curve,
            "pct": drv_pct,
            "color": drv['color']
        }
        
        # Atualiza o Preço Justo Teórico ponderado
        fair_value_curve += (drv_curve - price_curve) * abs(drv['weight'])

    # Times (Eixo X) - Apenas Hora:Minuto para limpar o gráfico
    now = datetime.now()
    times = [(now - timedelta(minutes=points-i)).strftime("%H:%M") for i in range(points)]
    
    return {
        "times": times,
        "price": price_curve,
        "price_pct": ((price_curve - price_curve[0]) / price_curve[0]) * 100,
        "fair_value": fair_value_curve,
        "drivers": drivers_data
    }

def render_trading_desk():
    # --- CSS HIGH-END SAAS ---
    st.markdown("""
    <style>
        .metric-label {font-size: 0.8rem; color: #94a3b8; letter-spacing: 1px;}
        .metric-value {font-size: 1.8rem; font-weight: 700; color: #e2e8f0;}
        .spread-box {
            background: rgba(210, 161, 6, 0.05); 
            border: 1px solid #d2a106; 
            border-radius: 5px; 
            padding: 10px; 
            text-align: center;
        }
        /* Animação Neon Suave */
        @keyframes pulse-neon {
            0% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.2); }
            50% { box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
            100% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.2); }
        }
        .chart-container { animation: pulse-neon 3s infinite; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 💠 Intelligence Flow | Market Dynamics Analytics")
    st.markdown("<div style='font-size:0.9em; color:#64748b; margin-top:-10px; margin-bottom:20px;'>High-Frequency Data Processing & Arbitrage Monitor</div>", unsafe_allow_html=True)

    # --- 1. CONTROLES DO ANALYTICS ---
    col_sel, col_ctrl = st.columns([2, 3])
    
    with col_sel:
        all_assets = [a for cat in ASSETS_PORTFOLIO.values() for a in cat]
        selected_asset = st.selectbox("Ativo em Análise", all_assets, index=0)
    
    if 'trading_running' not in st.session_state: st.session_state.trading_running = False
    if 'sim_data' not in st.session_state: st.session_state.sim_data = None
    if 'tick_idx' not in st.session_state: st.session_state.tick_idx = 0

    with col_ctrl:
        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("▶️ INICIAR FLUXO", type="primary", use_container_width=True):
                st.session_state.trading_running = True
                st.session_state.sim_data = generate_complex_intraday_data(selected_asset)
                st.session_state.tick_idx = 30 # Buffer inicial
        with c2:
            if st.button("⏸️ PAUSAR", use_container_width=True):
                st.session_state.trading_running = False
        with c3:
            if st.button("⏹️ RESET", use_container_width=True):
                st.session_state.trading_running = False
                st.session_state.tick_idx = 0
                st.rerun()

    # --- 2. ÁREA DINÂMICA (CONTAINERS) ---
    top_metrics = st.empty()
    main_chart = st.empty()
    spread_monitor = st.empty()

    # --- LOOP DO COCKPIT ---
    if st.session_state.trading_running and st.session_state.sim_data is not None:
        
        data = st.session_state.sim_data
        total_ticks = len(data['times'])
        
        while st.session_state.trading_running and st.session_state.tick_idx < total_ticks:
            
            curr = st.session_state.tick_idx
            # Janela de visualização (últimos 40 candles para ficar limpo)
            start = max(0, curr - 40)
            
            # Dados do momento
            curr_price = data['price'][curr]
            prev_price = data['price'][curr-1] if curr > 0 else curr_price
            var_pct = ((curr_price - prev_price)/prev_price)*100
            
            curr_fair = data['fair_value'][curr]
            spread_val = curr_price - curr_fair
            spread_pct = (spread_val / curr_fair) * 100
            
            # 1. MÉTRICAS DE TOPO
            with top_metrics.container():
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Cotação Atual", f"{curr_price:.2f}", f"{var_pct:.3f}%")
                k2.metric("Preço Justo (Modelo)", f"{curr_fair:.2f}", delta_color="off")
                
                # Volatilidade baseada no desvio padrão dos últimos 5 ticks
                recent_vol = np.std(data['price'][max(0, curr-5):curr+1])
                vol_state = "ALTA" if recent_vol > (curr_price * 0.0005) else "NORMAL"
                k3.metric("Regime de Volatilidade", vol_state)
                
                k4.metric("Tick Atual", f"{data['times'][curr]}")

            # 2. MONITOR DE SPREAD (ARBITRAGEM)
            # Mostra a fórmula e o valor vivo piscando se a oportunidade for boa
            with spread_monitor.container():
                col_math, col_res = st.columns([2, 1])
                with col_math:
                    if selected_asset == "WING26":
                        st.latex(r"Spread_{Indice} = P_{WIN} - (\alpha \cdot SPX + \beta \cdot VALE + \gamma \cdot PETR - \delta \cdot WDO)")
                    else:
                        st.latex(r"Spread_{Arbitrage} = \frac{(ADR \times FX) - Local}{Local}")
                
                with col_res:
                    color = "red" if abs(spread_pct) > 0.5 else "green"
                    st.markdown(f"""
                    <div class="spread-box">
                        <span style="font-size:0.9em; color:#d2a106;">SPREAD / DIVERGÊNCIA</span><br>
                        <span style="font-size:1.8rem; font-weight:bold; color:{color};">
                            {spread_pct:+.2f}%
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

            # 3. GRÁFICO MULTI-FATOR (A JOIA DO SISTEMA)
            fig = go.Figure()
            
            # Ativo Principal (Linha Branca Grossa + Área)
            slice_times = data['times'][start:curr+1]
            slice_price_pct = data['price_pct'][start:curr+1]
            
            fig.add_trace(go.Scatter(
                x=slice_times, y=slice_price_pct,
                mode='lines', name=selected_asset,
                line=dict(color='white', width=4),
                fill='tozeroy', fillcolor='rgba(255, 255, 255, 0.05)'
            ))
            
            # Plota os Drivers (Correlações)
            for drv_name, drv_info in data['drivers'].items():
                fig.add_trace(go.Scatter(
                    x=slice_times, 
                    y=drv_info['pct'][start:curr+1],
                    mode='lines', name=drv_name,
                    line=dict(color=drv_info['color'], width=2, dash='dot')
                ))

            fig.update_layout(
                template="plotly_dark",
                height=500,
                title=dict(text="<b>Dinâmica de Preços e Correlações</b>", font=dict(color="#e2e8f0")),
                xaxis=dict(showgrid=False, tickfont=dict(color="#64748b")), # Eixo X Limpo
                yaxis=dict(showgrid=True, gridcolor="#334155", zerolinecolor="#475569"),
                legend=dict(orientation="h", y=1.02, x=0, bgcolor='rgba(0,0,0,0)'),
                margin=dict(l=0, r=0, t=50, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            main_chart.plotly_chart(fig, use_container_width=True)
            
            st.session_state.tick_idx += 1
            time.sleep(1) # Delay realista (1s)

    else:
        st.info("Aguardando inicialização do fluxo de dados...")

# Função de compatibilidade (para evitar erro no app.py)
def show_desk():
    render_trading_desk()
