import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText
import streamlit as st
import random
import string
import requests
import urllib.parse

# --- 1. BANCO DE DADOS (SQLite Local) ---
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (email TEXT PRIMARY KEY, password TEXT, name TEXT)''')
    conn.commit()
    conn.close()

def hash_pass(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def create_user(email, password, name):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password, name) VALUES (?, ?, ?)", 
                  (email, hash_pass(password), name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_login(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", 
              (email, hash_pass(password)))
    data = c.fetchall()
    conn.close()
    return data

# --- 2. GERADOR DE CREDENCIAIS ---
def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$"
    return ''.join(random.choice(chars) for i in range(10))

# --- 3. DISPARO DE EMAIL (Desativado/Simulado) ---
def send_confirmation_email(email, name, password):
    # Função mantida para compatibilidade, mas não envia sem SMTP configurado
    return True

# --- 4. DISPARO WHATSAPP (CallMeBot) ---
def send_whatsapp_admin(email, name, password):
    # ⚠️ CONFIGURE AQUI SEUS DADOS REAIS SE QUISER RECEBER
    phone = "5541999999999"  # Seu celular com DDD
    apikey = "123456"        # Sua API Key do CallMeBot
    
    message = f"""
    🌪️ *INTELLIGENCE FLOW*
    
    👤 *Novo:* {name}
    📧 *Email:* {email}
    🔑 *Senha:* {password}
    """
    
    encoded_msg = urllib.parse.quote(message)
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={encoded_msg}&apikey={apikey}"
    
    try:
        # Timeout curto para não travar o app se a API demorar
        requests.get(url, timeout=5) 
        return True
    except Exception:
        return False
