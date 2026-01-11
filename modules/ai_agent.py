import google.generativeai as genai
import os
import pandas as pd

# --- 1. CONFIGURAÇÃO E DADOS ---

def configure_genai():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: return False
    genai.configure(api_key=api_key)
    return True

def get_market_overview():
    """
    Simula (ou busca via API) um panorama completo de Renda Fixa e Variável.
    Isso alimenta o comando 'assets value'.
    """
    # Em produção, substitua por chamadas à API da Brapi/HG Brasil
    dados = {
        "Renda Fixa (Taxas Ref.)": {
            "Selic Meta": "11.25% a.a.",
            "CDI": "11.15% a.a.",
            "Tesouro IPCA+ 2029": "IPCA + 6.10%",
            "Tesouro Selic 2027": "Selic + 0.04%",
            "CDB Banco Master (Ref)": "120% do CDI"
        },
        "Renda Variável (Destaques B3)": {
            "IBOV": "128.500 pts",
            "PETR4": "R$ 38,45",
            "VALE3": "R$ 62,10",
            "WING26": "130.100 pts",
            "IFIX (FIIs)": "3.350 pts"
        },
        "Moedas e Global": {
            "Dólar (WDO)": "R$ 5.85",
            "S&P 500": "5.230 pts",
            "Bitcoin": "US$ 68,000"
        }
    }
    return str(dados)

# --- 2. A PERSONA (SYSTEM PROMPT) ---

SYSTEM_INSTRUCTION = """
CONTEXTO:
Você é o 'Agente Intelligence Flow', um analista de mercado financeiro institucional sênior.
Sua missão é fornecer dados baseados no princípio 'Full and Fair Disclosure'.

REGRAS DE CONDUTA (RESTRIÇÕES):
1. ASSUNTO RESTRITO: Você SÓ responde sobre Mercado Financeiro, Economia, Trading, Ativos (B3, NYSE, Cripto) e Análise Técnica/Fundamentalista.
2. RECUSA: Se o usuário perguntar sobre política partidária, receitas culinárias, relacionamentos, códigos de programação (fora de trading) ou qualquer tema não-financeiro, responda APENAS: "Como Agente Intelligence Flow, minha diretriz limita-se estritamente à análise de mercado financeiro."
3. TOM DE VOZ: Profissional, direto, técnico e imparcial. Sem gírias.
4. COMANDOS: Se o usuário digitar "assets value", forneça o resumo completo de Renda Fixa e Variável.
"""

# --- 3. FUNÇÕES DE CONSULTA ---

def consultar_gemini(user_input, contexto_adicional=""):
    """
    Função principal que processa a entrada do usuário.
    """
    if not configure_genai(): return "⚠️ Erro: Chave API ausente."

    # --- LÓGICA DO COMANDO ESPECÍFICO ---
    # Se o usuário digitar o comando exato (case insensitive)
    if user_input.strip().lower() == "assets value":
        dados_mercado = get_market_overview()
        prompt_especifico = f"""
        O usuário solicitou o comando 'assets value'.
        Abaixo estão os dados brutos atuais do mercado:
        {dados_mercado}
        
        TAREFA:
        Formate esses dados em uma tabela Markdown profissional e limpa.
        Separe claramente 'Renda Fixa' de 'Renda Variável'.
        Adicione um breve comentário de 1 linha sobre o sentimento geral.
        """
        user_input = prompt_especifico # Substitui o input pela instrução de formatação
    
    # --- FLUXO NORMAL DA IA ---
    try:
        # Usamos o modelo mais inteligente disponível (2.5 Pro)
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Montamos o Prompt Final com a Persona + Contexto + Pergunta
        full_prompt = f"""
        {SYSTEM_INSTRUCTION}
        
        CONTEXTO TÉCNICO ADICIONAL (Se houver):
        {contexto_adicional}
        
        PERGUNTA/COMANDO DO USUÁRIO:
        {user_input}
        """
        
        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        return f"Erro no Agente: {str(e)}"

# Mantemos a função de Roadmap para compatibilidade
def gerar_roadmap_solucoes(problema):
    if not configure_genai(): return "Erro API"
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        prompt = f"{SYSTEM_INSTRUCTION}\n\nGere um Roadmap para o desafio: {problema}"
        return model.generate_content(prompt).text
    except Exception as e: return str(e)
