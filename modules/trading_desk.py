import streamlit as st
import pandas as pd
import plotly.graph_objects as go
# Importa a função correta do arquivo ai_agent.py
from modules.ai_agent import consultar_gemini

def render_trading_desk():
    st.markdown("## 🦅 Trading Desk | Intelligence Flow")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        ativo = st.selectbox("Ativo Principal", ["WING26", "PETR4", "VALE3"])

    # Dados Simulados
    times = pd.date_range(start="09:00", periods=40, freq="10min").strftime("%H:%M")
    df = pd.DataFrame({
        "Hora": times,
        "Principal": [x * 0.15 for x in range(40)],
        "Driver_Petro": [x * 0.12 for x in range(40)],
        "Driver_Vale": [x * -0.05 for x in range(40)],
        "Juros_DI": [x * -0.02 for x in range(40)]
    })

    st.markdown("### 📊 Drivers de Mercado (Força Relativa %)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Principal'], mode='lines', name=ativo, line=dict(color='#d2a106', width=4)))
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Driver_Petro'], mode='lines', name='PETR4', line=dict(color='#3b82f6', width=2)))
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Driver_Vale'], mode='lines', name='VALE3', line=dict(color='#f97316', width=2)))
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Juros_DI'], mode='lines', name='DI Futuro', line=dict(color='#ef4444', width=2, dash='dot')))
    fig.update_layout(template="plotly_dark", height=450, margin=dict(t=30, l=0, r=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

    c_arb, c_ai = st.columns(2)
    with c_arb:
        st.markdown("### ⚖️ Monitor Arbitragem")
        adr, fx, local = 13.50, 5.85, 39.00
        parity = (adr * fx) / 2
        spread = ((local - parity) / parity) * 100
        st.latex(r'''Spread = \frac{(ADR \times FX) - Local}{Local}''')
        st.metric("Spread Atual", f"{spread:.2f}%")

    with c_ai:
        st.markdown("### 🤖 IA Intelligence Flow")
        if st.button("Gerar Análise de Fluxo"):
            with st.spinner("Analisando mercado..."):
                info = {"Ativo": ativo, "Tendencia": "Alta", "Divergencia": "Sim", "Juros": "Queda"}
                # Chama a função restaurada
                resultado = consultar_gemini(info, spread)
                st.info(resultado)
