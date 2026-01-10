import requests
import streamlit as st

# ==============================================================================
# 🔑 COLE SUAS CHAVES AQUI (Se estiverem vazias, o sistema simula os dados)
# ==============================================================================
BRAPI_TOKEN = "8KnkXQTU5haqRDCGiAoup2"       
TWELVE_KEY = "19744b9e6e99456da5af7c626c6148d0"        
ALPHA_KEY = "VSC2ZCMUJBJGM8SF"         
# ==============================================================================

# 1. BRAPI (B3)
@st.cache_data(ttl=300)
def get_b3_tickers():
    if not BRAPI_TOKEN: return None
    tickers = "PETR4,VALE3,ITUB4,WEGE3,BOVA11"
    url = f"https://brapi.dev/api/quote/{tickers}?token={BRAPI_TOKEN}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()['results']
            results = {}
            for item in data:
                results[item['symbol']] = (item['regularMarketPrice'], item['regularMarketChangePercent'])
            return results
    except: pass
    return None

# 2. TWELVE DATA (GLOBAL)
@st.cache_data(ttl=300)
def get_global_tickers():
    if not TWELVE_KEY: return None
    symbols = "DXY,EUR/USD,IXIC" 
    url = f"https://api.twelvedata.com/price?symbol={symbols}&apikey={TWELVE_KEY}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            results = {}
            for key, val in data.items():
                results[key] = (float(val['price']), 0.0) 
            return results
    except: pass
    return None

# 3. ALPHA VANTAGE (IA NEWS)
@st.cache_data(ttl=7200) 
def get_ai_news_sentiment():
    if not ALPHA_KEY: return None
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=finance&limit=5&apikey={ALPHA_KEY}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            feed = r.json().get('feed', [])
            processed = []
            for item in feed:
                score = float(item['overall_sentiment_score'])
                label = "OTIMISTA" if score >= 0.15 else ("PESSIMISTA" if score <= -0.15 else "NEUTRO")
                color = "#10b981" if score >= 0.15 else ("#ef4444" if score <= -0.15 else "#94a3b8")
                processed.append({
                    "title": item['title'],
                    "source": item['source'],
                    "score": score,
                    "label": label,
                    "color": color,
                    "url": item['url']
                })
            return processed
    except: pass
    return None
