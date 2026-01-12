import requests
import pandas as pd

# Variável Global para armazenar a URL da ponte
# (O usuário vai colar isso na tela do Streamlit)
URL_PONTE = None 

def set_url_ponte(url):
    global URL_PONTE
    # Garante que não tem barra no final
    URL_PONTE = url.rstrip("/")

def get_data_ponte(lista_ativos):
    """
    Busca dados direto do seu PC via API Ngrok
    """
    global URL_PONTE
    resultados = {}
    
    if not URL_PONTE:
        return {"ERRO": {"preco": 0, "origem": "URL Não Definida"}}

    for ativo in lista_ativos:
        try:
            # Faz a requisição para o seu PC: GET https://....ngrok-free.app/api/cotacao/WDO$N
            response = requests.get(f"{URL_PONTE}/api/cotacao/{ativo}", timeout=2)
            
            if response.status_code == 200:
                dados = response.json()
                if "erro" not in dados:
                    resultados[ativo] = {
                        "preco": dados['preco'],
                        "spread": dados['spread'],
                        "ask": dados['ask'],
                        "bid": dados['bid'],
                        "origem": "PC Local (Ponte) 🌉"
                    }
                else:
                    resultados[ativo] = {"preco": 0, "origem": "Erro MT5"}
            else:
                resultados[ativo] = {"preco": 0, "origem": "Erro Conexão"}
                
        except Exception as e:
            resultados[ativo] = {"preco": 0, "origem": "Offline"}

    return resultados
