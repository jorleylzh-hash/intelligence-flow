import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print("--- 📡 CONSULTANDO MODELOS DISPONÍVEIS NO GOOGLE ---")

try:
    response = requests.get(url)
    if response.status_code == 200:
        models = response.json().get('models', [])
        found_flash = False
        print(f"✅ Conexão OK! Listando modelos permitidos para sua chave:\n")
        
        for m in models:
            name = m['name'].replace('models/', '')
            # Filtra apenas os que geram texto
            if 'generateContent' in m['supportedGenerationMethods']:
                print(f"🔹 {name}")
                if "flash" in name:
                    found_flash = True
        
        print("\n------------------------------------------------")
        if not found_flash:
            print("⚠️ AVISO: Nenhum modelo 'Flash' encontrado na sua lista!")
        else:
            print("💡 DICA: Copie um dos nomes acima EXATAMENTE como aparece (ex: gemini-1.5-flash)")
            
    else:
        print(f"❌ Erro de Permissão: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Erro de Conexão: {e}")