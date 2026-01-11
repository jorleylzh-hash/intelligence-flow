import streamlit as st
import pandas as pd
import random

# Tenta importar de forma segura
try:
    from modules.ai_agent import gerar_roadmap_solucoes
except ImportError:
    def gerar_roadmap_solucoes(x): return "⚠️ Erro: modules/ai_agent.py não encontrado."

def render_driver_card(name, value, weight, correlation, explanation):
    color = "#10b981" if correlation > 0 else "#ef4444"
    corr_text = "Positiva" if correlation > 0 else "Inversa"
    st.markdown(f"""
    <div style="background:rgba(30, 41, 59, 0.7); border-left:4px solid {color}; padding:15px; border-radius:8px; margin-bottom:10px;">
        <h4 style="margin:0; color:#fff;">{name}</h4>
        <div style="font-size:1.2rem; font-weight:bold; color:#cbd5e1;">{value}</div>
        <div style="font-size:0.8rem; color:#94a3b8;">Corr: {corr_text} ({correlation})</div>
    </div>
    """, unsafe_allow_html=True)

def show_solutions():
    st.markdown("## 💎 Intelligence Flow Solutions")
    
    tab_market, tab_ai = st.tabs(["💠 Market Drivers", "🚀 Consultoria IA"])

    # ABA 1: DRIVERS
    with tab_market:
        st.markdown("<br>", unsafe_allow_html=True)
        target = st.selectbox("Ativo Alvo:", ["WIN", "WDO", "PETR4", "VALE3"])
        if st.button("GERAR MAPA ⚡"):
            st.success(f"Mapeando drivers para {target}...")
            c1, c2 = st.columns(2)
            with c1: render_driver_card("S&P 500", "5.230", "Alto", 0.85, "Direcional")
            with c2: render_driver_card("DI Futuro", "10.45%", "Alto", -0.92, "Juros")

    # ABA 2: IA GEMINI (Corrigido o erro de sintaxe)
    with tab_ai:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 🧠 Arquiteto de Soluções")
        
        c1, c2 = st.columns([3, 1])
        with c1:
            desafio = st.text_area("Descreva o Desafio:", height=100)
        with c2:
            st.write("")
            st.write("")
            btn_gerar = st.button("DESENHAR MAPA 🚀", use_container_width=True)

        # Lógica simplificada para evitar erros
        if btn_gerar and desafio:
            st.session_state['solucao_pronta'] = False 
            with st.spinner("IA desenhando o mapa..."):
                resp = gerar_roadmap_solucoes(desafio)
                st.session_state['resultado_mapa'] = resp
                st.session_state['solucao_pronta'] = True

        if st.session_state.get('solucao_pronta'):
            st.markdown("---")
            st.markdown(st.session_state['resultado_mapa'])
            if st.button("Limpar"):
                st.session_state['solucao_pronta'] = False
                st.rerun()
