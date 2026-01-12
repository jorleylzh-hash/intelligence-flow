import MetaTrader5 as mt5
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import calendar

# --- CLASSE DE AUTOMAÇÃO DE VENCIMENTOS (WDO/WIN) ---
class TickerAutomator:
    @staticmethod
    def get_vencimento_wdo():
        agora = datetime.now()
        mes_atual = agora.month
        ano_atual = agora.year
        ultimo_dia = calendar.monthrange(ano_atual, mes_atual)[1]
        
        # Regra: Vira no último dia útil (Simplificado: dia > ultimo_dia - 2)
        if agora.day >= ultimo_dia - 1:
            mes_alvo = mes_atual + 2
        else:
            mes_alvo = mes_atual + 1
            
        if mes_alvo > 12:
            mes_alvo -= 12
            ano_atual += 1
            
        letras = {1:'F', 2:'G', 3:'H', 4:'J', 5:'K', 6:'M', 7:'N', 8:'Q', 9:'U', 10:'V', 11:'X', 12:'Z'}
        return f"WDO{letras[mes_alvo]}{str(ano_atual)[-2:]}"

    @staticmethod
    def get_vencimento_win():
        agora = datetime.now()
        mes_atual = agora.month
        ano_atual = agora.year
        
        # Regra simples: Meses pares (G,J,M,Q,V,Z) vencem na quarta mais próxima do dia 15
        if mes_atual % 2 != 0: mes_alvo = mes_atual + 1
        else: mes_alvo = mes_atual # Ajustar dia 15 se precisar (simplificado)
            
        if mes_alvo > 12:
            mes_alvo -= 12
            ano_atual += 1
            
        letras = {2:'G', 4:'J', 6:'M', 8:'Q', 10:'V', 12:'Z'}
        return f"WIN{letras.get(mes_alvo, 'G')}{str(ano_atual)[-2:]}"

# --- MAPA DE ATIVOS COMPLETO ---
def get_tickers_config():
    wdo_atual = TickerAutomator.get_vencimento_wdo()
    win_atual = TickerAutomator.get_vencimento_win()
    
    return {
        # --- DERIVATIVOS B3 (MT5 - Zero Delay) ---
        "WDO":      {"source": "MT5", "symbol": wdo_atual},
        "WIN":      {"source": "MT5", "symbol": win_atual},
        "DI29":     {"source": "MT5", "symbol": "DI1F29"},
        "VXBR":     {"source": "MT5", "symbol": "VXBR"}, # Se sua corretora liberar
        
        # --- AÇÕES B3 (MT5) ---
        "PETR4":    {"source": "MT5", "symbol": "PETR4"},
        "VALE3":    {"source": "MT5", "symbol": "VALE3"},
        "ITUB4":    {"source": "MT5", "symbol": "ITUB4"},
        "AXIA3":    {"source": "MT5", "symbol": "AXIA3"}, # Antiga ELET3
        "B3SA3":    {"source": "MT5", "symbol": "B3SA3"},
        "MULT3":    {"source": "MT5", "symbol": "MULT3"}, # Correção de Milt3
        "SUZB3":    {"source": "MT5", "symbol": "SUZB3"},
        "CSAN3":    {"source": "MT5", "symbol": "CSAN3"},
        "RENT3":    {"source": "MT5", "symbol": "RENT3"},
        "MGLU3":    {"source": "MT5", "symbol": "MGLU3"},
        "VIVA3":    {"source": "MT5", "symbol": "VIVA3"},
        "LREN3":    {"source": "MT5", "symbol": "LREN3"},
        "ABEV3":    {"source": "MT5", "symbol": "ABEV3"},
        "WEGE3":    {"source": "MT5", "symbol": "WEGE3"},
        "BOVA11":   {"source": "MT5", "symbol": "BOVA11"}, # Correção de Ibova11

        # --- MACRO / INTERNACIONAL (YFinance - Nuvem) ---
        # S&P500 Futuro (ESH26)
        "SPX_FUT":  {"source": "YF", "symbol": "ES=F"}, 
        # Dow Jones Futuro (YMH26)
        "DOW_FUT":  {"source": "YF", "symbol": "YM=F"},
        # Treasury 10Y (US10YT=X)
        "US10Y":    {"source": "YF", "symbol": "^TNX"},
        # Dólar Index (DXY)
        "DXY":      {"source": "YF", "symbol": "DX-Y.NYB"},
        # Minério de Ferro (SM58Fc1 -> Proxy 62% TIO=F)
        "IRON_ORE": {"source": "YF", "symbol": "TIO=F"}, 
        
        # --- ADRs (Para Arbitragem) ---
        "EWZ":      {"source": "YF", "symbol": "EWZ"},
        "VALE_ADR": {"source": "YF", "symbol": "VALE"},
        "PBR_ADR":  {"source": "YF", "symbol": "PBR"},
        "ITUB_ADR": {"source": "YF", "symbol": "ITUB"},
        "BBD_ADR":  {"source": "YF", "symbol": "BBD"},
    }

# modules/data_feed.py

# ... imports ...

# ---------------------------------------------------------
# COLE O CAMINHO AQUI (Mantenha o 'r' antes das aspas)
# Exemplo: r"C:\Program Files\XP MetaTrader 5\terminal64.exe"
CAMINHO_MT5 = r"C:\Program Files\MetaTrader 5\terminal64.exe" 
# ---------------------------------------------------------

def conectar_mt5():
    # Tenta conectar no terminal que já estiver aberto
    if not mt5.initialize():
        print("Tentando abrir pelo caminho específico...")
        
        # Se falhar, força a abertura do executável específico da corretora
        if not mt5.initialize(path=CAMINHO_MT5):
            print(f"❌ ERRO CRÍTICO MT5: {mt5.last_error()}")
            return False
            
    # print("✅ Conectado ao MT5 com sucesso!")
    return True

def get_data_hibrido(lista_ativos):
    config_map = get_tickers_config()
    resultados = {}
    
    # 1. MT5 (Rápido)
    for user_code in lista_ativos:
        cfg = config_map.get(user_code)
        if cfg and cfg["source"] == "MT5":
            tick = mt5.symbol_info_tick(cfg["symbol"])
            if tick:
                resultados[user_code] = {
                    "preco": tick.last,
                    "var": 0.0, # Implementar cálculo de variação se desejar
                    "origem": "MT5"
                }

    # 2. YFinance (Lote)
    yf_symbols = [cfg["symbol"] for code, cfg in config_map.items() 
                  if code in lista_ativos and cfg["source"] == "YF"]
    
    if yf_symbols:
        try:
            # Baixa tudo de uma vez para não travar
            df = yf.download(yf_symbols, period="1d", interval="1m", progress=False)['Close']
            
            # Pega o último preço válido
            if not df.empty:
                last_prices = df.iloc[-1]
                for user_code in lista_ativos:
                    cfg = config_map.get(user_code)
                    if cfg and cfg["source"] == "YF":
                        sym = cfg["symbol"]
                        val = last_prices[sym] if isinstance(last_prices, pd.Series) else last_prices
                        resultados[user_code] = {
                            "preco": float(val),
                            "origem": "YF"
                        }
        except Exception as e:
            print(f"Erro YFinance: {e}")

    return resultados
