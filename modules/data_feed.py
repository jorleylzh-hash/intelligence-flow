import requests
import pandas as pd
# Tenta importar MT5 só pra não quebrar, mas não usa
try: import MetaTrader5 as mt5 
except: pass

# --- 🔒 SUAS CHAVES DO JSONBIN (AS MESMAS DO PC) ---
BIN_ID = "69646fe2ae596e708fd6049f"
API_KEY = "$2a$10$yaTm2tuNpX5.nY3IsbFx1eMZqTtLVG/6HgECo2TveCr3yCTBmvClK" 
# ---------------------------------------------------

def obter_url_automatica():
    """Lê o cofre digital para descobrir onde está o PC"""
    try:
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
        headers = {"X-Master-Key": API_KEY}
        resp = requests.get(url, headers=headers, timeout=3)
        if resp.status_code == 200:
            return resp.json()['record']['ponte_url']
    except:
        return None

def get_data_hibrido(lista_ativos, url_ponte=None):
    resultados = {}
    
    # 1. Se não veio link manual, busca no cofre automático
    if not url_ponte:
        url_ponte = obter_url_automatica()

    if url_ponte:
        url_ponte = url_ponte.rstrip("/")

    for ativo in lista_ativos:
        dados = None
        if url_ponte:
            try:
                # Tenta conectar no PC
                resp = requests.get(f"{url_ponte}/api/cotacao/{ativo}", timeout=3)
                if resp.status_code == 200:
                    js = resp.json()
                    if "erro" not in js:
                        dados = {
                            "preco": js['preco'], "bid": js['bid'], "ask": js['ask'],
                            "spread": js.get('spread', 0), "origem": "Conexão Auto 🟢"
                        }
            except: pass
        
        if dados:
            resultados[ativo] = dados
        else:
            resultados[ativo] = {"preco": 0.0, "origem": "Buscando Sinal... 📡"}

    return resultados
