# backend_api/assets.py

# CONFIGURAÇÃO DE ATIVOS
# Adicione ou remova ativos aqui. O sistema lerá esta lista automaticamente.

# 1. MERCADO GLOBAL (Fonte: YFinance / Yahoo)
GLOBAL_ASSETS = [
    {"ticker": "EWZ",    "name": "EWZ (Brasil ETF)",    "type": "ETF",    "base_price": 32.50},
    {"ticker": "VALE",   "name": "Vale ADR (NYSE)",     "type": "ADR",    "base_price": 14.20},
    {"ticker": "PBR",    "name": "Petrobras ADR",       "type": "ADR",    "base_price": 15.30},
    {"ticker": "ITUB",   "name": "Itaú ADR",            "type": "ADR",    "base_price": 6.80},
    {"ticker": "BBD",    "name": "Bradesco ADR",        "type": "ADR",    "base_price": 3.20},
    {"ticker": "ES=F",   "name": "S&P 500 Fut",         "type": "INDEX",  "base_price": 4800.00},
    {"ticker": "YM=F",   "name": "Dow Jones Fut",       "type": "INDEX",  "base_price": 37500.00},
    {"ticker": "DX-Y.NYB", "name": "Dólar DXY",         "type": "FOREX",  "base_price": 102.40},
    {"ticker": "^TNX",   "name": "US Treasury 10Y",     "type": "RATES",  "base_price": 4.05},
    {"ticker": "TIO",    "name": "Iron Ore (China)",    "type": "COMM",   "base_price": 135.00},
]

# 2. MERCADO LOCAL B3 (Fonte Futura: MT5)
# "friendly_name" é o nome bonito que aparecerá no Front, escondendo o código feio.
LOCAL_ASSETS = [
    {"ticker": "DI1F29", "name": "Juros DI 2029",       "type": "RATES",  "base_price": 10.50},
    {"ticker": "VALE3",  "name": "Vale S.A.",           "type": "STOCK",  "base_price": 68.40},
    {"ticker": "PETR4",  "name": "Petrobras PN",        "type": "STOCK",  "base_price": 36.20},
    {"ticker": "ITUB4",  "name": "Itaú Unibanco",       "type": "STOCK",  "base_price": 32.10},
    {"ticker": "BBDC4",  "name": "Bradesco PN",         "type": "STOCK",  "base_price": 15.50},
    # Futuramente o MT5 preencherá isso real-time
]