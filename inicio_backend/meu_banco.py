import sqlite3

# Conecta ou cria o banco
conn = sqlite3.connect("meu_banco.db")
cursor = conn.cursor()

# Cria uma tabela exemplo
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

conn.commit()
conn.close()
