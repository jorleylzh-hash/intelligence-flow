import google.generativeai as genai
import os

def configure_genai():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return True

def consultar_gemini_trader(dados_mercado, spread_arbitragem):
    """ IA focada no Trading Desk (Respostas curtas) """
    if not configure_genai(): return "⚠️ Erro: Chave API ausente."

    try:
        # Modelo atualizado e rápido
        model = genai.GenerativeModel('gemini-1.5-flash')
        
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
        return f"Erro IA: {str(e)}"

def gerar_roadmap_solucoes(problema_usuario):
    """ NOVA FUNÇÃO: Gera o Mapa de Soluções Estratégicas """
    if not configure_genai(): return "⚠️ Erro: Chave API ausente."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt desenhado para criar o "Formato de Mapa"
        prompt = f"""
        Você é o Arquiteto de Soluções da Intelligence Flow.
        O usuário tem o seguinte desafio: "{problema_usuario}"
        
        Gere um MAPA ESTRATÉGICO DE SOLUÇÃO.
        Não use texto corrido. Use estritamente a estrutura visual abaixo (Markdown):

        ### 🎯 Objetivo Central
        [Definição clara do objetivo]

        ### 🗺️ Fases de Implementação
        
        #### Fase 1: Diagnóstico & Base 🏗️
        * [Ação Chave 1]
        * [Ação Chave 2]
        
        #### Fase 2: Execução & Otimização 🚀
        * [Ação Chave 1]
        * [Tecnologia Sugerida]
        
        #### Fase 3: Escala & Resultados 💎
        * [Métrica de Sucesso]
        * [Impacto Esperado]

        ---
        **💡 Insight Intelligence Flow:** [Uma frase de alto impacto sobre a solução]
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar mapa: {str(e)}"
