import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def list_tables():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = conn.cursor()
        
        # Pergunta ao banco: "Quais tabelas você tem?"
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        tables = cursor.fetchall()
        
        print("\n--- 📂 TABELAS ENCONTRADAS NO NEON ---")
        if not tables:
            print("❌ Nenhuma tabela encontrada! O mt5_bridge.py criou a tabela?")
        else:
            for table in tables:
                print(f"✅ Tabela: {table[0]}")
                
                # Espia as colunas dessa tabela
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table[0]}'")
                columns = cursor.fetchall()
                cols_names = [c[0] for c in columns]
                print(f"   └── Colunas: {cols_names}")
                
        conn.close()
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    list_tables()