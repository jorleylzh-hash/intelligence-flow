# modules/data_feed.py
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO ---
# Se o MT5 não iniciar, aponte o caminho do .exe aqui (opcional)
# CAMINHO_MT5 = r"C:\Program Files\XP MetaTrader 5\terminal64.exe"

def conectar_mt5():
    """Inicia a conexão com o terminal MT5."""
    if not mt5.initialize():
        print("❌ Falha ao iniciar MT5:", mt5.last_error())
        return False
    # print("✅ Conexão MT5 estabelecida") # (Comente para não poluir o terminal)
    return True

def pegar_dados_tempo_real(ativo):
    """
    Busca o último tick (preço, bid, ask) e dados fundamentais básicos.
    Retorna um dicionário pronto para o Dashboard.
    """
    if not mt5.symbol_select(ativo, True):
        return None

    tick = mt5.symbol_info_tick(ativo)
    info = mt5.symbol_info(ativo)

    if tick is None or info is None:
        return None

    # Cálculo do Spread em Pontos
    spread = info.spread
    if "WDO" in ativo: # Ajuste para Dólar (pontos flutuantes)
        spread = (tick.ask - tick.bid)
    
    return {
        "ativo": ativo,
        "preco": tick.last,
        "bid": tick.bid,
        "ask": tick.ask,
        "spread": spread,
        "volume_real": tick.volume_real, # Volume do último negócio
        "time": datetime.fromtimestamp(tick.time).strftime('%H:%M:%S')
    }

def pegar_candles_para_indicadores(ativo, timeframe=mt5.TIMEFRAME_M5, n=100):
    """
    Busca os últimos N candles para calcular VWAP, IRR, SMC.
    Retorna um DataFrame Pandas.
    """
    rates = mt5.copy_rates_from_pos(ativo, timeframe, 0, n)
    if rates is None:
        return None
    
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df
