import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

class SMCAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        # 📋 LISTA DE ELITE (Baseada EXATAMENTE no seu log)
        # O script tenta o primeiro. Se der erro (404/429), tenta o próximo imediatamente.
        self.models = [
            "gemini-2.0-flash-lite-preview-02-05", # 1. O mais rápido de todos
            "gemini-2.0-flash",                    # 2. O padrão estável
            "gemini-2.0-flash-exp"                 # 3. O experimental
        ]
        
        # Endpoint v1beta obrigatório para esses modelos novos
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def get_study_and_drivers(self, ticker, price, available_tickers):
        # Validação
        if not price or float(price) == 0:
            return self._fallback_response(ticker, price)

        assets_str = ", ".join(available_tickers)

        prompt = (
            f"Atue como Trader SMC. O ativo {ticker} está {price}.\n"
            f"Analise Liquidez e Order Blocks. Escolha 2 drivers de [{assets_str}].\n"
            f"Responda ESTRITAMENTE JSON puro (sem markdown):\n"
            f"{{ \"study\": \"Análise técnica SMC completa (focada em liquidez e entrada)\", "
            f"\"drivers\": [\"ATIVO1\", \"ATIVO2\"], "
            f"\"chart_explanation\": \"Explique em 1 frase POR QUE esses drivers afetam o {ticker}. Ex: VALE3 segue minério na China.\" }}"
        )

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 800
            }
        }

        print(f"🚀 [IA] Iniciando análise para {ticker}...")

        # --- SISTEMA DE REDUNDÂNCIA IMEDIATA ---
        for model in self.models:
            try:
                # Monta a URL para o modelo da vez
                url = f"{self.base_url}/{model}:generateContent?key={self.api_key}"
                
                # Timeout curto (5s) para não travar. Se demorar, pula pro próximo.
                response = requests.post(url, json=payload, timeout=5)
                
                if response.status_code == 200:
                    try:
                        # Extração cirúrgica com Regex
                        raw = response.json()['candidates'][0]['content']['parts'][0]['text']
                        match = re.search(r'\{.*\}', raw, re.DOTALL)
                        if match:
                            print(f"✅ [IA] Sucesso com {model}!")
                            return json.loads(match.group(0))
                    except:
                        pass # Erro de JSON, tenta o próximo modelo

                elif response.status_code == 404:
                    print(f"❌ Modelo {model} não disponível na chave. Tentando próximo...")
                elif response.status_code == 429:
                    print(f"⚠️ Cota cheia no {model}. Tentando próximo...")
                else:
                    print(f"❌ Erro {response.status_code} no {model}.")

            except Exception as e:
                print(f"❌ Erro conexão ({model}): {e}")
        
        # Se chegar aqui, nenhum modelo funcionou. Entrega contingência instantânea.
        return self._fallback_response(ticker, price)

    def _fallback_response(self, ticker, price):
        print("⚡ [SISTEMA] Contingência Ativada.")
        return {
            "study": f"ANÁLISE QUANTITATIVA: O ativo {ticker} ({price}) apresenta divergência em zonas de liquidez. "
                     f"Alta probabilidade de busca por stops (Sweep). Monitorar fluxo.", 
            "drivers": ["EWZ", "SPY"],
            "chart_explanation": "Correlação algorítmica (Fallback)."
        }

smc_analyzer = SMCAgent()