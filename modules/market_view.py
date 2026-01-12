import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# --- CONFIGURAÇÃO DE ATIVOS (Mapeamento Nuvem/YF) ---
# Usamos sufixo .SA para B3 e tickers globais para o resto
ASSETS = {
    # GLOBAL & MACRO
    'S&P500 Fut': 'ES=F',
    'Dow Jones': 'YM=F',
    'DXY (Dólar Global)': 'DX-Y.NYB',
    'US 10Y Yield': '^TNX',
    'Minério (Singapura)': 'TIO=F',
    'EWZ (Brasil ETF)': 'EWZ',
    
    # MOEDA & ARBITRAGEM (ADRs)
    'USD/BRL': 'BRL=X',
    'Vale ADR': 'VALE',
    'Petro ADR': 'PBR',
    'Itaú ADR': 'ITUB',
    'Bradesco ADR': 'BBD',

    # MERCADO LOCAL (B3 - Atraso de 15min no YF Gratuito)
    'Ibovespa': '^BVSP',
    'Vale B3': 'VALE3.SA',
    'Petro B3': 'PETR4.SA',
    'Itaú B3': 'ITUB4.SA',
    'Bradesco B3': 'BBD4.SA',
    'BOVA11': 'BOVA11.SA',
    'AXIA3': 'AXIA3.SA',
    'MULT3': 'MULT3.SA',
    'VIVA3': 'VIVA3.SA',
    'RENT3': 'RENT3.SA'
}

def get_data():
    """Baixa dados recentes para cálculo de variação"""
    tickers = list(ASSETS.values())
    try:
        # Baixa 5 dias para garantir pegar o fechamento anterior (D-1)
        df = yf.download(tickers, period='5d', progress=False)['Close']
        return df
    except Exception as e:
        print(f"Erro YF: {e}")
        return pd.DataFrame()

def create_dashboard():
    df = get_data()
    if df.empty:
        return go.Figure().add_annotation(text="Carregando dados...", showarrow=False)

    # Último preço (Current) e Fechamento Anterior (Prev)
    curr_data = df.iloc[-1]
    prev_data = df.iloc[-2]

    # Lista de ativos para exibir (excluindo os usados apenas para cálculo se quiser)
    display_assets = [k for k in ASSETS.keys()] 
    
    # ARBITRAGEM: Adicionamos manualmente os cards de Spread
    # Spread = ((ADR * Dolar) / Local) - 1
    arbitrages = []
    try:
        usd = curr_data['BRL=X']
        
        # VALE (1:1)
        if 'VALE' in curr_data and 'VALE3.SA' in curr_data:
            spread_vale = (((curr_data['VALE'] * usd) / curr_data['VALE3.SA']) - 1) * 100
            arbitrages.append(('Arb VALE %', spread_vale))

        # PETRO (PBR = 2 ações PN aprox. Ajuste de paridade pode variar, mas usaremos 2x)
        if 'PBR' in curr_data and 'PETR4.SA' in curr_data:
            spread_petro = ((((curr_data['PBR']/2) * usd) / curr_data['PETR4.SA']) - 1) * 100
            arbitrages.append(('Arb PETRO %', spread_petro))
            
    except Exception as e:
        print(f"Erro Calc Arb: {e}")

    # Layout: Ativos + Arbitragens
    total_plots = len(display_assets) + len(arbitrages)
    rows = (total_plots + 1) // 2 
    
    fig = make_subplots(
        rows=rows, cols=2,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}]] * rows,
        vertical_spacing=0.03, horizontal_spacing=0.05
    )

    r, c = 1, 1

    # --- FUNÇÃO DE COR (Espectro Dinâmico) ---
    def get_color(val, ref):
        # Verde se subir, Vermelho se cair
        return "#00FF7F" if val >= ref else "#FF4040"

    # 1. PLOTAR ATIVOS
    for name in display_assets:
        ticker = ASSETS[name]
        if ticker in curr_data:
            val = curr_data[ticker]
            ref = prev_data[ticker]
            
            # Ajuste de escala automático (+/- 5%)
            min_gauge = ref * 0.95
            max_gauge = ref * 1.05

            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=val,
                title={'text': name, 'font': {'size': 14, 'color': 'white'}},
                delta={'reference': ref, 'relative': True, 'valueformat': ".2%"},
                gauge={
                    'axis': {'range': [min_gauge, max_gauge], 'tickcolor': "white"},
                    'bar': {'color': get_color(val, ref)},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2, 'bordercolor': "#333",
                    'steps': [
                        {'range': [min_gauge, ref], 'color': 'rgba(255, 64, 64, 0.15)'},
                        {'range': [ref, max_gauge], 'color': 'rgba(0, 255, 127, 0.15)'}
                    ],
                    'threshold': {'line': {'color': "white", 'width': 2}, 'thickness': 0.75, 'value': ref}
                },
                number={'font': {'color': 'white'}}
            ), row=r, col=c)

            c += 1
            if c > 2: c=1; r+=1

    # 2. PLOTAR ARBITRAGENS
    for name, spread in arbitrages:
        # Gauge de Arbitragem (+/- 2% de spread é o range crítico)
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=spread,
            title={'text': name, 'font': {'size': 14, 'color': 'cyan'}},
            gauge={
                'axis': {'range': [-2, 2], 'tickcolor': "white"},
                'bar': {'color': 'cyan'},
                'bgcolor': "rgba(0,0,0,0)",
                'steps': [{'range': [-0.5, 0.5], 'color': 'rgba(255,255,255,0.1)'}] # Zona Neutra
            },
            number={'suffix': "%", 'font': {'color': 'cyan'}}
        ), row=r, col=c)
        
        c += 1
        if c > 2: c=1; r+=1

    fig.update_layout(
        paper_bgcolor='black', font={'color': 'white', 'family': 'Arial'},
        margin=dict(l=20, r=20, t=40, b=20),
        height=rows * 160, # Altura dinâmica
        title="<b>Painel M5 - Intelligence Flow</b>"
    )
    
    return fig
