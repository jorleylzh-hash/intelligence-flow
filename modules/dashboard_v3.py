import streamlit as st
import pandas as pd

# --- ESTILIZAÇÃO CSS AVANÇADA (DARK MODE PREMIUM) ---
def apply_styles():
    st.markdown("""
    <style>
        /* Fundo Geral */
        .stApp { background-color: #050505; }
        
        /* Tipografia */
        h1, h2, h3 { color: #ffffff; font-family: 'Helvetica Neue', sans-serif; font-weight: 300; }
        p { color: #b0b3b8; font-size: 16px; line-height: 1.6; }
        
        /* Container Hero */
        .hero-box {
            background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 100%);
            padding: 60px 40px;
            border-radius: 0px 0px 20px 20px;
            margin-bottom: 40px;
            text-align: center;
            border-bottom: 4px solid #3b82f6;
        }
        .hero-title { font-size: 48px; font-weight: 700; color: #fff; letter-spacing: -1px; margin-bottom: 10px; }
        .hero-sub { font-size: 20px; color: #93c5fd; max-width: 800px; margin: 0 auto; }

        /* Cards de Conceito */
        .feature-card {
            background-color: #111; 
            padding: 30px; 
            border-radius: 15px; 
            border: 1px solid #333;
            height: 100%;
            transition: all 0.3s ease;
        }
        .feature-card:hover { border-color: #3b82f6; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(59, 130, 246, 0.1); }
        .card-icon { font-size: 40px; margin-bottom: 15px; }
        .card-title { font-size: 22px; font-weight: 600; color: #fff; margin-bottom: 10px; }
        .card-text { font-size: 14px; color: #888; }
        
        /* Destaques (Arbitragem) */
        .highlight-box {
            background-color: #1e293b;
            border-left: 5px solid #10b981;
            padding: 20px;
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# AQUI ESTÁ A FUNÇÃO QUE O SEU ERRO DIZ QUE FALTA:
def show_landing_page():
    apply_styles()
    
    # 1. HERO SECTION (Impacto Visual)
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">INTELLIGENCE FLOW</div>
        <div class="hero-sub">Plataforma Institucional de Monitoramento Macroquantitativo & Arbitragem de Alta Frequência</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. CONCEITOS MACRO (Imagens e Explicação)
    st.markdown("## 🌐 A Dinâmica dos Mercados Globais")
    st.markdown("O mercado financeiro não é aleatório. Ele segue fluxos de capital ditados por juros, risco e correlações.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="card-icon">🇺🇸 vs 🇧🇷</div>
            <div class="card-title">B3 vs. NYSE: Quem manda?</div>
            <p class="card-text">
                O Brasil é um mercado emergente. O volume financeiro da nossa bolsa (B3) é uma fração do mercado americano (NYSE).
                <br><br>
                <b>A Tese:</b> O fluxo estrangeiro dita a tendência do IBOV. Monitoramos o <b>EWZ</b> (ETF do Brasil em Nova York) 
                para antecipar movimentos locais. Se o gringo vende lá fora, o preço cai aqui minutos depois.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        # Imagem ilustrativa de mercado
        st.image("https://images.unsplash.com/photo-1611974765270-ca1258634369?q=80&w=1000&auto=format&fit=crop", 
                 use_container_width=True)

    st.markdown("---")

    # 3. ARBITRAGEM E GAPS (A parte técnica explicada)
    st.markdown("## ⚡ O Conceito de Arbitragem e GAP")
    
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="card-title">1. Ativos Espelhados</div>
            <p class="card-text">
                Empresas como Petrobras e Vale são negociadas em Reais (R$) no Brasil e em Dólares (US$) nos EUA (ADRs).
                Matematicamente, elas representam a mesma empresa.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="card-title">2. A Paridade</div>
            <p class="card-text">
                O preço deve ser igual. A fórmula básica é:<br>
                <code>Preço BR = Preço NY * Dólar</code><br>
                Se o Dólar sobe, a ação no Brasil deveria subir para compensar.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card" style="border-color: #10b981;">
            <div class="card-title">3. O GAP de Lucro</div>
            <p class="card-text">
                Quando essa conta não fecha, surge um <b>GAP de Arbitragem</b>. Robôs HFT compram onde está barato e vendem onde está caro.
                Nossa plataforma identifica esses momentos em tempo real.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    # Exemplo Visual
    st.markdown("""
    <div class="highlight-box">
        <h3 style="margin:0; font-size:18px; color:#fff;">📐 Exemplo Prático de Correlação:</h3>
        <p style="margin-top:10px; color:#cbd5e1;">
        Se o <b>Minério de Ferro</b> cai na China e o <b>Dólar</b> cai no mundo (DXY), é matematicamente provável que a <b>VALE3</b> sofra pressão vendedora, 
        independentemente do gráfico técnico. Operamos fluxo e fundamento, não apenas preço.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 4. RODAPÉ DE AUTORIDADE
    st.markdown("## 🚀 Por que Intelligence Flow?")
    cols = st.columns(4)
    cols[0].metric("Latência", "Low Latency", "10ms")
    cols[1].metric("Dados", "NYSE & B3", "Real-Time")
    cols[2].metric("Modelos", "Quantitativos", "Proprietários")
    cols[3].metric("Foco", "Institucional", "Day Trade")
    
    st.markdown("<br><br><div style='text-align:center; color:#555;'>Intelligence Flow Solutions © 2026 • Tecnologia para Alta Performance</div>", unsafe_allow_html=True)
