import requests
import pandas as pd
import time
import threading
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÃO JSONBIN (Sua Ponte Automática) ---
BIN_ID = "COLE_SEU_BIN_ID_AQUI"
API_KEY = "COLE_SUA_API_KEY_AQUI"

# --- CONFIGURAÇÃO DE ATIVOS MACRO (YFinance) ---
# Estes ativos serão baixados direto pela nuvem (não usam seu PC)
MACRO_TICKERS = {
    "S&P500": "ES=F",
    "DXY": "DX-Y.NYB",
    "US10Y": "^TNX",
    "Minério": "TIO=F",
    "EWZ": "EWZ",
    "VALE_ADR": "VALE"
}

# --- CACHE GLOBAL (O Segredo da Escalabilidade) ---
# A memória é compartilhada entre todos os usuários
CACHE_DADOS = {}
LOCK = threading.Lock()
LAST_UPDATE = 0
URL_PONTE_CACHE = None

def obter_url_automatica():
    """Busca o IP do seu PC no JsonBin (com cache para não estourar limite)"""
    global URL_PONTE_CACHE
    if URL_PONTE_CACHE: return URL_PONTE_CACHE
    
    try:
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
        headers = {"X-Master-Key": API_KEY}
        resp = requests.get(url, headers=headers, timeout=2)
        if resp.status_code == 200:
            URL_PONTE_CACHE = resp.json()['record']['ponte_url'].rstrip("/")
            return URL_PONTE_CACHE
    except: pass
    return None

def motor_atualizacao(ativos_mt5):
    """
    ESTA É A MÁGICA.
    Roda em segundo plano e alimenta o Cache com dados do PC + Yahoo.
    """
    global CACHE_DADOS, LAST_UPDATE
    
    novos_dados = {}
    
    # 1. BUSCA DADOS DO SEU PC (Ponte MT5)
    url = obter_url_automatica()
    if url:
        for ativo in ativos_mt5:
            try:
                r = requests.get(f"{url}/api/cotacao/{ativo}", timeout=2)
                if r.status_code == 200:
                    js = r.json()
                    if "erro" not in js:
                        novos_dados[ativo] = {
                            "preco": js['preco'],
                            "bid": js['bid'],
                            "ask": js['ask'],
                            "spread": js.get('spread', 0),
                            "origem": "MT5 Local 🏠"
                        }
            except: 
                # Se falhar, mantém o dado antigo no cache (não zera)
                pass

    # 2. BUSCA DADOS DA NUVEM (Yahoo Finance)
    # Baixa tudo de uma vez (Bulk) para ser rápido
    try:
        tickers_yf = list(MACRO_TICKERS.values())
        df = yf.download(tickers_yf, period="1d", interval="1m", progress=False)['Close']
        
        # Pega a última linha (preço atual)
        if not df.empty:
            last_row = df.iloc[-1]
            for nome_amigavel, simbolo_yf in MACRO_TICKERS.items():
                try:
                    # Lida com formato Series ou float
                    preco = float(last_row[simbolo_yf]) if isinstance(last_row, pd.Series) else float(last_row)
                    novos_dados[nome_amigavel] = {
                        "preco": preco,
                        "bid": preco, # Yahoo não dá Bid/Ask fácil em delay
                        "ask": preco,
                        "spread": 0.0,
                        "origem": "Yahoo ☁️"
                    }
                except: pass
    except Exception as e:
        print(f"Erro YF: {e}")

    # 3. ATUALIZA A MEMÓRIA GLOBAL
    if novos_dados:
        with LOCK:
            CACHE_DADOS.update(novos_dados)
            LAST_UPDATE = time.time()

def get_data_hibrido(lista_ativos_solicitados):
    """
    O usuário chama isso. Ele só LÊ o cache. Rápido e Leve.
    """
    global LAST_UPDATE
    
    # Se o cache estiver velho (> 3 seg), acorda o motor
    # (Mas não trava o usuário, roda em thread separada)
    if time.time() - LAST_UPDATE > 3.0:
        # Filtra quais ativos são do MT5 para pedir pro PC
        ativos_mt5_reais = [a for a in lista_ativos_solicitados if a not in MACRO_TICKERS]
        
        t = threading.Thread(target=motor_atualizacao, args=(ativos_mt5_reais,))
        t.start()
    
    # Entrega o que tem na memória AGORA
    resultados = {}
    with LOCK:
        for ativo in lista_ativos_solicitados:
            # Verifica se já temos no cache
            dado = CACHE_DADOS.get(ativo)
            if dado:
                resultados[ativo] = dado
            else:
                resultados[ativo] = {"preco": 0.0, "origem": "Carregando..."}
                
    return resultados
