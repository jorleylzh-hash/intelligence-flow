import streamlit as st
import pandas as pd
import random

# Função auxiliar para desenhar cards de influência
def render_driver_card(name, value, weight, correlation, explanation):
    # Lógica de cor baseada na correlação
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

def show_solutions():
    st.markdown("## 💠 Mapa de Correlação & Drivers de Preço")
    st.markdown("Selecione um ativo-alvo para mapear a rede de influências que compõe seu preço justo (Fair Value).")

    # 1. SELETOR DE ATIVO ALVO
    target_asset = st.selectbox(
        "Selecione o Ativo para Decomposição:",
        ["WIN (Índice Futuro)", "WDO (Dólar Futuro)", "PETR4 (Petrobras)", "VALE3 (Vale)"]
    )
    
    if st.button("GERAR MAPA DE INFLUÊNCIA ⚡", type="primary"):
        st.markdown("---")
        
        # LOGICA DO MAPA (SIMULAÇÃO INTELIGENTE)
        
        # === CENÁRIO 1: WIN (ÍNDICE FUTURO) ===
        if "WIN" in target_asset:
            col_main, col_drivers = st.columns([1, 2])
            
            with col_main:
                st.markdown(f"""
                <div style="text-align:center; padding:30px; background:#0f172a; border:2px solid #3b82f6; border-radius:15px; box-shadow:0 0 20px rgba(59, 130, 246, 0.3);">
                    <h1 style="color:#3b82f6; margin:0;">WIN</h1>
                    <p style="color:#94a3b8;">Índice Futuro B3</p>
                    <h2 style="color:#fff;">128.500</h2>
                    <hr style="border-color:#1e293b;">
                    <p style="font-size:0.9rem; color:#cbd5e1;">Viés Calculado:</p>
                    <div style="background:#10b981; color:white; padding:5px; border-radius:5px; font-weight:bold;">VIÉS DE ALTA LEVE</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_drivers:
                st.markdown("### 🔗 Drivers de Preço (O que move o WIN?)")
                render_driver_card(
                    "S&P 500 (EUA)", "5.230 pts (+0.4%)", "Alta Relevância", 0.85,
                    "O humor de NY dita a abertura. S&P subindo puxa fluxo comprador para Emergentes."
                )
                render_driver_card(
                    "VALE3 + PETR4", "Carteira Teórica", "Peso: ~25% do Índice", 0.90,
                    "As Blue Chips carregam o índice. Ambas positivas = Índice forte."
                )
                render_driver_card(
                    "DI1F27 (Juros Futuros)", "10.45% (-0.05%)", "Alta Relevância", -0.92,
                    "Correlação INVERSA. Juro caindo diminui custo de capital e impulsiona Bolsa."
                )

        # === CENÁRIO 2: PETR4 ===
        elif "PETR4" in target_asset:
            col_main, col_drivers = st.columns([1, 2])
            
            with col_main:
                st.markdown(f"""
                <div style="text-align:center; padding:30px; background:#0f172a; border:2px solid #f59e0b; border-radius:15px; box-shadow:0 0 20px rgba(245, 158, 11, 0.3);">
                    <h1 style="color:#f59e0b; margin:0;">PETR4</h1>
                    <p style="color:#94a3b8;">Petrobras PN</p>
                    <h2 style="color:#fff;">R$ 38,45</h2>
                    <hr style="border-color:#1e293b;">
                    <p style="font-size:0.9rem; color:#cbd5e1;">Spread de Arbitragem:</p>
                    <div style="background:#10b981; color:white; padding:5px; border-radius:5px; font-weight:bold;">+0.8% (COMPRA)</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_drivers:
                st.markdown("### 🔗 Drivers de Preço (O que move a PETR4?)")
                render_driver_card(
                    "PBR (ADR Nova York)", "US$ 15.40", "Paridade Direta", 0.99,
                    "O preço 'mãe'. O robô calcula PBR * Dólar para achar o preço justo."
                )
                render_driver_card(
                    "Petróleo Brent", "US$ 82.10 (+1.2%)", "Commodity Base", 0.70,
                    "Matéria prima sobe, receita projetada sobe. Correlação positiva forte."
                )
                render_driver_card(
                    "Risco Político (Brasília)", "Ruído Baixo Hoje", "Fator de Desconto", -0.50,
                    "Notícias sobre intervenção aumentam o deságio em relação aos pares internacionais."
                )

        # === CENÁRIO 3: WDO (DÓLAR) ===
        elif "WDO" in target_asset:
            col_main, col_drivers = st.columns([1, 2])
            
            with col_main:
                st.markdown(f"""
                <div style="text-align:center; padding:30px; background:#0f172a; border:2px solid #10b981; border-radius:15px; box-shadow:0 0 20px rgba(16, 185, 129, 0.3);">
                    <h1 style="color:#10b981; margin:0;">WDO</h1>
                    <p style="color:#94a3b8;">Dólar Futuro</p>
                    <h2 style="color:#fff;">5.015,00</h2>
                    <hr style="border-color:#1e293b;">
                    <p style="font-size:0.9rem; color:#cbd5e1;">Fluxo Cambial:</p>
                    <div style="background:#ef4444; color:white; padding:5px; border-radius:5px; font-weight:bold;">SAÍDA LÍQUIDA (ALTA)</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_drivers:
                st.markdown("### 🔗 Drivers de Preço (O que move o Dólar?)")
                render_driver_card(
                    "DXY (Dólar Global)", "104.50 (+0.3%)", "Força Global", 0.80,
                    "Se o Dólar ganha força contra Euro e Yen, tende a ganhar contra o Real."
                )
                render_driver_card(
                    "Treasuries 10Y (US)", "4.30% (+1.5%)", "Fly to Quality", 0.85,
                    "Juro americano sobe = Dinheiro sai do Brasil para os EUA = Dólar sobe."
                )
                render_driver_card(
                    "Commodities (CRB)", "Índice em Queda", "Termos de Troca", -0.60,
                    "Brasil exporta commodities. Preço baixo = Menos dólar entrando = Dólar sobe."
                )
