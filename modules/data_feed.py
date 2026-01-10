import requests
import streamlit as st

# CHAVES (Mantenha as suas chaves aqui se já tiver colocado)
# Se não tiver, o código usa fallback visual
BRAPI_TOKEN = "8KnkXQTU5haqRDCGiAoup2" 
TWELVE_KEY = "19744b9e6e99456da5af7c626c6148d0"
ALPHA_KEY = "VSC2ZCMUJBJGM8SF"

# ... (Funções get_b3_tickers e get_global_tickers mantidas iguais) ...
# Vou focar na alteração da IA abaixo:

@st.cache_data(ttl=7200) 
def get_ai_news_sentiment():
    # Se não tiver chave, retorna None para não quebrar
    if not ALPHA_KEY or "COLE_SUA" in ALPHA_KEY: return None
    
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=finance&limit=5&apikey={ALPHA_KEY}"
    
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            feed = data.get('feed', [])
            processed_news = []
            
            for item in feed:
                title = item['title']
                source = item['source']
                score = float(item['overall_sentiment_score'])
                
                # --- TRADUÇÃO DO SENTIMENTO ---
                sentiment_label = "NEUTRO"
                color = "#94a3b8" # Cinza
                
                if score >= 0.15: 
                    sentiment_label = "OTIMISTA (ALTA)" # Traduzido
                    color = "#10b981" # Verde
                elif score <= -0.15:
                    sentiment_label = "PESSIMISTA (BAIXA)" # Traduzido
                    color = "#ef4444" # Vermelho
                
                processed_news.append({
                    "title": title, # Título original (inglês financeiro)
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
