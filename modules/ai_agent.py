import google.generativeai as genai
import os

def configure_genai():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return False
    genai.configure(api_key=api_key)
    return True

def consultar_gemini(dados_mercado, spread_arbitragem):
    """
    IA para o TRADING DESK
    """
    if not configure_genai(): return "⚠️ Erro: Chave API ausente."

    try:
        # ATUALIZADO: Usando o modelo disponível na sua conta
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Atue como Head de Trading Institucional.
        Dados: {dados_mercado}
        Arbitragem: {spread_arbitragem}%
        
        Responda em 3 bullets curtos:
        1. Sentimento (Bullish/Bearish/Neutro)
        2. Avaliação da Arbitragem
        3. Divergências Críticas
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback de segurança: Se o 2.5 falhar, tenta o 2.0
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            return response.text
        except:
            return f"Erro IA: {str(e)}"

def gerar_roadmap_solucoes(problema_usuario):
    """ 
    IA para a área de SOLUÇÕES 
    """
    if not configure_genai(): return "⚠️ Erro: Chave API ausente."

    try:
        # ATUALIZADO: Usando o modelo disponível na sua conta
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Você é o Arquiteto de Soluções da Intelligence Flow.
        Desafio: "{problema_usuario}"
        
        Gere um MAPA ESTRATÉGICO (Markdown).
        Estrutura Obrigatória:
        ### 🎯 Objetivo Central
        [Texto]
        ### 🗺️ Fases de Implementação
        #### Fase 1: Diagnóstico 🏗️
        * [Ação]
        #### Fase 2: Execução 🚀
        * [Ação]
        #### Fase 3: Resultados 💎
        * [Métrica]
        ---
        **💡 Insight IF:** [Frase final]
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar mapa: {str(e)}"
