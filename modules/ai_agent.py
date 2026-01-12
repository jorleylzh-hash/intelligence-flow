import google.generativeai as genai
import os
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente (para rodar local)
load_dotenv()

# --- CONFIGURAÇÃO ---
def configure_genai():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: 
        return False
    genai.configure(api_key=api_key)
    return True

# --- PERSONA DO AGENTE ---
SYSTEM_INSTRUCTION = """
VOCÊ É: O Agente Intelligence Flow, uma IA especializada em Mercado Financeiro (B3, Forex, Macroeconomia).
TOM DE VOZ: Profissional, Institucional, Direto (estilo Bloomberg/Broadcast).
DIRETRIZES:
1. Nunca dê recomendação direta de compra/venda (Compliance).
2. Explique o "Porquê" dos movimentos (Drivers: Juros, Commodities, Risco Fiscal).
3. Seja conciso. Traders não leem textos longos durante o pregão.
"""

# --- FUNÇÃO PRINCIPAL BLINDADA ---
def consultar_gemini(user_input, contexto_adicional=""):
    """
    Consulta a IA com fallback: Tenta o modelo PRO (Inteligente), 
    se falhar por cota (429), usa o FLASH (Rápido).
    """
    if not configure_genai(): 
        return "⚠️ Erro: Chave API (GEMINI_API_KEY) não encontrada no .env ou nas variáveis do Render."
    
    # Prepara o prompt
    prompt_final = f"""
    {SYSTEM_INSTRUCTION}
    
    CONTEXTO TÉCNICO ATUAL (DADOS DO SISTEMA):
    {contexto_adicional}
    
    PERGUNTA DO TRADER:
    "{user_input}"
    
    RESPOSTA (Focada em análise de fluxo e correlações):
    """

    try:
        # TENTATIVA 1: Modelo Mais Inteligente (Pode dar erro de cota)
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt_final)
        return response.text
        
    except Exception as e_pro:
        # Se der erro (Cota excedida, server busy, etc), tenta o plano B
        try:
            # TENTATIVA 2: Modelo Mais Rápido (Aguenta muita carga)
            # print(f"Alternando para Flash devido a: {e_pro}") # Debug silencioso
            model_flash = genai.GenerativeModel('gemini-1.5-flash')
            response_flash = model_flash.generate_content(prompt_final)
            return f"⚡ (Modo Alta Velocidade) {response_flash.text}"
            
        except Exception as e_flash:
            # Se tudo falhar
            return f"❌ Sistema de IA indisponível no momento. (Erro: {str(e_flash)})"

# --- FUNÇÕES AUXILIARES (SOLUÇÕES/EDUCAÇÃO) ---
def gerar_roadmap_solucoes(problema):
    if not configure_genai(): return "Erro de Configuração API"
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # Usa flash direto para ser rápido
        return model.generate_content(f"Crie um roadmap executivo para: {problema}").text
    except:
        return "Não foi possível gerar o roadmap agora."
