import google.generativeai as genai
import os
import requests
import json

# --- 1. CONFIGURAÇÃO ---
def configure_genai():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: return False
    genai.configure(api_key=api_key)
    return True

# --- 2. DADOS DE MERCADO (Comando: assets value) ---
def get_market_overview():
    """ Busca dados reais para o comando 'assets value' """
    # Tentativa de pegar dados reais da Brapi (Gratuito)
    url = "https://brapi.dev/api/quote/PETR4,VALE3,BTC-USD,USDBRL"
    
    dados = {
        "Renda Fixa (Referência)": {
            "Selic Meta": "11.25% a.a. (Copom)",
            "CDI": "11.15% a.a.",
            "Tesouro IPCA+": "IPCA + 6.XX%"
        }
    }
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            res = {i['symbol']: i['regularMarketPrice'] for i in resp.json()['results']}
            dados["Renda Variável"] = {"PETR4": res.get('PETR4'), "VALE3": res.get('VALE3')}
            dados["Moedas/Cripto"] = {"Dólar": res.get('USDBRL'), "Bitcoin": res.get('BTC-USD')}
        else:
            dados["Status"] = "Dados offline (Delay B3)"
    except:
        dados["Status"] = "Erro de Conexão API"
        
    return str(dados)

# --- 3. CONTEÚDO EDUCACIONAL (NOVO: Comando 'educational map') ---
def get_educational_syllabus():
    """ Retorna a ementa estruturada (Estilo CPA-20 / ANCORD) """
    ementa = {
        "1. Sistema Financeiro Nacional (SFN)": [
            "CMN (Conselho Monetário Nacional): O órgão normativo máximo.",
            "Bacen (Banco Central): Executor da política monetária e cambial.",
            "CVM (Comissão de Valores Mobiliários): Fiscalizador do mercado de capitais."
        ],
        "2. Infraestrutura de Mercado": [
            "B3 (Brasil, Bolsa, Balcão): Histórico e Fusão (Bovespa + BM&F + Cetip).",
            "Clearing House: Câmaras de compensação e liquidação.",
            "Full and Fair Disclosure: O princípio da transparência total."
        ],
        "3. Instrumentos Financeiros": [
            "Renda Variável: Ações, FIIs, ETFs e BDRs.",
            "Derivativos: Futuros (Dólar/Índice), Opções e Swaps.",
            "Renda Fixa: Títulos Públicos (Tesouro) e Privados (CDB, LCI, LCA)."
        ],
        "4. Economia e Indicadores": [
            "IPCA e IGPM (Inflação).",
            "PIB (Atividade Econômica).",
            "Taxa de Câmbio e Reservas Internacionais."
        ]
    }
    return str(ementa)

# --- 4. A PERSONA (SYSTEM PROMPT) ---
SYSTEM_INSTRUCTION = """
IDENTIDADE:
Você é o 'Agente Intelligence Flow', uma IA especialista em Mercado Financeiro.
Você NÃO é um Analista CNPI, portanto, NÃO faz recomendações de compra/venda.

FUNÇÕES:
1. LEITURA DE MERCADO: Interpretar dados técnicos e fundamentalistas.
2. TUTOR EDUCACIONAL: Explicar conceitos complexos (CVM, B3, Derivativos) de forma didática.

REGRAS DE CONDUTA:
1. NUNCA dê "Calls" (Indicação de investimento).
2. Se o usuário pedir "educational map", apresente a Ementa de Estudos.
3. Se o usuário pedir "assets value", apresente as cotações.
4. Assuntos fora de finanças devem ser recusados cordialmente.
"""

# --- 5. FUNÇÃO PRINCIPAL DE CONSULTA ---
def consultar_gemini(user_input, contexto_adicional=""):
    if not configure_genai(): return "⚠️ Erro: Chave API ausente."
    
    user_input_clean = user_input.strip().lower()

    # --- COMANDO 1: COTAÇÕES ---
    if user_input_clean == "assets value":
        dados = get_market_overview()
        prompt_final = f"""
        {SYSTEM_INSTRUCTION}
        O usuário executou o comando 'assets value'.
        Dados brutos: {dados}
        TAREFA: Gere uma tabela Markdown com estes valores. Adicione um breve comentário sobre a volatilidade atual.
        """
        
    # --- COMANDO 2: CONTEÚDO EDUCACIONAL (NOVO) ---
    elif user_input_clean == "educational map" or user_input_clean == "topicos":
        syllabus = get_educational_syllabus()
        prompt_final = f"""
        {SYSTEM_INSTRUCTION}
        O usuário executou o comando 'educational map'.
        
        EMENTA DO CURSO:
        {syllabus}
        
        TAREFA:
        1. Apresente esta ementa em formato de Lista Estruturada (Markdown).
        2. Convide o usuário a escolher um tópico para aprender mais (Ex: "Digite 'História da B3' para saber mais").
        3. Use emojis para separar os módulos.
        """
    
    # --- FLUXO LIVRE (PERGUNTAS GERAIS) ---
    else:
        prompt_final = f"""
        {SYSTEM_INSTRUCTION}
        PERGUNTA DO USUÁRIO: "{user_input}"
        """

    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        return model.generate_content(prompt_final).text
    except Exception as e:
        return f"Erro no Agente: {str(e)}"

# Mantido para compatibilidade com o módulo Solutions
def gerar_roadmap_solucoes(problema):
    if not configure_genai(): return "Erro API"
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        return model.generate_content(f"{SYSTEM_INSTRUCTION}\nRoadmap para: {problema}").text
    except: return "Erro"
