import requests
import pandas as pd
from datetime import datetime

# Tenta importar MT5, mas não quebra se falhar (caso da Nuvem)
try:
    import MetaTrader5 as mt5
    MT5_INSTALADO = True
except ImportError:
    MT5_INSTALADO = False

# --- FUNÇÃO PRINCIPAL HÍBRIDA ---
def get_data_hibrido(lista_ativos, url_ponte=None):
    """
    Busca dados. Se tiver URL da ponte, usa ela.
    Se não, tenta MT5 local (apenas se estiver no PC).
    """
    resultados = {}
    
    # Verifica se a URL é válida (remove barra final se tiver)
    if url_ponte:
        url_ponte = url_ponte.rstrip("/")

    for ativo in lista_ativos:
        dados_coletados = None

        # 1. TENTATIVA VIA PONTE (Prioridade na Nuvem)
        if url_ponte:
            try:
                # Chama a API do seu PC: GET https://.../api/cotacao/WDO$N
                resp = requests.get(f"{url_ponte}/api/cotacao/{ativo}", timeout=3)
                if resp.status_code == 200:
                    json_data = resp.json()
                    if "erro" not in json_data:
                        dados_coletados = {
                            "preco": json_data['preco'],
                            "bid": json_data['bid'],
                            "ask": json_data['ask'],
                            "spread": json_data.get('spread', 0.5),
                            "volume": json_data.get('volume', 0),
                            "origem": "Ponte Nuvem ☁️"
                        }
            except Exception as e:
                # Se der erro na conexão, segue o baile
                pass

        # 2. TENTATIVA LOCAL (Fallback se estiver no PC sem ponte)
        if dados_coletados is None and MT5_INSTALADO:
            try:
                # Garante conexão
                if not mt5.initialize():
                    mt5.initialize()
                
                if mt5.symbol_select(ativo, True):
                    tick = mt5.symbol_info_tick(ativo)
                    if tick:
                        dados_coletados = {
                            "preco": tick.last,
                            "bid": tick.bid,
                            "ask": tick.ask,
                            "spread": tick.ask - tick.bid if tick.ask > tick.bid else 0.0,
                            "volume": tick.volume_real,
                            "origem": "MT5 Local 🏠"
                        }
            except:
                pass

        # 3. RESULTADO FINAL
        if dados_coletados:
            resultados[ativo] = dados_coletados
        else:
            resultados[ativo] = {"preco": 0.0, "origem": "Offline 🔴"}

    return resultados
