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

# --- 2. DADOS DE MERCADO ---
def get_market_overview():
    url = "https://brapi.dev/api/quote/PETR4,VALE3,BTC-USD,USDBRL"
    dados = {
        "Renda Fixa (Ref)": {"Selic": "11.25%", "CDI": "11.15%"},
        "Renda Variável": {},
        "Câmbio": {}
    }
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            res = {i['symbol']: i['regularMarketPrice'] for i in resp.json()['results']}
            dados["Renda Variável"] = {"PETR4": res.get('PETR4'), "VALE3": res.get('VALE3')}
            dados["Câmbio"] = {"Dólar": res.get('USDBRL'), "Bitcoin": res.get('BTC-USD')}
        else:
            dados["Status"] = "Dados offline"
    except:
        dados["Status"] = "Erro API Dados"
    return str(dados)

# --- 3. EMENTA EDUCACIONAL ---
def get_educational_syllabus():
    return str({
        "1. SFN": ["CMN", "Bacen", "CVM"],
        "2. Mercado": ["B3", "Clearing", "Disclosure"],
        "3. Produtos": ["Ações", "FIIs", "Derivativos (Futuros/Opções)"]
    })

# --- 4. PERSONA ---
SYSTEM_INSTRUCTION = """
IDENTIDADE: Agente Intelligence Flow (IA Financeira). NÃO sou analista CNPI.
FUNÇÃO: Leitura de Mercado e Educação.
REGRAS: Sem recomendações de compra/venda.
"""

# --- 5. FUNÇÃO BLINDADA (COM FALLBACK) ---
def consultar_gemini(user_input, contexto_adicional=""):
    if not configure_genai(): return "⚠️ Erro: Chave API ausente."
    
    user_input_clean = user_input.strip().lower()

    # Prepara o Prompt conforme o comando
    if user_input_clean == "assets value":
        dados = get_market_overview()
        prompt_final = f"{SYSTEM_INSTRUCTION}\nComando 'assets value'. Dados: {dados}\nGere tabela Markdown."
    elif user_input_clean == "educational map" or user_input_clean == "topicos":
        syllabus = get_educational_syllabus()
        prompt_final = f"{SYSTEM_INSTRUCTION}\nComando 'educational map'. Ementa: {syllabus}\nListe os tópicos."
    else:
        prompt_final = f"{SYSTEM_INSTRUCTION}\nContexto: {contexto_adicional}\nPergunta: {user_input}"

    # --- LÓGICA DE TENTATIVAS (RETRY) ---
    try:
        # TENTATIVA 1: O Melhor Modelo (2.5 Pro)
        model = genai.GenerativeModel('gemini-2.5-pro')
        return model.generate_content(prompt_final).text
        
    except Exception as e_pro:
        erro_str = str(e_pro).lower()
        # Se for erro de Cota (429) ou Recurso Esgotado
        if "429" in erro_str or "quota" in erro_str or "exhausted" in erro_str:
            try:
                # TENTATIVA 2: O Modelo Rápido (Flash) - Aguenta muito mais carga
                model_flash = genai.GenerativeModel('gemini-2.5-flash')
                resposta_flash = model_flash.generate_content(prompt_final).text
                return f"⚠️ *Nota: Alta demanda no modelo Pro. Respondendo via Flash (Alta Velocidade).*\n\n{resposta_flash}"
            except Exception as e_flash:
                return f"❌ Erro Crítico: Ambos os modelos (Pro e Flash) falharam.\nDetalhe: {str(e_flash)}"
        
        # Se for outro erro (não cota), mostra direto
        return f"❌ Erro Técnico: {str(e_pro)}"

# Função Soluções (Também com Fallback)
def gerar_roadmap_solucoes(problema):
    if not configure_genai(): return "Erro API"
    prompt = f"{SYSTEM_INSTRUCTION}\nRoadmap para: {problema}"
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        return model.generate_content(prompt).text
    except:
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            return model.generate_content(prompt).text
        except Exception as e:
            return f"Erro ao gerar mapa: {str(e)}"
