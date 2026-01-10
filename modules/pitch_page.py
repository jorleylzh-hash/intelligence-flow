import streamlit as st
from streamlit_lottie import st_lottie
import requests

# --- CONFIGURAÇÃO DE ASSETS (Lottie Animations) ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- CSS PROFISSIONAL (LANDING PAGE STYLE) ---
def apply_pitch_css():
    st.markdown("""
    <style>
        /* Tipografia e Fundo */
        .stApp { background-color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
        h1, h2, h3 { color: #0f172a; font-weight: 700; }
        p { color: #475569; font-size: 1.1rem; line-height: 1.6; }
        
        /* Destaques de Texto */
        .highlight-blue { color: #2563eb; font-weight: bold; }
        .highlight-green { color: #059669; font-weight: bold; }
        
        /* Cards de Benefício (Efeito Glass/Shadow) */
        .benefit-card {
            background: #ffffff;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #2563eb;
            transition: transform 0.3s ease;
            margin-bottom: 20px;
        }
        .benefit-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }
        
        /* Seção Swing Trade (Cor Diferente) */
        .swing-card {
            border-left: 5px solid #059669; /* Verde para Swing/Estrutura */
        }

        /* Botão CTA Falso (Estilo) */
        .cta-box {
            background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            margin-top: 50px;
        }
    </style>
    """, unsafe_allow_html=True)

def show_pitch():
    apply_pitch_css()
    
    # Carregando Animações Contextuais
    anim_sniper = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_3rw3X4.json") # Target/Sniper
    anim_strategy = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_qmfs6c3i.json") # Growing Chart/Strategy
    anim_network = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_w51pcehl.json") # Global Connection

    # --- 1. HERO SECTION (A PROMESSA) ---
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">
            Não opere o Gráfico.<br><span class="highlight-blue">Opere o Contexto.</span>
        </h1>
        <p style="font-size: 1.3rem; max-width: 800px; margin: 0 auto;">
            A Intelligence Flow não entrega apenas dados. Entregamos a <b>visão privilegiada</b> que os grandes players usam para antecipar movimentos.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # --- 2. PERFILS DE TRADER (ZIG-ZAG LAYOUT) ---
    
    # === PERFIL DAY TRADER (M5) ===
    c1, c2 = st.columns([1, 1.2])
    
    with c1:
        if anim_sniper:
            st_lottie(anim_sniper, height=350, key="anim_day")
    
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="benefit-card">
            <h2 style="color: #2563eb;">⚡ Para o Day Trader (M5)</h2>
            <h3 style="font-size: 1.2rem; color: #64748b;">O Radar de Antecipação</h3>
            <p>
                No gráfico de 5 minutos, cada segundo conta. Você não pode ser pego por uma "violinada".
                <br><br>
                ✅ <b>O Espelho do Futuro:</b> O EWZ (ETF Brasil em NY) muitas vezes antecipa o movimento do Índice em até 2 minutos. Veja o futuro antes dele acontecer no gráfico.
                <br>
                ✅ <b>Arbitragem HFT:</b> Identifique Gaps de preço entre PETR4 e ADRs. Entre exatamente quando os robôs institucionais entram para fechar o spread.
                <br><br>
                <i>"A plataforma responde: O fluxo global apoia o meu clique agora?"</i>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # === PERFIL SWING TRADER (D1) ===
    c3, c4 = st.columns([1.2, 1])
    
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="benefit-card swing-card">
            <h2 style="color: #059669;">📅 Para o Swing Trader</h2>
            <h3 style="font-size: 1.2rem; color: #64748b;">A Bússola de Navegação</h3>
            <p>
                Você busca tendências estruturais. O perigo é comprar um ativo "barato" quando o ciclo macroeconômico virou para venda.
                <br><br>
                ✅ <b>Validação de Tendência:</b> O gráfico diz compra, mas o Minério na China perdeu fundo? A Intelligence Flow te salva de entrar na hora errada.
                <br>
                ✅ <b>Risco Sistêmico:</b> Monitore os Treasuries (Juros EUA). Se eles sobem, o capital sai da Bolsa. Proteja sua carteira antes da queda.
                <br><br>
                <i>"A plataforma responde: O cenário macro sustenta essa posição por semanas?"</i>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        if anim_strategy:
            st_lottie(anim_strategy, height=350, key="anim_swing")

    st.markdown("---")

    # --- 3. COMPARATIVO VISUAL ---
    st.markdown("<h2 style='text-align:center;'>O Impacto da Tecnologia</h2>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("""
        <div style="background:#e0f2fe; padding:20px; border-radius:10px; text-align:center;">
            <h3 style="color:#0369a1;">Trader Comum</h3>
            <p style="font-size:0.9rem;">Analisa apenas o Preço (Passado).</p>
            <h1 style="color:#64748b;">📉</h1>
            <p style="font-size:0.9rem;">Reage atrasado aos movimentos.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_b:
        if anim_network:
            st_lottie(anim_network, height=180, key="center_anim")
            
    with col_c:
        st.markdown("""
        <div style="background:#dcfce7; padding:20px; border-radius:10px; text-align:center;">
            <h3 style="color:#15803d;">Trader Intelligence</h3>
            <p style="font-size:0.9rem;">Analisa o Fluxo (Presente).</p>
            <h1 style="color:#15803d;">🚀</h1>
            <p style="font-size:0.9rem;">Antecipa movimentos via Arbitragem.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- 4. CALL TO ACTION (CTA) ---
    st.markdown("""
    <div class="cta-box">
        <h2>Pronto para elevar seu nível operacional?</h2>
        <p style="color: #cbd5e1; margin-bottom: 20px;">Acesse agora a Área do Trader e veja esses dados em tempo real.</p>
        <p style="font-size: 0.9rem; color: #94a3b8;">Use o menu lateral para fazer Login 🔐</p>
    </div>
    """, unsafe_allow_html=True)