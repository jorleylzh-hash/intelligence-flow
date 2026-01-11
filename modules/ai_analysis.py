import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def configurar_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def analisar_mercado(dados_mercado):
    """
    Recebe um dicionário com dados (ex: {'WING26': 130000, 'PETR4': 38.50...})
    e retorna a análise textual da IA.
    """
    model = configurar_gemini()
    if not model:
        return "Erro: Chave API não configurada."

    prompt = f"""
    Atue como um analista sênior de Trading Institucional da 'Intelligence Flow'.
    Analise os seguintes dados de mercado em tempo real:
    {dados_mercado}
    
    Contexto:
    - O ativo principal é o índice futuro ou dólar.
    - Analise a correlação com Petro, Vale e Juros Futuros (DI).
    
    Forneça um resumo curto (máx 3 linhas) sobre o sentimento (Bullish/Bearish) e se há divergência ou confirmação de tendência.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"IA Indisponível no momento: {str(e)}"
