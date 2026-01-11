import google.generativeai as genai
import os

def consultar_gemini(dados_mercado, spread_arbitragem):
    """
    Função isolada para conectar com a IA Intelligence Flow
    """
    # Pega a chave configurada nas Variáveis de Ambiente do Render
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return "⚠️ Erro: Chave API (GEMINI_API_KEY) não encontrada no Render."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        Você é o analista chefe da Intelligence Flow.
        Analise os dados abaixo com o princípio 'Full and Fair Disclosure'.
        
        DADOS DE MERCADO:
        {dados_mercado}
        
        ARBITRAGEM (B3 vs NYSE):
        Spread atual: {spread_arbitragem}%
        
        Responda em português, curto e direto (máx 3 linhas):
        1. Qual o sentimento (Bullish/Bearish)?
        2. O spread favorece a ponta compradora ou vendedora?
        3. Há divergência crítica nos drivers?
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"IA Indisponível: {str(e)}"
