import google.generativeai as genai
import os

def configure_genai():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return False
    genai.configure(api_key=api_key)
    return True

def try_generate(prompt):
    """
    Tenta gerar conteúdo testando múltiplos modelos em sequência.
    Isso resolve o problema de erro 404 por nome de modelo errado.
    """
    # Lista de tentativas: Do mais novo para o mais antigo/estável
    modelos_tentativa = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-1.0-pro', 
        'gemini-pro'
    ]
    
    erros = []

    for nome_modelo in modelos_tentativa:
        try:
            model = genai.GenerativeModel(nome_modelo)
            response = model.generate_content(prompt)
            return response.text # Sucesso! Retorna e sai da função.
        except Exception as e:
            erros.append(f"{nome_modelo}: {str(e)}")
            continue # Tenta o próximo da lista
            
    # Se chegou aqui, todos falharam. Vamos tentar listar o que existe.
    try:
        disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        lista_str = ", ".join(disponiveis)
        return f"⚠️ ERRO CRÍTICO IA. Nenhum modelo funcionou.\nModelos disponíveis na sua conta: {lista_str}.\nErros técnicos: {erros}"
    except Exception as e_list:
        return f"⚠️ ERRO TOTAL. API Key pode estar inválida ou sem permissão.\nDetalhes: {erros}"

def consultar_gemini(dados_mercado, spread_arbitragem):
    if not configure_genai(): return "⚠️ Configurar GEMINI_API_KEY no Render."
    
    prompt = f"""
    Analista de Trading. Dados: {dados_mercado}. Spread: {spread_arbitragem}%.
    Responda curto: 1. Sentimento 2. Arbitragem 3. Divergências.
    """
    return try_generate(prompt)

def gerar_roadmap_solucoes(problema_usuario):
    if not configure_genai(): return "⚠️ Configurar GEMINI_API_KEY no Render."
    
    prompt = f"""
    Arquiteto de Soluções. Desafio: "{problema_usuario}".
    Gere um Roadmap em Markdown (Objetivo, Fases 1/2/3, Insight).
    """
    return try_generate(prompt)
