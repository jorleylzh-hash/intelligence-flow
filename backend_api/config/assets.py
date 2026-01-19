# IntelligenceFlow/backend_api/config/assets.py

# --- ATIVOS PARA MONITORAMENTO RÁPIDO (CARD DASHBOARD) ---
# Estes aparecem na tela principal.
MONITORED_TICKERS = [
    "PETR4.SA", 
    "VALE3.SA", 
    "ITUB4.SA", 
    "BBDC4.SA", 
    "EWZ", 
    "DX-Y.NYB"
]

# --- MENU GERAL DO SISTEMA (IA) ---
# A IA pode escolher qualquer um destes para correlacionar no gráfico.
SYSTEM_ASSETS_FULL_LIST = [
    # B3 (Brasil)
    "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "^BVSP", "BRL=X",
    
    # NYSE/US (Estados Unidos)
    "EWZ", "SPY", "QQQ", "IWM", "XLF", # ETFs Setoriais
    "AAPL", "MSFT", "NVDA",            # Tech
    
    # Commodities & Futuros (Global)
    "CL=F", # Petróleo WTI
    "GC=F", # Ouro
    "SI=F", # Prata
    "HG=F", # Cobre
    
    # Macroeconomia
    "DX-Y.NYB", # Dólar Index (DXY)
    "^TNX",     # Treasury 10Y (Juros Longos)
    "^VIX",     # Índice do Medo
    "BTC-USD"   # Bitcoin
]

# --- MAPA DE TRADUÇÃO (INTELLIGENCE LAYER) ---
# O Yahoo Finance não reconhece códigos de futuros da B3 (WING26, WDOG26).
# Aqui definimos o "Proxy" (Ativo Equivalente) para baixar o gráfico.
YAHOO_TRANSLATION_MAP = {
    # Índice Futuro -> Ibovespa
    "WING26": "^BVSP",
    "WIN": "^BVSP",
    "IND": "^BVSP",
    
    # Dólar Futuro -> Dólar/Real
    "WDOG26": "BRL=X",
    "WDO": "BRL=X",
    "DOL": "BRL=X",
    
    # Juros Futuros (DI) -> Treasury 10Y (Melhor proxy de correlação global)
    "DI": "^TNX",
    "DI1F29": "^TNX" 
}