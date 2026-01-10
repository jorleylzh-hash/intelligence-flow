import requests
import streamlit as st
import random

# ==============================================================================
# 🔑 CHAVES DE PRODUÇÃO (INSERIDAS)
# ==============================================================================
BRAPI_TOKEN = "8KnkXQTU5haqRDCGiAoup2"       
TWELVE_KEY = "19744b9e6e99456da5af7c626c6148d0"        
ALPHA_KEY = "VSC2ZCMUJBJGM8SF"         
# ==============================================================================

# --- FUNÇÕES DE FALLBACK (Caso a API demore ou limite exceda) ---
def get_simulated_b3():
    return {
        "PETR4": (38.50, 0.5), "VALE3": (62.30, -0.2), 
        "ITUB4": (33.10, 1.2), "WEGE3": (40.20, 0.5), "BOVA11": (128.00, 0.1)
    }

def get_simulated_global():
    return {"DXY": (104.20, 0.15), "EUR/USD": (1.08, -0.05), "IXIC": (16200.00, 1.20)}

# 1. BRAPI (B3 - AÇÕES BRASIL)
@st.cache_data(ttl=60)
def get_b3_tickers():
    if BRAPI_TOKEN:
        try:
            # Lista de ativos monitorados
            tickers = "PETR4,VALE3,ITUB4,WEGE3,BOVA11"
            url = f"https://brapi.dev/api/quote/{tickers}?token={BRAPI_TOKEN}"
            
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json().get('results', [])
                results = {}
                for item in data:
                    # Captura preço e variação real
                    price = item.get('regularMarketPrice', 0.0)
                    change = item.get('regularMarketChangePercent', 0.0)
                    results[item['symbol']] = (price, change)
                
                if results: return results
        except Exception as e:
            print(f"Erro Brapi: {e}")
            pass
    
    return get_simulated_b3() # Fallback se falhar

# 2. TWELVE DATA (GLOBAL - FOREX & ÍNDICES)
@st.cache_data(ttl=60)
def get_global_tickers():
    if TWELVE_KEY:
        try:
            # DXY (Índice Dólar), EUR/USD, IXIC (Nasdaq)
            symbols = "DXY,EUR/USD,IXIC" 
            url = f"https://api.twelvedata.com/price?symbol={symbols}&apikey={TWELVE_KEY}"
            
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                results = {}
                
                # A Twelve Data retorna estrutura diferente se pedir 1 ou vários
                # Se houver erro de estrutura, cai no except e usa simulado
                for key, val in data.items():
                    price = float(val['price'])
                    # A API básica de preço não dá variação %, usamos 0.0 ou calculamos se tiver histórico
                    results[key] = (price, 0.0) 
                
                if results: return results
        except Exception as e:
            print(f"Erro Twelve: {e}")
            pass
    
    return get_simulated_global()

# 3. ALPHA VANTAGE (IA NEWS SENTIMENT)
@st.cache_data(ttl=300) 
def get_ai_news_sentiment():
    if ALPHA_KEY:
        try:
            # Busca notícias de Finanças/Mercado
            url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=finance&limit=5&apikey={ALPHA_KEY}"
            
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                feed = data.get('feed', [])
                processed = []
                
                for item in feed:
                    score = float(item.get('overall_sentiment_score', 0))
                    
                    # Lógica de Tradução do Sentimento
                    if score >= 0.15:
                        label = "OTIMISTA"
                        color = "#10b981" # Verde
                    elif score <= -0.15:
                        label = "PESSIMISTA"
                        color = "#ef4444" # Vermelho
                    else:
                        label = "NEUTRO"
                        color = "#94a3b8" # Cinza
                        
                    processed.append({
                        "title": item['title'],
                        "source": item['source'],
                        "score": score,
                        "label": label,
                        "color": color,
                        "url": item['url']
                    })
                
                if processed: return processed
        except Exception as e:
            print(f"Erro Alpha Vantage: {e}")
            pass
    
    # Retorna vazio ou simulado se exceder limite da API Free (5 calls/min)
    return [
        {"title": "Limit API reached or Connection Error", "source": "System", "score": 0.0, "label": "NEUTRO", "color": "#94a3b8", "url": "#"}
    ]
