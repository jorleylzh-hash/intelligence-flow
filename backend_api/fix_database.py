import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from models import Base, MarketTick # Importa o modelo atualizado

# Carrega configurações
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def fix_schema():
    print("🔌 Conectando ao Neon...")
    
    with engine.connect() as connection:
        print("🔥 Destruindo tabela 'market_ticks' antiga...")
        # O CASCADE garante que se algo depender dela, também apaga (limpeza total)
        connection.execute(text("DROP TABLE IF EXISTS market_ticks CASCADE;"))
        connection.commit()
        print("✅ Tabela antiga removida.")

    print("🏗️  Criando nova tabela 'market_ticks' com colunas OPEN, HIGH, LOW...")
    # Recria TODAS as tabelas baseadas no models.py atual
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de Dados Corrigido! Estrutura nova aplicada.")

if __name__ == "__main__":
    fix_schema()