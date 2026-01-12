# Arquivo: app.py
import os
import webbrowser
from modulo import dashboard_live

def main():
    try:
        # Chama a inteligência do módulo
        fig = dashboard_live.build_dashboard()
        
        # Salva e Exibe
        filename = "Monitor_M5_Live.html"
        fig.write_html(filename)
        
        print(f"\n[SUCESSO] Dashboard gerado: {filename}")
        
        # Abre automaticamente no navegador padrão
        file_path = os.path.realpath(filename)
        webbrowser.open(f'file://{file_path}')
        
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao gerar dashboard: {e}")

if __name__ == "__main__":
    main()
