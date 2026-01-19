import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from models import Base

# Carrega suas configurações (URL do Neon)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print("🔌 Conectando ao Neon Database...")
engine = create_engine(DATABASE_URL)

def reset_tables():
    with engine.connect() as connection:
        print("⚠️  APAGANDO tabelas antigas (market_ticks e market_history)...")
        # Força a exclusão das tabelas que mudaram
        connection.execute(text("DROP TABLE IF EXISTS market_ticks CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS market_history CASCADE;"))
        connection.commit()
        print("✅ Tabelas antigas removidas.")

    print("🔨 Recriando tabelas com a NOVA estrutura (colunas change/source)...")
    # O SQLAlchemy lê seu models.py e cria tudo novinho
    Base.metadata.create_all(bind=engine)
    print("✅ Estrutura do Banco Atualizada com Sucesso!")

if __name__ == "__main__":
    reset_tables()