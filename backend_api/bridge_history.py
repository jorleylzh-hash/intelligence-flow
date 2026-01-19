import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import MarketHistory, Base

# --- CONFIGURAÇÃO DE AMBIENTE ---
load_dotenv()

# 1. Configuração de Banco
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# 2. Configuração dos Caminhos (AGORA VIA .ENV)
PATH_MT5_LOCAL = os.getenv("MT5_PATH_LOCAL")
PATH_MT5_GLOBAL = os.getenv("MT5_PATH_GLOBAL")

# LISTA DE ATIVOS
ASSETS_LOCAL = ["PETR4", "VALE3", "ITUB4", "WIN$N", "WDO$N"] 
ASSETS_GLOBAL = ["PBR.A.US", "VALE.P.US", "USDIndMar26", "EURUSD", "ITUB.US"] 

# ==============================================================================

def sync_terminal(path_exe, assets, source_name):
    # Validação de Segurança
    if not path_exe or not os.path.exists(path_exe):
        print(f"\n❌ ERRO FATAL: Caminho do {source_name} não encontrado ou inválido.")
        print(f"   -> Verifique a variável no .env: {path_exe}")
        return

    print(f"\n🔌 [{source_name}] Tentando conectar em: {path_exe}...")
    
    # Inicializa Terminal
    if not mt5.initialize(path=path_exe):
        print(f"❌ Falha ao iniciar {source_name}: {mt5.last_error()}")
        return

    print(f"✅ {source_name} Conectado! Iniciando download...")
    total_inserted_session = 0
    
    for symbol in assets:
        print(f"   🔎 Processando ativo: {symbol}...", end="\r")
        
        if not mt5.symbol_select(symbol, True):
            print(f"   ⚠️  Ativo {symbol} não encontrado/disponível no {source_name}.       ")
            continue

        # Baixa 5000 velas (~17 dias em M5)
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 5000)
        
        if rates is None or len(rates) == 0:
            print(f"   ⚠️  Sem dados históricos para {symbol}.                           ")
            continue

        # Converte e Prepara
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Otimização: Descobre quais já existem para não tentar inserir
        existing_times = db.query(MarketHistory.time).filter(
            MarketHistory.ticker == symbol
        ).all()
        existing_times_set = {row[0] for row in existing_times}

        new_candles = []
        for index, row in df.iterrows():
            if row['time'] not in existing_times_set:
                new_candles.append({
                    "ticker": symbol,
                    "time": row['time'],
                    "open": float(row['open']),
                    "high": float(row['high']),
                    "low": float(row['low']),
                    "close": float(row['close']),
                    "volume": float(row['tick_volume']),
                    "source": source_name
                })
        
        # Bulk Insert
        if new_candles:
            db.bulk_insert_mappings(MarketHistory, new_candles)
            db.commit()
            total_inserted_session += len(new_candles)
            print(f"   📥 {symbol}: +{len(new_candles)} novas velas gravadas.                ")
        else:
            print(f"   ok {symbol}: Já está atualizado.                                      ")

    print(f"💾 FIM DA SESSÃO {source_name}. Total gravado: {total_inserted_session} registros.")
    mt5.shutdown() 
    print(f"🔌 {source_name} Desconectado.\n")
    time.sleep(2) 

# --- EXECUÇÃO ---
if __name__ == "__main__":
    print("="*60)
    print("🚀 INTELLIGENCE FLOW - HISTORICAL DATA SYNC (ENV CONFIG)")
    print("="*60)

    # Executa com base nas variáveis carregadas do .env
    sync_terminal(PATH_MT5_LOCAL, ASSETS_LOCAL, "MT5_LOCAL")
    sync_terminal(PATH_MT5_GLOBAL, ASSETS_GLOBAL, "MT5_GLOBAL")

    print("\n✅ Sincronização Completa!")