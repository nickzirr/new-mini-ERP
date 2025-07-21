import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Garante que a pasta db/ exista
if not os.path.exists("db"):
    os.makedirs("db")

DB_PATH = os.path.join("db", "loja_roupas.db")

# Conexão com o banco
def conectar():
    return sqlite3.connect(DB_PATH)

# Criação das tabelas
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

# Adicionar produto com estoque
def adicionar_produto():
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    preco = entry_preco.get()
    categoria = combo_categoria.get()
    quantidade = entry_quantidade.get()

    if not nome or not preco or not categoria or not quantidade:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos obrigatórios!")
        return

    try:
        preco = float(preco)
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showerror("Erro", "Preço ou quantidade inválida.")
        return

    conn = conectar()
    cursor = conn.cursor()

    # Garante que categoria existe
    cursor.execute("INSERT OR IGNORE INTO categorias (nome) VALUES (?)", (categoria,))
    conn.commit()

    # Pega id da categoria
    cursor.execute("SELECT id FROM categorias WHERE nome = ?", (categoria,))
    id_categoria = cursor.fetchone()[0]

    # Insere produto
    cursor.execute('''
        INSERT INTO produtos (nome, descricao, preco, id_categoria)
        VALUES (?, ?, ?, ?)
    ''', (nome, descricao, preco, id_categoria))
    id_produto = cursor.lastrowid

    # Insere no estoque
    cursor.execute('''
        INSERT INTO estoque (id_produto, quantidade)
        VALUES (?, ?)
    ''', (id_produto, quantidade))

    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

    # Limpa os campos
    entry_nome.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    combo_categoria.set('')

# Excluir produto pelo nome
def excluir_produto():
    nome = entry_excluir.get()
    if not nome:
        messagebox.showwarning("Atenção", "Informe o nome do produto a ser excluído.")
        return

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM produtos WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()

    if resultado:
        id_produto = resultado[0]
        cursor.execute("DELETE FROM estoque WHERE id_produto = ?", (id_produto,))
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Produto '{nome}' excluído.")
        entry_excluir.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", f"Produto '{nome}' não encontrado.")

    conn.close()

# Inicializa banco
criar_tabelas()

# === Interface Tkinter ===
root = tk.Tk()
root.title("Cadastro de Produtos - Loja de Roupas")
root.geometry("500x530")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Cadastrar Novo Produto", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=15)

form = tk.Frame(root, bg="#f0f0f0")
form.pack(pady=10)

# Nome
tk.Label(form, text="Nome:", bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=10, pady=5)
entry_nome = ttk.Entry(form, width=40)
entry_nome.grid(row=0, column=1)

# Descrição
tk.Label(form, text="Descrição:", bg="#f0f0f0").grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_descricao = ttk.Entry(form, width=40)
entry_descricao.grid(row=1, column=1)

# Preço
tk.Label(form, text="Preço (R$):", bg="#f0f0f0").grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_preco = ttk.Entry(form, width=20)
entry_preco.grid(row=2, column=1, sticky="w")

# Quantidade
tk.Label(form, text="Quantidade:", bg="#f0f0f0").grid(row=3, column=0, sticky="e", padx=10, pady=5)
entry_quantidade = ttk.Entry(form, width=20)
entry_quantidade.grid(row=3, column=1, sticky="w")

# Categoria
tk.Label(form, text="Categoria:", bg="#f0f0f0").grid(row=4, column=0, sticky="e", padx=10, pady=5)
combo_categoria = ttk.Combobox(form, values=["Camisa", "Calça", "Vestido", "Jaqueta", "Acessório"], width=37)
combo_categoria.grid(row=4, column=1)

# Botão salvar
ttk.Button(root, text="Salvar Produto", command=adicionar_produto).pack(pady=20)

# === Excluir produto ===
frame_excluir = tk.Frame(root, bg="#f0f0f0")
frame_excluir.pack(pady=10)

tk.Label(frame_excluir, text="Excluir Produto pelo Nome:", bg="#f0f0f0").grid(row=0, column=0, padx=10)
entry_excluir = ttk.Entry(frame_excluir, width=25)
entry_excluir.grid(row=0, column=1)
ttk.Button(frame_excluir, text="Excluir", command=excluir_produto).grid(row=0, column=2, padx=10)

root.mainloop()
