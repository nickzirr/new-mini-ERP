import sqlite3
import os

# Caminho do banco de dados
DB_PATH = os.path.join("db", "loja_roupas.db")

# Conecta ao banco
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Cria a tabela de usuários se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    );
''')

conn.commit()
conn.close()
print("Tabela 'usuarios' criada (ou já existia).")


