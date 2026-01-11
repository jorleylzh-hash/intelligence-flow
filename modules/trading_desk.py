import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from modules.ai_agent import consultar_gemini

def render_trading_desk():
    st.markdown("## 🦅 Trading Desk | Intelligence Flow")
    
    # --- 1. CONTROLES E SELEÇÃO ---
    col1, col2 = st.columns([1, 4])
    with col1:
        ativo = st.selectbox("Ativo Principal", ["WING26", "PETR4", "VALE3"])

    # --- 2. DADOS DE MERCADO (SIMULAÇÃO) ---
    # Gera dados fictícios para o gráfico visual
    times = pd.date_range(start="09:00", periods=40, freq="10min").strftime("%H:%M")
    df = pd.DataFrame({
        "Hora": times,
        "Principal": [x * 0.15 for x in range(40)],
        "Driver_Petro": [x * 0.12 for x in range(40)],
        "Driver_Vale": [x * -0.05 for x in range(40)],
        "Juros_DI": [x * -0.02 for x in range(40)]
    })

    # --- 3. GRÁFICO DE DRIVERS (PLOTLY) ---
    st.markdown("### 📊 Drivers de Mercado (Força Relativa %)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Principal'], mode='lines', name=ativo, line=dict(color='#d2a106', width=4)))
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Driver_Petro'], mode='lines', name='PETR4', line=dict(color='#3b82f6', width=2)))
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Driver_Vale'], mode='lines', name='VALE3', line=dict(color='#f97316', width=2)))
    fig.add_trace(go.Scatter(x=df['Hora'], y=df['Juros_DI'], mode='lines', name='DI Futuro', line=dict(color='#ef4444', width=2, dash='dot')))
    
    fig.update_layout(template="plotly_dark", height=400, margin=dict(t=30, l=0, r=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

    # --- 4. ÁREA INFERIOR: ARBITRAGEM E IA ---
    c_arb, c_ai = st.columns([1, 1])
    
    # --- COLUNA DA ESQUERDA: MONITOR DE ARBITRAGEM ---
    with c_arb:
        st.markdown("### ⚖️ Monitor Arbitragem")
        
        # Valores de exemplo (Fixos para demonstração da fórmula)
        adr = 13.50  # Preço em NY
        fx = 5.85    # Dólar
        local = 39.00 # Preço B3
        
        # Cálculo Matemático
        parity = (adr * fx) / 2 # /2 assumindo proporção 1:2 das ações (exemplo Petro)
        spread = ((local - parity) / parity) * 100
        
        # Exibe a Fórmula LaTeX
        st.latex(r'''Spread = \frac{(ADR \times FX) - Local}{Local}''')
        
        # Métricas Visuais
        c_met1, c_met2 = st.columns(2)
        c_met1.metric("Preço Justo (Paridade)", f"R$ {parity:.2f}")
        c_met2.metric("Spread Atual", f"{spread:.2f}%", delta_color="off" if -0.5 < spread < 0.5 else "inverse")
        
        st.info("💡 Spread negativo indica oportunidade de COMPRA na B3 (Desconto em relação a NY).")

    # --- COLUNA DA DIREITA: AGENTE INTELLIGENCE FLOW ---
    with c_ai:
        st.markdown("### 🤖 Agente Intelligence Flow")
        
        # "Cheat Sheet" - Painel de Comandos Visuais
        st.markdown("""
        <div style="background-color: #1e293b; border-left: 4px solid #d2a106; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <strong style="color: #e2e8f0;">⌨️ Comandos de Sistema Disponíveis:</strong>
            <ul style="margin-top: 5px; color: #94a3b8; font-family: monospace; font-size: 0.9em;">
                <li style="margin-bottom: 5px;">
                    <span style="color: #d2a106; font-weight: bold;">assets value</span> : 
                    Exibir cotações em tempo real (Renda Fixa, Variável e Câmbio).
                </li>
                <li>
                    <span style="color: #d2a106; font-weight: bold;">educational map</span> : 
                    Visualizar Ementa de Estudos (SFN, B3, Derivativos e Conceitos).
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Campo de Interação
        user_query = st.text_input("Terminal de Consulta:", placeholder="Digite um comando ou faça uma pergunta sobre o mercado...")
        
        # Botão de Ação
        if st.button("ENVIAR COMANDO / PERGUNTA 🚀", use_container_width=True):
            if user_query:
                with st.spinner("Processando solicitação..."):
                    # Prepara contexto técnico para enviar junto à pergunta (caso necessário)
                    contexto_tecnico = {
                        "Ativo_Selecionado": ativo,
                        "Spread_Arbitragem": f"{spread:.2f}%",
                        "Tendencia_Grafica": "Alta (Simulada)"
                    }
                    
                    # Chama a função inteligente no ai_agent.py
                    resposta = consultar_gemini(user_query, str(contexto_tecnico))
                    
                    # Exibe a resposta
                    st.markdown("---")
                    st.markdown(resposta)
            else:
                st.warning("⚠️ O campo de comando está vazio.")

# Função de fallback para compatibilidade com versões antigas do app.py
def show_desk():
    render_trading_desk()
