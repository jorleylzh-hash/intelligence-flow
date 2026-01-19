import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Carrega o .env que está na mesma pasta
load_dotenv()

# Pega a chave do banco
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    # Fallback para SQLite se a chave der erro, só para não crashar
    print("⚠️ DATABASE_URL não encontrada. Usando SQLite local.")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./temp.db"

# Ajuste para Neon
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# CRIA O MOTOR (ENGINE) DE LEITURA
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()