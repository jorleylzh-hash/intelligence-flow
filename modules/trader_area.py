import streamlit as st
import pandas as pd
import plotly.graph_objects as go
# Importa a função do arquivo vizinho dentro da pasta modules
from modules.ai_agent import consultar_gemini 

def render_trader_area():
    st.markdown("## 🦅 Intelligence Flow | Trader Cockpit")
    
    # --- 1. SELEÇÃO DE ATIVO ---
    col_sel, col_blank = st.columns([1, 3])
    with col_sel:
        ativo_principal = st.selectbox("Ativo Principal", ["WING26", "PETR4", "VALE3"])

    # --- 2. SIMULAÇÃO DE DADOS (Substitua por BRAPI aqui depois) ---
    # Normalizando dados para % para caber tudo no mesmo gráfico
    times = pd.date_range(start="09:00", periods=40, freq="10min").strftime("%H:%M")
    
    # Dados fictícios para estrutura visual
    df = pd.DataFrame({
        "Hora": times,
        "Principal": [x * 0.15 for x in range(40)], # Tendência Alta
        "Driver_1":  [x * 0.12 for x in range(40)], # Segue
        "Driver_2":  [x * -0.05 for x in range(40)], # Divergência
        "Juros_DI":  [x * -0.02 for x in range(40)]  # Caindo (Ajuda o índice)
    })

    # --- 3. GRÁFICO DRIVERS (NORMALIZADO EM %) ---
    st.markdown("### 📊 Drivers de Mercado (Correlação Intraday %)")
    
    fig = go.Figure()
    
    # Linha Principal (Ouro)
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Principal'], mode='lines', name=ativo_principal,
                             line=dict(color='#d2a106', width=4)))
    
    # Drivers (Cores frias)
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Driver_1'], mode='lines', name='Driver 1 (Petro)',
                             line=dict(color='#3b82f6', width=2)))
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Driver_2'], mode='lines', name='Driver 2 (Vale)',
                             line=dict(color='#f97316', width=2)))
    
    # Juros Futuros (Vermelho - Importante!)
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Juros_DI'], mode='lines', name='Juros Futuros (DI)',
                             line=dict(color='#ef4444', width=2, dash='dot')))

    fig.update_layout(
        template="plotly_dark", 
        height=450, 
        title="Todos os ativos partindo de 0% (Força Relativa)",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- 4. ARBITRAGEM E IA ---
    col_arb, col_ai = st.columns(2)
    
    with col_arb:
        st.markdown("### ⚖️ Monitor Arbitragem")
        
        # Dados Exemplo
        adr_ny = 13.20
        fx = 5.85
        local_b3 = 38.50
        ratio = 2 # Ex: 2 ações = 1 ADR
        
        parity = (adr_ny * fx) / ratio
        spread = ((local_b3 - parity) / parity) * 100
        
        st.latex(r'''Spread = \frac{(ADR \times FX) - Local}{Local}''')
        
        c1, c2 = st.columns(2)
        c1.metric("Preço Justo (Paridade)", f"R$ {parity:.2f}")
        c2.metric("Spread Atual", f"{spread:.2f}%", 
                  delta_color="off" if -0.5 < spread < 0.5 else "inverse")

    with col_ai:
        st.markdown("### 🤖 IA Intelligence Flow")
        st.write("Conectado ao Gemini via Python")
        
        if st.button("Analisar Fluxo Agora"):
            with st.spinner("Lendo mercado..."):
                # Pacote de dados para a IA
                info_mercado = {
                    "Ativo": ativo_principal,
                    "Tendencia_Principal": f"Alta de {df['Principal'].iloc[-1]}%",
                    "Juros": "Em queda (Favorável)",
                    "Divergencia": "Sim, Driver 2 negativo"
                }
                
                # CHAMA O ARQUIVO ai_agent.py
                analise = consultar_gemini(info_mercado, spread)
                st.info(analise)
