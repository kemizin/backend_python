import sqlite3
from typing import Optional, List, Dict
from security import verify_password

DB_NAME = "meu_banco.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def get_user(username: str) -> Optional[Dict]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user, senha FROM usuarios WHERE user = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"user": row[0], "senha": row[1]}
    return None

def create_user(username: str, senha: str) -> bool:
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (user, senha) VALUES (?, ?)", (username, senha))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def list_users() -> List[Dict]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user FROM usuarios")
    rows = cursor.fetchall()
    conn.close()
    return [{"user": row[0]} for row in rows]

def update_user(old_username: str, new_username: str, senha: str) -> bool:
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET user = ?, senha = ? WHERE user = ?", (new_username, senha, old_username))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_user(username: str, senha: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE user = ?", (username,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False  # usuário não existe
    
    senha_hash = row[0]
    if not verify_password(senha, senha_hash):
        conn.close()
        return False  # senha incorreta

    cursor.execute("DELETE FROM usuarios WHERE user = ?", (username,))
    conn.commit()
    conn.close()
    return True

# Inicializa o banco ao importar
init_db()
