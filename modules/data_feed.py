import requests
import streamlit as st
import pandas as pd

# ==============================================================================
# 🔑 ÁREA DE CHAVES DE API (COLE SUAS CHAVES AQUI)
# ==============================================================================
BRAPI_TOKEN = "8KnkXQTU5haqRDCGiAoup2"       # Ex: "woeiruo234..."
TWELVE_KEY = "19744b9e6e99456da5af7c626c6148d0"         # Ex: "8374823..."
ALPHA_KEY = "VSC2ZCMUJBJGM8SF"           # Ex: "K3J4..."
# ==============================================================================

# 1. BRAPI (B3 - Ações Brasileiras)
# Documentação Free: Cotação atual com 15-30min delay (padrão free)
@st.cache_data(ttl=300) # Cache de 5 min para economizar créditos
def get_b3_tickers():
    if "COLE_SEU" in BRAPI_TOKEN: return None # Proteção se não configurar
    
    tickers = "PETR4,VALE3,ITUB4,WEGE3,BOVA11"
    url = f"https://brapi.dev/api/quote/{tickers}?token={BRAPI_TOKEN}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()['results']
            results = {}
            for item in data:
                symbol = item['symbol']
                price = item['regularMarketPrice']
                change = item['regularMarketChangePercent']
                results[symbol] = (price, change)
            return results
    except:
        pass
    return None

# 2. TWELVE DATA (Global - Forex & Índices)
# Free Plan: 8 requests/minuto
@st.cache_data(ttl=300)
def get_global_tickers():
    if "COLE_SUA" in TWELVE_KEY: return None
    
    # Symbols: DXY (Index), EUR/USD, IXIC (Nasdaq)
    symbols = "DXY,EUR/USD,IXIC" 
    url = f"https://api.twelvedata.com/price?symbol={symbols}&apikey={TWELVE_KEY}"
    
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            # A Twelve Data retorna JSON diferente dependendo da qtd, normalizamos aqui:
            results = {}
            # Simulação de variação (A API Free básica só dá preço, calcamos variação fictícia para UI)
            # Para variação real no Free, precisaria de endpoint 'quote', que consome mais créditos.
            for key, val in data.items():
                price = float(val['price'])
                results[key] = (price, 0.0) 
            return results
    except:
        pass
    return None

# 3. ALPHA VANTAGE (IA - Sentiment Analysis)
# Free Plan: 25 requests/DIA (Muito limitado, usaremos cache longo de 2 horas)
@st.cache_data(ttl=7200) 
def get_ai_news_sentiment():
    if "COLE_SUA" in ALPHA_KEY: return None
    
    # Busca notícias sobre Mercado Financeiro com Sentimento
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=finance&limit=5&apikey={ALPHA_KEY}"
    
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            feed = r.json().get('feed', [])
            processed_news = []
            for item in feed:
                title = item['title']
                source = item['source']
                # Score vai de -1 (Bearish) a 1 (Bullish)
                score = float(item['overall_sentiment_score'])
                
                sentiment_label = "NEUTRO"
                color = "#94a3b8" # Cinza
                
                if score >= 0.15: 
                    sentiment_label = "BULLISH"
                    color = "#10b981" # Verde
                elif score <= -0.15:
                    sentiment_label = "BEARISH"
                    color = "#ef4444" # Vermelho
                
                processed_news.append({
                    "title": title,
                    "source": source,
                    "score": score,
                    "label": sentiment_label,
                    "color": color,
                    "url": item['url']
                })
            return processed_news
    except:
        pass
    return None
