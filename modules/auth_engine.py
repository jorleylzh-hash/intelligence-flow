import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText
import streamlit as st
import random
import string

# --- 1. BANCO DE DADOS (SQLite Local) ---
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Cria tabela se não existir
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
    # Gera uma senha aleatória segura
    chars = string.ascii_letters + string.digits + "!@#$"
    return ''.join(random.choice(chars) for i in range(10))

# --- 3. DISPARO DE EMAIL (SMTP) ---
def send_confirmation_email(email, name, password):
    # ⚠️ CONFIGURAÇÃO DO SEU EMAIL (GMAIL EXEMPLO)
    # Você precisa gerar uma "Senha de App" na sua conta Google
    sender_email = "seu_email@gmail.com"  
    sender_password = "sua_senha_de_app_aqui" 
    
    msg = MIMEText(f"""
    Olá, {name}!
    
    Bem-vindo ao Intelligence Flow. Sua conta Institutional foi ativada.
    
    SEUS DADOS DE ACESSO:
    Login: {email}
    Senha Provisória: {password}
    
    Acesse agora para visualizar o fluxo macro.
    
    Att,
    Equipe Intelligence Flow
    """)
    
    msg['Subject'] = "Acesso Confirmado | Intelligence Flow"
    msg['From'] = sender_email
    msg['To'] = email

    try:
        # Se for testar local sem configurar email, comente as linhas abaixo
        # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # server.login(sender_email, sender_password)
        # server.sendmail(sender_email, email, msg.as_string())
        # server.quit()
        return True
    except Exception as e:
        print(e)
        return False