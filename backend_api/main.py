import os
import random
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text, func, or_
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

from models import Base, MarketTick, MarketHistory, User, VerificationToken
from auth_service import (
    get_password_hash, verify_password, generate_complex_code, send_verification_email
)

load_dotenv()
# CONFIGURAÇÃO DO BANCO DE DADOS
DATABASE_URL = os.getenv("DATABASE_URL")

# --- BLOCO DE CORREÇÃO AUTOMÁTICA (O FIX DO RENDER) ---
# O Render entrega 'postgres://', mas o SQLAlchemy pede 'postgresql://'
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
# ------------------------------------------------------

if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não foi encontrada!")

# Criação do Engine com a URL corrigida
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ... (o resto do código permanece igual)

app = FastAPI(title="Intelligence Flow API v3.3 - Debug Arbitrage")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SCHEMAS ---
class SignupRequestSchema(BaseModel):
    email: str
    full_name: str

class CompleteSignupSchema(BaseModel):
    email: str
    code: str
    password: str

class LoginSchema(BaseModel):
    email: str
    password: str

class MarketDataSchema(BaseModel):
    ticker: str
    price: float
    open: Optional[float] = 0.0
    high: Optional[float] = 0.0
    low: Optional[float] = 0.0
    volume: Optional[float] = 0.0
    change: Optional[float] = 0.0
    source: Optional[str] = "MT5"
    timestamp: Optional[datetime] = None
    class Config:
        from_attributes = True

class ChartPointSchema(BaseModel):
    time: float 
    price: float
    open: float
    high: float
    low: float
    volume: float
    vwap: Optional[float] = None 

class PortfolioSchema(BaseModel):
    net_worth: float
    allocation: List[Dict[str, Any]]
    risk_matrix: List[Dict[str, Any]]
    positions: List[Dict[str, Any]]
    insight: Dict[str, str]

class ArbitrageOpportunity(BaseModel):
    asset: str
    local_price: float
    global_price_brl: float
    spread_pct: float
    status: str
    timestamp: datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- FUNÇÕES AUXILIARES ---
def get_latest_price_data(db: Session, ticker_partial: str):
    """ Busca Inteligente: Tenta encontrar o ativo mesmo com nome parcial """
    
    # 1. Tenta encontrar qualquer ativo que CONTENHA o nome (ex: "PETR4" acha "PETR4F")
    # Busca primeiro no Tick (Tempo Real)
    tick = db.query(MarketTick).filter(
        MarketTick.ticker.ilike(f"%{ticker_partial}%")
    ).order_by(MarketTick.timestamp.desc()).first()
    
    if tick:
        return {"price": tick.price, "obj": tick, "type": "realtime", "name": tick.ticker}
    
    # 2. Se não achar, busca no Histórico
    hist = db.query(MarketHistory).filter(
        MarketHistory.ticker.ilike(f"%{ticker_partial}%")
    ).order_by(MarketHistory.time.desc()).first()
    
    if hist:
        return {"price": hist.close, "obj": hist, "type": "history", "name": hist.ticker}
        
    return None

# --- ROTAS ---
@app.post("/auth/initiate-signup")
def initiate_signup(data: SignupRequestSchema, db: Session = Depends(get_db)):
    return {"message": "Código enviado."}

@app.post("/auth/complete-signup")
def complete_signup(data: CompleteSignupSchema, db: Session = Depends(get_db)):
    return {"message": "Conta criada."}

@app.post("/auth/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    return {"message": "Login OK", "user": {"email": data.email, "name": "Trader Z"}}

@app.get("/market/all", response_model=List[MarketDataSchema])
def get_market_data(db: Session = Depends(get_db)):
    unique_tickers_hist = db.query(MarketHistory.ticker).distinct().all()
    ticker_list = [t[0] for t in unique_tickers_hist]
    
    results = []
    for t in ticker_list:
        # Lógica simplificada para o overview
        last_candle = db.query(MarketHistory).filter(MarketHistory.ticker == t).order_by(MarketHistory.time.desc()).first()
        if last_candle:
            change = ((last_candle.close - last_candle.open) / last_candle.open * 100) if last_candle.open else 0.0
            results.append({
                "ticker": t,
                "price": last_candle.close,
                "open": last_candle.open,
                "high": last_candle.high,
                "low": last_candle.low,
                "volume": last_candle.volume,
                "change": round(change, 2),
                "source": last_candle.source or "MT5",
                "timestamp": last_candle.time
            })
    return sorted(results, key=lambda x: x['ticker'])

@app.get("/market/history/{ticker}", response_model=List[ChartPointSchema])
def get_ticker_history(ticker: str, db: Session = Depends(get_db)):
    # Busca com ILIKE para garantir que acha PETR4 mesmo se pedir petr4
    history = db.query(MarketHistory).filter(
        MarketHistory.ticker.ilike(f"%{ticker}%")
    ).order_by(MarketHistory.time.desc()).limit(300).all()
    
    data_points = []
    if history:
        for candle in reversed(history):
            data_points.append({
                "time": candle.time.timestamp(), 
                "price": candle.close,
                "open": candle.open,
                "high": candle.high,
                "low": candle.low,
                "volume": candle.volume,
                "vwap": candle.close
            })
    return data_points

# ==========================================
# ROTA ARBITRAGEM (DEBUG ATIVADO)
# ==========================================
@app.get("/market/arbitrage", response_model=List[ArbitrageOpportunity])
def get_arbitrage_monitor(db: Session = Depends(get_db)):
    print("\n--- 🔍 DEBUG ARBITRAGEM ---")
    
    def get_val(sym):
        data = get_latest_price_data(db, sym)
        if data:
            print(f"   ✅ {sym}: Encontrado ({data['name']}) -> {data['price']}")
            return data["price"]
        print(f"   ❌ {sym}: NÃO ENCONTRADO NO BANCO")
        return 0.0

    # Busca os ativos principais
    petr4 = get_val("PETR4")
    pbr = get_val("PBR")
    vale3 = get_val("VALE3")
    vale = get_val("VALE")
    
    # Busca Dólar (Tenta WDO, se falhar tenta USDBRL, se falhar usa fixo)
    wdo_data = get_latest_price_data(db, "WDO")
    if not wdo_data: wdo_data = get_latest_price_data(db, "USDBRL")
    
    if wdo_data:
        # Se for WDO (Indice), divide por 1000. Se for Spot, usa direto.
        raw_price = wdo_data["price"]
        usd = raw_price / 1000 if raw_price > 100 else raw_price
        print(f"   💵 Dólar: Encontrado ({wdo_data['name']}) -> {usd}")
    else:
        usd = 5.85
        print(f"   ⚠️ Dólar: Não encontrado. Usando FIXO -> {usd}")

    opportunities = []

    # CÁLCULO PETR4
    if petr4 > 0 and pbr > 0:
        fair_price = (pbr * usd) / 2
        spread = ((petr4 - fair_price) / fair_price) * 100
        
        status = "NEUTRO"
        if spread < -1.0: status = "DESCONTO"
        elif spread > 1.0: status = "ÁGIO"

        opportunities.append({
            "asset": "PETR4 / PBR",
            "local_price": petr4,
            "global_price_brl": fair_price,
            "spread_pct": round(spread, 2),
            "status": status,
            "timestamp": datetime.now()
        })
    else:
        print("   ⚠️ Pulei PETR4: Faltam dados.")

    # CÁLCULO VALE
    if vale3 > 0 and vale > 0:
        fair_vale = vale * usd
        spread_v = ((vale3 - fair_vale) / fair_vale) * 100
        
        status_v = "NEUTRO"
        if spread_v < -0.8: status_v = "LONG VALE"
        elif spread_v > 0.8: status_v = "SHORT VALE"

        opportunities.append({
            "asset": "VALE3 / VALE",
            "local_price": vale3,
            "global_price_brl": fair_vale,
            "spread_pct": round(spread_v, 2),
            "status": status_v,
            "timestamp": datetime.now()
        })
    else:
        print("   ⚠️ Pulei VALE: Faltam dados.")

    print(f"   📤 Retornando {len(opportunities)} oportunidades.\n")
    return opportunities

@app.get("/portfolio", response_model=PortfolioSchema)
def get_portfolio():
    return {
        "net_worth": 95450.00,
        "allocation": [{"name": "Ações BR", "value": 45000, "color": "#06b6d4"}],
        "risk_matrix": [{"subject": "Volatilidade", "A": 85, "fullMark": 100}],
        "positions": [{"ticker": "PETR4", "type": "Stock", "side": "LONG", "profit": 12.5}],
        "insight": {"title": "ALERTA", "message": "Mercado Volátil", "suggestion": "Hedge em Dólar."}
    }
