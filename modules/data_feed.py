import MetaTrader5 as mt5
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import calendar

# --- CLASSE DE AUTOMAÇÃO DE VENCIMENTOS ---
class TickerAutomator:
    """
    Calcula automaticamente os códigos de WDO e WIN vigentes
    baseado nas regras da B3.
    """
    
    @staticmethod
    def get_vencimento_wdo():
        """
        Regra WDO: Vence no 1º dia útil do mês. 
        A letra corresponde ao mês de vencimento.
        A troca de liquidez (Rolagem) ocorre no último dia útil do mês anterior.
        """
        agora = datetime.now()
        mes_atual = agora.month
        ano_atual = agora.year
        
        # Letras de vencimento do Dólar (Jan a Dez)
        letras_wdo = {1:'F', 2:'G', 3:'H', 4:'J', 5:'K', 6:'M', 
                      7:'N', 8:'Q', 9:'U', 10:'V', 11:'X', 12:'Z'}
        
        # Último dia do mês atual
        ultimo_dia = calendar.monthrange(ano_atual, mes_atual)[1]
        data_limite = datetime(ano_atual, mes_atual, ultimo_dia)
        
        # Se hoje for o último dia do mês (ou depois), já operamos o próximo
        # Simplificação: Troca no último dia do mês
        if agora.day == ultimo_dia:
            mes_alvo = mes_atual + 2 # Pula para o próximo (ex: Em Jan(1) operamos Fev(2). No fim de Jan, operamos Mar(3))
        else:
            mes_alvo = mes_atual + 1 # Normal: Em Jan operamos Fev(G)
            
        # Ajuste de virada de ano
        ano_target = ano_atual
        if mes_alvo > 12:
            mes_alvo -= 12
            ano_target += 1
            
        letra = letras_wdo[mes_alvo]
        ano_curto = str(ano_target)[-2:]
        
        return f"WDO{letra}{ano_curto}"

    @staticmethod
    def get_vencimento_win():
        """
        Regra WIN: Vence nos meses PARES, na quarta-feira mais próxima do dia 15.
        """
        agora = datetime.now()
        
        # Letras: G(Fev), J(Abr), M(Jun), Q(Ago), V(Out), Z(Dez)
        letras_win = {2:'G', 4:'J', 6:'M', 8:'Q', 10:'V', 12:'Z'}
        
        mes_atual = agora.month
        ano_atual = agora.year
        
        # 1. Descobrir o próximo mês par (ou o atual se for par)
        if mes_atual % 2 != 0: # Ímpar
            mes_alvo = mes_atual + 1
        else:
            # É mês par. Precisamos ver se já venceu (passou da quarta-feira dia 15)
            # Encontra a 4ª feira mais próxima do dia 15
            dia_15 = datetime(ano_atual, mes_atual, 15)
            weekday_15 = dia_15.weekday() # 0=Seg, 2=Qua, 6=Dom
            
            # Ajuste para chegar na quarta (2)
            diferenca = 2 - weekday_15
            vencimento = dia_15 + timedelta(days=diferenca)
            
            if agora > vencimento:
                mes_alvo = mes_atual + 2 # Já venceu, vai pro próximo par
            else:
                mes_alvo = mes_atual # Ainda não venceu
                
        # Ajuste virada de ano
        ano_target = ano_atual
        if mes_alvo > 12:
            mes_alvo -= 12
            ano_target += 1
            
        letra = letras_win[mes_alvo]
        ano_curto = str(ano_target)[-2:]
        
        return f"WIN{letra}{ano_curto}"

# --- SEU MAPA DE CORRELAÇÃO ATUALIZADO ---
def get_tickers_atualizados():
    # Calcula os códigos quentes do momento
    ticker_wdo = TickerAutomator.get_vencimento_wdo()
    ticker_win = TickerAutomator.get_vencimento_win()
    
    return {
        # AUTOMATIZADOS (O gargalo resolvido)
        "WDO":   {"source": "MT5", "symbol": ticker_wdo}, 
        "WIN":   {"source": "MT5", "symbol": ticker_win},
        
        # MANTIDOS (Série perpétua ou Ações)
        "DI29":  {"source": "MT5", "symbol": "DI1F29"},
        "PETR4": {"source": "MT5", "symbol": "PETR4"},
        "VALE3": {"source": "MT5", "symbol": "VALE3"},
        
        # INTERNACIONAL (YFinance)
        "DXY":     {"source": "YF", "symbol": "DX-Y.NYB"},
        "SPX_US":  {"source": "YF", "symbol": "ES=F"},
        "US10Y":   {"source": "YF", "symbol": "^TNX"},
        "VALE_ADR":{"source": "YF", "symbol": "VALE"},
        "EWZ":     {"source": "YF", "symbol": "EWZ"},
    }

# --- FUNÇÕES DE CONEXÃO (Mantidas do seu código anterior) ---
def conectar_mt5():
    if not mt5.initialize():
        print("❌ Erro MT5:", mt5.last_error())
        return False
    return True

def get_data_hibrido(lista_ativos_usuario):
    DICT_ATIVOS = get_tickers_atualizados() # <--- Chama a automação aqui
    resultados = {}
    
    # 1. Busca dados MT5
    for nome_amigavel in lista_ativos_usuario:
        config = DICT_ATIVOS.get(nome_amigavel)
        if config and config["source"] == "MT5":
            tick = mt5.symbol_info_tick(config["symbol"])
            if tick:
                resultados[nome_amigavel] = {
                    "preco": tick.last,
                    "symbol_real": config["symbol"], # Útil para ver qual código ele pegou
                    "origem": "MT5 ⚡"
                }
            else:
                resultados[nome_amigavel] = {"preco": 0.0, "origem": "MT5 (Off)"}

    # 2. Busca dados YFinance (Lógica mantida)
    tickers_yf = [v["symbol"] for k, v in DICT_ATIVOS.items() if v["source"] == "YF" and k in lista_ativos_usuario]
    if tickers_yf:
        try:
            dados_yf = yf.download(tickers_yf, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
            for nome_amigavel in lista_ativos_usuario:
                config = DICT_ATIVOS.get(nome_amigavel)
                if config and config["source"] == "YF":
                    sym = config["symbol"]
                    try:
                        price = dados_yf[sym] if isinstance(dados_yf, pd.Series) else dados_yf
                        resultados[nome_amigavel] = {
                            "preco": float(price),
                            "origem": "Cloud ☁️"
                        }
                    except: pass
        except Exception as e:
            print(f"Erro YF: {e}")

    return resultados
