# model/database.py
import os
import sqlite3

DB_PATH = os.path.join("db", "loja_roupas.db")

def conectar():
    return sqlite3.connect(DB_PATH)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            id_categoria INTEGER,
            FOREIGN KEY (id_categoria) REFERENCES categorias(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER,
            quantidade INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (id_produto) REFERENCES produtos(id)
        );
    ''')

    conn.commit()
    conn.close()

def inserir_categoria(nome_categoria):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO categorias (nome) VALUES (?)", (nome_categoria,))
    conn.commit()

    cursor.execute("SELECT id FROM categorias WHERE nome = ?", (nome_categoria,))
    id_categoria = cursor.fetchone()[0]

    conn.close()
    return id_categoria

def inserir_produto(nome, descricao, preco, id_categoria, quantidade):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO produtos (nome, descricao, preco, id_categoria)
        VALUES (?, ?, ?, ?)
    ''', (nome, descricao, preco, id_categoria))
    id_produto = cursor.lastrowid

    cursor.execute('''
        INSERT INTO estoque (id_produto, quantidade)
        VALUES (?, ?)
    ''', (id_produto, quantidade))

    conn.commit()
    conn.close()

def excluir_produto_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM produtos WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()

    if resultado:
        id_produto = resultado[0]
        cursor.execute("DELETE FROM estoque WHERE id_produto = ?", (id_produto,))
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def buscar_produto_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.nome, p.descricao, p.preco, c.nome, e.quantidade
        FROM produtos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        LEFT JOIN estoque e ON p.id = e.id_produto
        WHERE p.nome = ?
    ''', (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def atualizar_produto(nome_original, novo_nome, descricao, preco, id_categoria, quantidade):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM produtos WHERE nome = ?", (nome_original,))
    resultado = cursor.fetchone()
    if not resultado:
        conn.close()
        return False

    id_produto = resultado[0]

    cursor.execute('''
        UPDATE produtos
        SET nome = ?, descricao = ?, preco = ?, id_categoria = ?
        WHERE id = ?
    ''', (novo_nome, descricao, preco, id_categoria, id_produto))

    cursor.execute('''
        UPDATE estoque
        SET quantidade = ?
        WHERE id_produto = ?
    ''', (quantidade, id_produto))

    conn.commit()
    conn.close()
    return True

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.nome, p.descricao, c.nome, p.preco, e.quantidade
        FROM produtos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        LEFT JOIN estoque e ON p.id = e.id_produto
    ''')
    produtos = cursor.fetchall()
    conn.close()
    return produtos
