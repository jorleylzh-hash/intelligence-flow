from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# --- MODELO DE USUÁRIO ---
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

# --- MODELO DE VERIFICAÇÃO (Códigos de Email) ---
class VerificationToken(Base):
    __tablename__ = "verification_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    code = Column(String)
    expires_at = Column(DateTime)

# --- MODELO DE MERCADO (TICK A TICK / COTAÇÃO ATUAL) ---
# --- MODELO DE MERCADO (TICK A TICK / COTAÇÃO ATUAL) ---
class MarketTick(Base):
    __tablename__ = "market_ticks"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    price = Column(Float)
    
    # ADICIONANDO AS COLUNAS QUE O ERRO RECLAMOU
    open = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    change = Column(Float, nullable=True)
    source = Column(String, nullable=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow)

# --- NOVO MODELO: HISTÓRICO DE VELAS (OHLC) ---
class MarketHistory(Base):
    __tablename__ = "market_history"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    time = Column(DateTime, index=True) # Timestamp da vela
    
    # Dados OHLC
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    
    # Identifica de onde veio (MT5_LOCAL ou MT5_GLOBAL)
    source = Column(String) 

    # Garante que não teremos duas velas do mesmo horário para o mesmo ativo
    __table_args__ = (
        UniqueConstraint('ticker', 'time', name='uix_ticker_time'),
    )