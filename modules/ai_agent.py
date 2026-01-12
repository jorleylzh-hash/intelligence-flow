import google.generativeai as genai
import os
import requests

# --- CONFIGURAÇÃO ---
def configure_genai():
    # Tenta pegar a chave das Variáveis de Ambiente do Sistema (Render)
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Se você preferir hardcoded (não recomendado, mas funciona), descomente abaixo:
    # api_key = "SUA_CHAVE_AQUI_SE_QUISER_FIXA"
    
    if not api_key: 
        return False
    genai.configure(api_key=api_key)
    return True

# --- PERSONA DO AGENTE ---
SYSTEM_INSTRUCTION = """
VOCÊ É: O Agente Intelligence Flow, uma IA especializada em Mercado Financeiro.
TOM DE VOZ: Profissional, Institucional, Direto.
DIRETRIZES:
1. Sem recomendações de compra/venda.
2. Foco em Drivers e Fluxo.
3. Seja conciso.
"""

# --- FUNÇÃO PRINCIPAL BLINDADA ---
def consultar_gemini(user_input, contexto_adicional=""):
    if not configure_genai(): 
        return "⚠️ Erro: Chave API (GEMINI_API_KEY) não configurada no Render."
    
    prompt_final = f"""
    {SYSTEM_INSTRUCTION}
    CONTEXTO TÉCNICO: {contexto_adicional}
    PERGUNTA: "{user_input}"
    """

    try:
        # TENTA MODELO PRO
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt_final)
        return response.text
    except Exception:
        try:
            # TENTA MODELO FLASH
            model_flash = genai.GenerativeModel('gemini-1.5-flash')
            response_flash = model_flash.generate_content(prompt_final)
            return f"⚡ {response_flash.text}"
        except Exception as e:
            return f"❌ IA Indisponível: {str(e)}"

def gerar_roadmap_solucoes(problema):
    if not configure_genai(): return "Erro Configuração"
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(f"Roadmap para: {problema}").text
    except:
        return "Erro ao gerar roadmap."
