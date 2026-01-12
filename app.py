import streamlit as st
from modules import trader_area

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Intelligence Flow", 
    layout="wide", 
    page_icon="⚡"
)

# --- APLICAÇÃO PRINCIPAL ---
def main():
    # Não verificamos mais "conectar_mt5" aqui.
    # O App carrega livre e a conexão acontece dentro da Área Trader via Link.
    trader_area.render_trader_area()

if __name__ == "__main__":
    main()
