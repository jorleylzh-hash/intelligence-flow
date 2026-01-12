import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests

# --- CONFIGURAÇÕES DE ACESSO (JsonBin) ---
BIN_ID = "69646fe2ae596e708fd6049f"
API_KEY = "$2a$10$yaTm2tuNpX5.nY3IsbFx1eMZqTtLVG/6HgECo2TveCr3yCTBmvClK"

# --- MAPEAMENTO DE ATIVOS ---
# Label (Front) -> Chave Técnica (Back)
ASSETS_MAP = {
    # > GLOBAL (Yahoo Finance)
    'S&P500 Fut':       {'type': 'global', 'ticker': 'ES=F'},
    'Dow Jones':        {'type': 'global', 'ticker': 'YM=F'},
    'DXY (Dólar)':      {'type': 'global', 'ticker': 'DX-Y.NYB'},
    'US 10Y Yield':     {'type': 'global', 'ticker': '^TNX'},
    'EWZ (Brasil)':     {'type': 'global', 'ticker': 'EWZ'},
    'Minério (Sing)':   {'type': 'global', 'ticker': 'TIO=F'},

    # > ARBITRAGEM (YF - Apenas para cálculo)
    'Vale ADR':         {'type': 'global', 'ticker': 'VALE'},
    'Petro ADR':        {'type': 'global', 'ticker': 'PBR'},
    'USD/BRL':          {'type': 'global', 'ticker': 'BRL=X'},

    # > LOCAL (B3 - Vindo do seu MT5 via JsonBin)
    # A chave 'json_key' DEVE ser igual ao que está no seu ponte_mt5_push.py
    'WINFUT':           {'type': 'local', 'json_key': 'WIN$N'},
    'WDOFUT':           {'type': 'local', 'json_key': 'WDO$N'},
    'DI1F29':           {'type': 'local', 'json_key': 'DI1F29'},
    'VALE3':            {'type': 'local', 'json_key': 'VALE3'},
    'PETR4':            {'type': 'local', 'json_key': 'PETR4'},
    'ITUB4':            {'type': 'local', 'json_key': 'ITUB4'},
    'BBDC4':            {'type': 'local', 'json_key': 'BBDC4'},
    'BOVA11':           {'type': 'local', 'json_key': 'BOVA11'},
    'AXIA3':            {'type': 'local', 'json_key': 'AXIA3'},
    'MULT3':            {'type': 'local', 'json_key': 'MULT3'},
    'VIVA3':            {'type': 'local', 'json_key': 'VIVA3'},
    'RENT3':            {'type': 'local', 'json_key': 'RENT3'}
}

def get_local_data():
    """Baixa o JSON enviado pelo seu MT5"""
    url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
    headers = {'X-Master-Key': API_KEY}
    try:
        # Timeout curto para não travar o dashboard
        r = requests.get(url, headers=headers, timeout=2.5)
        if r.status_code == 200:
            return r.json().get('record', {})
        return {}
    except Exception:
        return {}

def get_global_data():
    """Baixa dados do Yahoo Finance"""
    import yfinance as yf
    tickers = [v['ticker'] for k, v in ASSETS_MAP.items() if v['type'] == 'global']
    try:
        # Baixa apenas o necessário
        df = yf.download(tickers, period='5d', progress=False)['Close']
        if df.empty: return {}, {}
        
        # Pega último preço (Current) e Penúltimo (Prev)
        return df.iloc[-1].to_dict(), df.iloc[-2].to_dict()
    except Exception:
        return {}, {}

def create_dashboard():
    # 1. Coleta Dados
    local_data = get_local_data()
    global_curr, global_prev = get_global_data()

    # 2. Configura Layout (Linhas e Colunas)
    display_assets = [k for k in ASSETS_MAP.keys() if k not in ['Vale ADR', 'Petro ADR', 'USD/BRL']]
    total_plots = len(display_assets) + 2 # +2 para os Arbs
    rows = (total_plots + 1) // 2

    fig = make_subplots(
        rows=rows, cols=2,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}]] * rows,
        vertical_spacing=0.04, horizontal_spacing=0.05
    )

    # 3. Função de Cor (Verde/Vermelho)
    def get_color(val, ref):
        return "#00FF7F" if val >= ref else "#FF4040"

    r, c = 1, 1

    # --- LOOP DOS ATIVOS ---
    for label in display_assets:
        conf = ASSETS_MAP[label]
        curr, prev = None, None

        # Lógica de Extração
        if conf['type'] == 'local':
            key = conf['json_key']
            item = local_data.get(key)
            # Suporta formato {"price": 10, "prev": 9} ou direto 10
            if isinstance(item, dict):
                curr = item.get('price')
                prev = item.get('prev')
            elif isinstance(item, (int, float)):
                curr = item
                prev = item # Sem variação se não tiver histórico
        
        elif conf['type'] == 'global':
            ticker = conf['ticker']
            if ticker in global_curr:
                curr = global_curr[ticker]
                prev = global_prev.get(ticker, curr)

        # Plotagem
        if curr is not None:
            ref = prev if prev else curr
            min_g = ref * 0.98
            max_g = ref * 1.02
            
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=curr,
                title={'text': label, 'font': {'size': 14, 'color': 'white'}},
                delta={'reference': ref, 'relative': True, 'valueformat': ".2%"},
                gauge={
                    'axis': {'range': [min_g, max_g], 'tickcolor': 'white'},
                    'bar': {'color': get_color(curr, ref)},
                    'bgcolor': "rgba(0,0,0,0)",
                    'steps': [{'range': [min_g, ref], 'color': 'rgba(255,0,0,0.1)'},
                              {'range': [ref, max_g], 'color': 'rgba(0,255,0,0.1)'}]
                }
            ), row=r, col=c)
            
            c += 1
            if c > 2: c=1; r+=1

    # --- CÁLCULO DE ARBITRAGEM ---
    # Spread = ((ADR * USD) / Local - 1) * 100
    try:
        usd = global_curr.get('BRL=X')
        
        # VALE
        adr_v = global_curr.get('VALE')
        # Tenta pegar valor local (suporta dict ou float)
        loc_v_raw = local_data.get('VALE3')
        loc_v = loc_v_raw.get('price') if isinstance(loc_v_raw, dict) else loc_v_raw
        
        if usd and adr_v and loc_v:
            spread = (((adr_v * usd) / loc_v) - 1) * 100
            fig.add_trace(go.Indicator(
                mode="gauge+number", value=spread,
                title={'text': "Arb VALE %", 'font': {'size': 14, 'color': 'cyan'}},
                gauge={'axis': {'range': [-2, 2]}, 'bar': {'color': 'cyan'}, 'bgcolor': "rgba(0,0,0,0)"}
            ), row=r, col=c)
            c += 1
            if c > 2: c=1; r+=1

        # PETRO (PBR / 2 vs PETR4)
        adr_p = global_curr.get('PBR')
        loc_p_raw = local_data.get('PETR4')
        loc_p = loc_p_raw.get('price') if isinstance(loc_p_raw, dict) else loc_p_raw

        if usd and adr_p and loc_p:
            spread = ((((adr_p/2) * usd) / loc_p) - 1) * 100
            fig.add_trace(go.Indicator(
                mode="gauge+number", value=spread,
                title={'text': "Arb PETRO %", 'font': {'size': 14, 'color': 'cyan'}},
                gauge={'axis': {'range': [-2, 2]}, 'bar': {'color': 'cyan'}, 'bgcolor': "rgba(0,0,0,0)"}
            ), row=r, col=c)

    except Exception:
        pass

    fig.update_layout(
        paper_bgcolor='black', font={'color': 'white', 'family': 'Arial'},
        margin=dict(l=20, r=20, t=30, b=20),
        height=rows*150,
        title="<b>Intelligence Flow (M5)</b>"
    )
    return fig
