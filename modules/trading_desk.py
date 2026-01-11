import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from modules.ai_agent import consultar_gemini  # Importa a IA que criamos acima

def render_trading_desk():
    st.markdown("## 🦅 Trading Desk | Intelligence Flow")
    
    # --- 1. SELEÇÃO DE ATIVO ---
    col1, col2 = st.columns([1, 4])
    with col1:
        ativo = st.selectbox("Ativo Principal", ["WING26", "PETR4", "VALE3"])

    # --- 2. DADOS (Simulação para Visualização - Substitua por API real depois) ---
    times = pd.date_range(start="09:00", periods=40, freq="10min").strftime("%H:%M")
    
    # Normalização em % (Tudo partindo do zero)
    df = pd.DataFrame({
        "Hora": times,
        "Principal": [x * 0.15 for x in range(40)], # Tendência Alta
        "Driver_Petro": [x * 0.12 for x in range(40)], # Segue
        "Driver_Vale": [x * -0.05 for x in range(40)], # Divergência
        "Juros_DI": [x * -0.02 for x in range(40)]  # Juros Caindo (Bom)
    })

    # --- 3. GRÁFICO DE DRIVERS (3 LINHAS + JUROS) ---
    st.markdown("### 📊 Drivers de Mercado (Força Relativa %)")
    
    fig = go.Figure()
    
    # Linha Dourada (Principal)
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Principal'], mode='lines', name=ativo,
                             line=dict(color='#d2a106', width=4)))
    
    # Drivers (Azul e Laranja)
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Driver_Petro'], mode='lines', name='PETR4',
                             line=dict(color='#3b82f6', width=2)))
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Driver_Vale'], mode='lines', name='VALE3',
                             line=dict(color='#f97316', width=2)))
    
    # Juros Futuros (Vermelho)
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Juros_DI'], mode='lines', name='DI Futuro',
                             line=dict(color='#ef4444', width=2, dash='dot')))

    fig.update_layout(template="plotly_dark", height=450, margin=dict(t=30, l=0, r=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

    # --- 4. ARBITRAGEM E PAINEL IA ---
    c_arb, c_ai = st.columns(2)
    
    with c_arb:
        st.markdown("### ⚖️ Monitor Arbitragem")
        # Simulação Cálculo
        adr = 13.50
        fx = 5.85
        local = 39.00
        ratio = 2
        
        parity = (adr * fx) / ratio
        spread = ((local - parity) / parity) * 100
        
        st.latex(r'''Spread = \frac{(ADR \times FX) - Local}{Local}''')
        st.metric("Spread Atual", f"{spread:.2f}%", 
                  delta_color="off" if -0.5 < spread < 0.5 else "inverse")

    with c_ai:
        st.markdown("### 🤖 IA Intelligence Flow")
        if st.button("Gerar Análise de Fluxo"):
            with st.spinner("Analisando mercado..."):
                # Prepara dados para enviar
                info = {
                    "Ativo": ativo,
                    "Tendencia": "Alta",
                    "Divergencia": "Sim (Vale negativa)",
                    "Juros": "Queda"
                }
                # CHAMA A FUNÇÃO DO ARQUIVO SEPARADO
                resultado = consultar_gemini(info, spread)
                st.info(resultado)
