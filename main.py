import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Garante que a pasta db/ exista
if not os.path.exists("db"):
    os.makedirs("db")

# Caminho para o banco de dados
DB_PATH = os.path.join("db", "loja_roupas.db")

# Função para conectar ao banco
def conectar():
    return sqlite3.connect(DB_PATH)

# Função para criar as tabelas necessárias
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

    conn.commit()
    conn.close()

# Função para adicionar produto
def adicionar_produto():
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    preco = entry_preco.get()
    categoria = combo_categoria.get()

    if not nome or not preco or not categoria:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos obrigatórios!")
        return

    try:
        preco = float(preco)
    except ValueError:
        messagebox.showerror("Erro", "Preço inválido.")
        return

    conn = conectar()
    cursor = conn.cursor()

    # Adiciona categoria se não existir
    cursor.execute("INSERT OR IGNORE INTO categorias (nome) VALUES (?)", (categoria,))
    conn.commit()

    # Recupera ID da categoria
    cursor.execute("SELECT id FROM categorias WHERE nome = ?", (categoria,))
    id_categoria = cursor.fetchone()[0]

    # Insere o produto
    cursor.execute('''
        INSERT INTO produtos (nome, descricao, preco, id_categoria)
        VALUES (?, ?, ?, ?)
    ''', (nome, descricao, preco, id_categoria))

    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

    # Limpa os campos
    entry_nome.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    combo_categoria.set('')

# Inicializa banco
criar_tabelas()

# === Interface Tkinter ===
root = tk.Tk()
root.title("Cadastro de Produtos - Loja de Roupas")
root.geometry("480x400")
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

# Categoria
tk.Label(form, text="Categoria:", bg="#f0f0f0").grid(row=3, column=0, sticky="e", padx=10, pady=5)
combo_categoria = ttk.Combobox(form, values=["Camisa", "Calça", "Vestido", "Jaqueta", "Acessório"], width=37)
combo_categoria.grid(row=3, column=1)

# Botão
ttk.Button(root, text="Salvar Produto", command=adicionar_produto).pack(pady=20)

root.mainloop()
