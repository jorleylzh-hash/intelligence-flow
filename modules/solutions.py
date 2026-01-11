import streamlit as st
import pandas as pd
import random

# Tenta importar a IA de forma segura
try:
    from modules.ai_agent import gerar_roadmap_solucoes
except ImportError:
    def gerar_roadmap_solucoes(x): return "⚠️ Erro: Arquivo modules/ai_agent.py não encontrado."

# --- FUNÇÃO AUXILIAR DE DESIGN ---
def render_driver_card(name, value, weight, correlation, explanation):
    color = "#10b981" if correlation > 0 else "#ef4444"
    corr_text = "Positiva" if correlation > 0 else "Inversa"
    
    st.markdown(f"""
    <div style="background:rgba(30, 41, 59, 0.7); border-left:4px solid {color}; padding:15px; border-radius:8px; margin-bottom:10px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h4 style="margin:0; color:#fff;">{name}</h4>
            <span style="background:{color}; color:white; padding:2px 8px; border-radius:10px; font-size:0.7rem; font-weight:bold;">Corr. {corr_text} ({correlation})</span>
        </div>
        <div style="font-size:1.2rem; font-weight:bold; color:#cbd5e1; margin-top:5px;">{value}</div>
        <div style="font-size:0.85rem; color:#94a3b8; margin-top:5px;">
            <i>Impacto no Preço:</i> <b>{weight}</b><br>
            {explanation}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- TELA PRINCIPAL ---
def show_solutions():
    st.markdown("## 💎 Intelligence Flow Solutions")
    
    tab_market, tab_ai = st.tabs(["💠 Market Drivers", "🚀 Consultoria IA"])

    # === ABA 1: DRIVERS DE MERCADO ===
    with tab_market:
        st.markdown("<br>", unsafe_allow_html=True)
        target_asset = st.selectbox("Ativo Alvo:", ["WIN (Índice)", "WDO (Dólar)", "PETR4", "VALE3"])
        
        if st.button("GERAR MAPA ⚡", key="btn_mkt"):
            st.markdown("---")
            col_main, col_drivers = st.columns([1, 2])
            
            # Exemplo Visual Simplificado para não estourar linhas
            with col_main:
                st.info(f"Analisando {target_asset}...")
                st.metric("Preço Justo", "Calculando...", "---")
            
            with col_drivers:
                render_driver_card("S&P 500", "5.230", "Alto", 0.85, "Direcional de abertura.")
                render_driver_card("Juros DI", "10.45%", "Alto", -0.92, "Correlação inversa.")

    # === ABA 2: IA GEMINI (ONDE O ERRO OCORREU) ===
    with tab_ai:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 🧠 Arquiteto de Soluções")
        
        c1, c2 = st.columns([3, 1])
        with c1:
            desafio = st.text_area("Descreva o Desafio:", height=100)
        with c2:
            st.write("")
            st.write("")
            btn_gerar = st.button("DESENHAR MAPA 🚀", key="btn_ai", use_container_width=True)

        if btn_gerar and desafio:
            st.session_state['solucao_gerada'] = True
            st.session_state['ultimo_desafio'] = desafio
            
        # Lógica corrigida para evitar erro de sintaxe
        if st.session_state.get('solucao_gerada'):
            
            # Verificações quebradas em linhas separadas para segurança
            sem_resultado = 'resultado_ia' not in st.session_state
            novo_desafio = st.session_state.get('last_processed') != st.session_state['ultimo_desafio']

            if sem_resultado or novo_desafio:
                with st.spinner("IA Intelligence Flow trabalhando..."):
                    resposta = gerar_roadmap_solucoes(st.session_state['ultimo_desafio'])
                    st.session_state['resultado_ia'] = resposta
                    st.session_state['last_processed'] = st.session_state['ultimo_desafio']

            st.markdown("---")
            st.markdown(st.session_state['resultado_ia'])
            
            if st.button("Limpar"):
                del st.session_state['solucao_gerada']
                del st.session_state['resultado_ia']
                st.rerun()
