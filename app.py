import streamlit as st
from modules import trader_area

st.set_page_config(page_title="Intelligence Flow", layout="wide")

def main():
    # Carrega direto a área do trader. A conexão é feita lá dentro automaticamente.
    trader_area.render_trader_area()

if __name__ == "__main__":
    main()
