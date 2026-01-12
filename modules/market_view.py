import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests
import os

# --- SUAS CHAVES DO JSONBIN (Para ler no Render) ---
# Dica: No Render, o ideal é usar Environment Variables, mas para testar pode deixar hardcoded.
BIN_ID = "69646fe2ae596e708fd6049f"
API_KEY = "$2a$10$yaTm2tuNpX5.nY3IsbFx1eMZqTtLVG/6HgECo2TveCr3yCTBmvClK"

# --- MAPEAMENTO: NOME NO PAINEL -> NOME TÉCNICO ---
ASSETS_MAP = {
    # > MACRO GLOBAL (Yahoo Finance)
    'S&P500 Fut':       {'type': 'global', 'ticker': 'ES=F'},
    'Dow Jones':        {'type': 'global', 'ticker': 'YM=F'},
    'DXY (Dólar)':      {'type': 'global', 'ticker': 'DX-Y.NYB'},
    'US 10Y Yield':     {'type': 'global', 'ticker': '^TNX'},
    'Minério (Sing)':   {'type': 'global', 'ticker': 'TIO=F'},
    'EWZ (Brasil)':     {'type': 'global', 'ticker': 'EWZ'},
    
    # > ARBITRAGEM (ADRs - Yahoo Finance)
    'Vale ADR':         {'type': 'global', 'ticker': 'VALE'},
    'Petro ADR':        {'type': 'global', 'ticker': 'PBR'},
    'USD/BRL (Ref)':    {'type': 'global', 'ticker': 'BRL=X'},

    # > MERCADO LOCAL (B3 - Via JsonBin/MT5)
    # A chave 'json_key' deve ser igual ao que seu script ponte_mt5_push.py está enviando
    'WINFUT':           {'type': 'local',  'json_key': 'WIN$N'},
    'WDOFUT':           {'type': 'local',  'json_key': 'WDO$N'},
    'DI1F29':           {'type': 'local',  'json_key': 'DI1F29'},
    'VALE3':            {'type': 'local',  'json_key': 'VALE3'},
    'PETR4':            {'type': 'local',  'json_key': 'PETR4'},
    'ITUB4':            {'type': 'local',  'json_key': 'ITUB4'},
    'BBDC4':            {'type': 'local',  'json_key': 'BBDC4'},
    'BOVA11':           {'type': 'local',  'json_key': 'BOVA11'},
    'AXIA3':            {'type': 'local',  'json_key': 'AXIA3'},
    'MULT3':            {'type': 'local',  'json_key': 'MULT3'},
    'VIVA3':            {'type': 'local',  'json_key': 'VIVA3'},
    'RENT3':            {'type': 'local',  'json_key': 'RENT3'}
}

def get_data_local():
    """Baixa dados do JsonBin (Cache Rápido do MT5)"""
    url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
    headers = {'X-Master-Key': API_KEY}
    try:
        req = requests.get(url, headers=headers, timeout=3)
        if req.status_code == 200:
            # O JsonBin retorna os dados dentro de 'record'
            return req.json().get('record', {})
        else:
            print(f"Erro JsonBin: {req.status_code}")
            return {}
    except Exception as e:
        print(f"Erro Conexão Local: {e}")
        return {}

def get_data_yf():
    """Baixa dados Globais (Cache Lento)"""
    import yfinance as yf
    tickers = [v['ticker'] for k, v in ASSETS_MAP.items() if v['type'] == 'global']
    try:
        df = yf.download(tickers, period='5d', progress=False)['Close']
        return df
    except Exception as e:
        print(f"Erro YF: {e}")
        return pd.DataFrame()

def create_dashboard():
    # 1. Pega dados de ambas as fontes
    local_data = get_data_local() 
    yf_df = get_data_yf()
    
    # 2. Prepara dicionários Globais
    global_current = {}
    global_prev = {}
    if not yf_df.empty:
        global_current = yf_df.iloc[-1].to_dict()
        global_prev = yf_df.iloc[-2].to_dict()

    # Layout Dinâmico
    display_items = [k for k in ASSETS_MAP.keys() if k != 'USD/BRL (Ref)']
    total_plots = len(display_items) + 2 # +2 para Arbs
    rows = (total_plots + 1) // 2
    
    fig = make_subplots(
        rows=rows, cols=2,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}]] * rows,
        vertical_spacing=0.03, horizontal_spacing=0.05
    )

    r, c = 1, 1
    
    # Cor: Verde (Alta) / Vermelho (Baixa)
    def get_color(val, ref):
        return "#00FF7F" if val >= ref else "#FF4040"

    # --- LOOP DE ATIVOS ---
    for label in display_items:
        info = ASSETS_MAP[label]
        
        current_val = None
        prev_val = None 
        
        # BUSCA DADOS
        if info['type'] == 'local':
            # Dados vindo do MT5 via JsonBin
            # Formato esperado: {"WIN$N": {"price": 100, "prev": 99}, ...}
            key = info['json_key']
            data_item = local_data.get(key)
            
            if isinstance(data_item, dict):
                current_val = data_item.get('price')
                prev_val = data_item.get('prev')
            elif isinstance(data_item, (int, float)):
                # Fallback se vier só número
                current_val = data_item
                prev_val = data_item 

        elif info['type'] == 'global':
            ticker = info['ticker']
            if ticker in global_current:
                current_val = global_current[ticker]
                prev_val = global_prev[ticker]

        # PLOTAGEM
        if current_val is not None:
            reference = prev_val if prev_val else current_val
            min_g = reference * 0.98
            max_g = reference * 1.02
            
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=current_val,
                title={'text': label, 'font': {'size': 14, 'color': 'white'}},
                delta={'reference': reference, 'relative': True, 'valueformat': ".2%"},
                gauge={
                    'axis': {'range': [min_g, max_g], 'tickcolor': 'white'},
                    'bar': {'color': get_color(current_val, reference)},
                    'bgcolor': "rgba(0,0,0,0)",
                    'steps': [{'range': [min_g, reference], 'color': 'rgba(255,0,0,0.15)'},
                              {'range': [reference, max_g], 'color': 'rgba(0,255,0,0.15)'}]
                }
            ), row=r, col=c)
            
            c+=1; 
            if c>2: c=1; r+=1

    # --- ARBITRAGEM ---
    try:
        usd = global_current.get('BRL=X')
        
        # VALE
        vale_adr = global_current.get('VALE')
        vale_local_dict = local_data.get('VALE3') # Pegando do MT5
        vale_local = vale_local_dict.get('price') if isinstance(vale_local_dict, dict) else vale_local_dict

        if usd and vale_adr and vale_local:
            spread = (((vale_adr * usd) / vale_local) - 1) * 100
            fig.add_trace(go.Indicator(
                mode="gauge+number", value=spread,
                title={'text': "Arb VALE %", 'font': {'size': 14, 'color': 'cyan'}},
                gauge={'axis': {'range': [-2, 2]}, 'bar': {'color': 'cyan'}, 'bgcolor': "rgba(0,0,0,0)"}
            ), row=r, col=c)
            c+=1; 
            if c>2: c=1; r+=1

        # PETRO (PBR / 2 vs PETR4)
        petro_adr = global_current.get('PBR')
        petro_local_dict = local_data.get('PETR4')
        petro_local = petro_local_dict.get('price') if isinstance(petro_local_dict, dict) else petro_local_dict
        
        if usd and petro_adr and petro_local:
            spread = ((((petro_adr/2) * usd) / petro_local) - 1) * 100
            fig.add_trace(go.Indicator(
                mode="gauge+number", value=spread,
                title={'text': "Arb PETRO %", 'font': {'size': 14, 'color': 'cyan'}},
                gauge={'axis': {'range': [-2, 2]}, 'bar': {'color': 'cyan'}, 'bgcolor': "rgba(0,0,0,0)"}
            ), row=r, col=c)

    except Exception:
        pass

    fig.update_layout(
        paper_bgcolor='black', font={'color': 'white', 'family': 'Arial'},
        margin=dict(l=20, r=20, t=40, b=20),
        height=rows*150, title="<b>Intelligence Flow (M5)</b>"
    )
    return fig
