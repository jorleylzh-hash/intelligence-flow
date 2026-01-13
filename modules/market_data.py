import requests
import pandas as pd
import yfinance as yf
import random
from concurrent.futures import ThreadPoolExecutor

# Monitoramento NYSE/B3
ASSETS_CONFIG = {
    'WINFUT': {'type': 'local', 'key': 'WIN$N'},
    'WDOFUT': {'type': 'local', 'key': 'WDO$N'},
    'S&P500': {'type': 'global', 'key': 'ES=F'},
    'DXY':    {'type': 'global', 'key': 'DX-Y.NYB'},
    'VALE3':  {'type': 'local', 'key': 'VALE3'},
    'PETR4':  {'type': 'local', 'key': 'PETR4'},
    'ITUB4':  {'type': 'local', 'key': 'ITUB4'},
    'BBDC4':  {'type': 'local', 'key': 'BBDC4'},
    'EWZ':    {'type': 'global', 'key': 'EWZ'},
    '10Y Yield': {'type': 'global', 'key': '^TNX'},
    'VALE_ADR': {'type': 'global', 'key': 'VALE', 'hidden': True},
    'PETR_ADR': {'type': 'global', 'key': 'PBR', 'hidden': True},
    'USD_BRL':  {'type': 'global', 'key': 'BRL=X', 'hidden': True}
}

BIN_ID = "69646fe2ae596e708fd6049f"
API_KEY = "$2a$10$yaTm2tuNpX5.nY3IsbFx1eMZqTtLVG/6HgECo2TveCr3yCTBmvClK"

def fetch_local():
    try:
        r = requests.get(f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest", 
                         headers={'X-Master-Key': API_KEY}, timeout=2)
        return r.json().get('record', {}) if r.status_code == 200 else {}
    except: return {}

def fetch_global():
    tickers = [v['key'] for k,v in ASSETS_CONFIG.items() if v['type'] == 'global']
    try:
        return yf.download(tickers, period='2d', progress=False, threads=True, timeout=5)
    except: return pd.DataFrame()

def get_data():
    with ThreadPoolExecutor(max_workers=2) as executor:
        f_local = executor.submit(fetch_local)
        f_global = executor.submit(fetch_global)
        local_raw, global_df = f_local.result(), f_global.result()

    final_data = {}
    data_found = bool(local_raw or not global_df.empty)
    
    if not data_found:
        for label in ASSETS_CONFIG.keys():
            final_data[label] = {'curr': 100.0 + random.uniform(-1, 1), 'prev': 100.0, 'hidden': ASSETS_CONFIG[label].get('hidden', False)}
        final_data['_META'] = {'status': 'SIMULATOR'}
        return final_data

    for label, conf in ASSETS_CONFIG.items():
        curr, prev = None, None
        if conf['type'] == 'local':
            item = local_raw.get(conf['key'])
            if isinstance(item, dict):
                curr, prev = item.get('price'), item.get('prev')
        elif conf['type'] == 'global' and not global_df.empty:
            try:
                key = conf['key']
                if 'Close' in global_df.columns and key in global_df['Close'].columns:
                    series = global_df['Close'][key].dropna()
                    if len(series) >= 2: curr, prev = series.iloc[-1], series.iloc[-2]
            except: pass
        final_data[label] = {'curr': curr, 'prev': prev, 'hidden': conf.get('hidden', False)}
    
    final_data['_META'] = {'status': 'LIVE ON'}
    return final_data