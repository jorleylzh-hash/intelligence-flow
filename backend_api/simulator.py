import random
import pandas as pd
from datetime import datetime, timedelta
from assets import GLOBAL_ASSETS, LOCAL_ASSETS

def calculate_rsi(prices, periods=9):
    if len(prices) < periods: return 50
    deltas = pd.Series(prices).diff()
    gain = (deltas.where(deltas > 0, 0)).rolling(window=periods).mean()
    loss = (-deltas.where(deltas < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return round(100 - (100 / (1 + rs.iloc[-1])), 2)

def generate_advanced_data(ticker, base_price):
    points = 30
    history = []
    current_price = base_price
    sum_pv = 0
    sum_vol = 0
    
    for i in range(points):
        variation = random.uniform(-0.002, 0.002)
        current_price *= (1 + variation)
        volume = random.randint(1000, 5000)
        
        # Cálculo de VWAP
        sum_pv += current_price * volume
        sum_vol += volume
        vwap = sum_pv / sum_vol
        
        history.append({
            "time": (datetime.now() - timedelta(minutes=points-i)).strftime("%H:%M"),
            "price": round(current_price, 2),
            "vwap": round(vwap, 2),
            "volume": volume
        })
    
    prices = [h["price"] for h in history]
    return {
        "history": history,
        "rsi": calculate_rsi(prices),
        "vwap": history[-1]["vwap"],
        "last_vol": history[-1]["volume"]
    }

def get_simulated_data():
    market_snapshot = []
    all_assets = GLOBAL_ASSETS + LOCAL_ASSETS
    
    # Cache simples para arbitragem
    prices_cache = {}

    for asset in all_assets:
        adv = generate_advanced_data(asset["ticker"], asset["base_price"])
        prices_cache[asset["ticker"]] = adv["history"][-1]["price"]
        
        market_snapshot.append({
            **asset,
            "price": adv["history"][-1]["price"],
            "trend": "bullish" if adv["history"][-1]["price"] > asset["base_price"] else "bearish",
            "variation": f"{((adv['history'][-1]['price']/asset['base_price'])-1)*100:.2f}%",
            "history": adv["history"],
            "vwap": adv["vwap"],
            "rsi": adv["rsi"],
            "volume": adv["last_vol"]
        })

    # Cálculo de Arbitragem (VALE3 vs VALE ADR)
    # Supondo Dólar fixo em 5.00 para o cálculo de Gap
    usd_brl = 5.00 
    if "VALE3" in prices_cache and "VALE" in prices_cache:
        vale_adr_brl = prices_cache["VALE"] * usd_brl
        gap = ((vale_adr_brl / prices_cache["VALE3"]) - 1) * 100
        for a in market_snapshot:
            if a["ticker"] == "VALE3": a["arbitrage_gap"] = f"{gap:.2f}%"

    return market_snapshot