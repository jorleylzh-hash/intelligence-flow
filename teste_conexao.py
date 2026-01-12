import MetaTrader5 as mt5
import time

# Cole o mesmo caminho aqui também para testar
CAMINHO = r"C:\Program Files\XP MetaTrader 5\terminal64.exe"

print("1. Iniciando conexão...")
if not mt5.initialize(path=CAMINHO):
    print("❌ Falha na inicialização")
    mt5.shutdown()
else:
    print("✅ Conexão estabelecida!")
    
    # Teste de dados
    print("2. Verificando PETR4...")
    symbol = "PETR4"
    if mt5.symbol_select(symbol, True):
        tick = mt5.symbol_info_tick(symbol)
        print(f"   Preço PETR4: {tick.last}")
        print(f"   Ask: {tick.ask} | Bid: {tick.bid}")
    else:
        print("   ❌ Não encontrei PETR4 (Verifique se está no Market Watch)")

    print("3. Teste concluído. Desconectando...")
    mt5.shutdown()
