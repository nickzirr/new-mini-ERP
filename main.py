import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Garante que a pasta db/ exista
if not os.path.exists("db"):
    os.makedirs("db")

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

    cursor.execute("INSERT OR IGNORE INTO categorias (nome) VALUES (?)", (categoria,))
    conn.commit()

    cursor.execute("SELECT id FROM categorias WHERE nome = ?", (categoria,))
    id_categoria = cursor.fetchone()[0]

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

    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

    entry_nome.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    combo_categoria.set('')

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

def carregar_dados_produto():
    nome_original = entry_atualizar_nome.get()

    if not nome_original:
        messagebox.showwarning("Atenção", "Informe o nome do produto que deseja editar.")
        return

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.nome, p.descricao, p.preco, c.nome, e.quantidade
        FROM produtos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        LEFT JOIN estoque e ON p.id = e.id_produto
        WHERE p.nome = ?
    ''', (nome_original,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        entry_nome.delete(0, tk.END)
        entry_descricao.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)
        combo_categoria.set('')

        entry_nome.insert(0, resultado[0])
        entry_descricao.insert(0, resultado[1])
        entry_preco.insert(0, str(resultado[2]))
        combo_categoria.set(resultado[3])
        entry_quantidade.insert(0, str(resultado[4]))

        messagebox.showinfo("Editar Produto", "Altere os dados e clique em 'Salvar Alterações'.")
    else:
        messagebox.showerror("Erro", f"Produto '{nome_original}' não encontrado.")

def salvar_alteracoes_produto():
    nome_original = entry_atualizar_nome.get()
    novo_nome = entry_nome.get()
    descricao = entry_descricao.get()
    preco = entry_preco.get()
    categoria = combo_categoria.get()
    quantidade = entry_quantidade.get()

    if not nome_original:
        messagebox.showwarning("Atenção", "Informe o nome original do produto.")
        return

    if not novo_nome or not preco or not categoria or not quantidade:
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

    cursor.execute("SELECT id FROM produtos WHERE nome = ?", (nome_original,))
    resultado = cursor.fetchone()

    if resultado:
        id_produto = resultado[0]

        cursor.execute("INSERT OR IGNORE INTO categorias (nome) VALUES (?)", (categoria,))
        conn.commit()

        cursor.execute("SELECT id FROM categorias WHERE nome = ?", (categoria,))
        id_categoria = cursor.fetchone()[0]

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
        messagebox.showinfo("Sucesso", f"Produto '{nome_original}' atualizado.")
    else:
        messagebox.showerror("Erro", f"Produto '{nome_original}' não encontrado.")

    conn.close()

def mostrar_produtos():
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

    janela = tk.Toplevel(root)
    janela.title("Produtos Cadastrados")
    janela.geometry("800x400")

    tree = ttk.Treeview(janela, columns=("Nome", "Descrição", "Categoria", "Preço", "Quantidade"), show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Categoria", text="Categoria")
    tree.heading("Preço", text="Preço (R$)")
    tree.heading("Quantidade", text="Quantidade")

    for produto in produtos:
        tree.insert("", tk.END, values=produto)

    tree.pack(fill="both", expand=True)

criar_tabelas()

root = tk.Tk()
root.title("Cadastro de Produtos - Loja de Roupas")
root.geometry("1920x1080")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Cadastrar Novo Produto", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=15)

form = tk.Frame(root, bg="#f0f0f0")
form.pack(pady=10)

tk.Label(form, text="Nome:", bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=10, pady=5)
entry_nome = ttk.Entry(form, width=40)
entry_nome.grid(row=0, column=1)

tk.Label(form, text="Descrição:", bg="#f0f0f0").grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_descricao = ttk.Entry(form, width=40)
entry_descricao.grid(row=1, column=1)

tk.Label(form, text="Preço (R$):", bg="#f0f0f0").grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_preco = ttk.Entry(form, width=20)
entry_preco.grid(row=2, column=1, sticky="w")

tk.Label(form, text="Quantidade:", bg="#f0f0f0").grid(row=3, column=0, sticky="e", padx=10, pady=5)
entry_quantidade = ttk.Entry(form, width=20)
entry_quantidade.grid(row=3, column=1, sticky="w")

tk.Label(form, text="Categoria:", bg="#f0f0f0").grid(row=4, column=0, sticky="e", padx=10, pady=5)
combo_categoria = ttk.Combobox(form, values=["Camisa", "Calça", "Vestido", "Jaqueta", "Acessório"], width=37)
combo_categoria.grid(row=4, column=1)

ttk.Button(root, text="Salvar Produto", command=adicionar_produto).pack(pady=10)

frame_excluir = tk.Frame(root, bg="#f0f0f0")
frame_excluir.pack(pady=10)

tk.Label(frame_excluir, text="Excluir Produto pelo Nome:", bg="#f0f0f0").grid(row=0, column=0, padx=10)
entry_excluir = ttk.Entry(frame_excluir, width=25)
entry_excluir.grid(row=0, column=1)
ttk.Button(frame_excluir, text="Excluir", command=excluir_produto).grid(row=0, column=2, padx=10)

frame_atualizar = tk.Frame(root, bg="#f0f0f0")
frame_atualizar.pack(pady=10)

tk.Label(frame_atualizar, text="Atualizar Produto (nome atual):", bg="#f0f0f0").grid(row=0, column=0, padx=10)
entry_atualizar_nome = ttk.Entry(frame_atualizar, width=25)
entry_atualizar_nome.grid(row=0, column=1)
ttk.Button(frame_atualizar, text="Carregar Dados", command=carregar_dados_produto).grid(row=0, column=2, padx=10)
ttk.Button(frame_atualizar, text="Salvar Alterações", command=salvar_alteracoes_produto).grid(row=0, column=3, padx=10)

ttk.Button(root, text="Visualizar Produtos", command=mostrar_produtos).pack(pady=15)

root.mainloop()
