# produtos/main.py

import sys
import os
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Ajusta o path para importar model.database se necessário (pode remover se não usar)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DB_NAME = 'loja.db'

# --- Funções Banco de Dados ---

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        preco REAL NOT NULL,
        id_categoria INTEGER,
        quantidade INTEGER NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,  -- 'receita' ou 'despesa'
        valor REAL NOT NULL,
        descricao TEXT,
        data TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def inserir_categoria(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categoria WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    if resultado:
        conn.close()
        return resultado[0]
    cursor.execute("INSERT INTO categoria (nome) VALUES (?)", (nome,))
    conn.commit()
    id_cat = cursor.lastrowid
    conn.close()
    return id_cat

def inserir_produto(nome, descricao, preco, id_categoria, quantidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO produto (nome, descricao, preco, id_categoria, quantidade) VALUES (?, ?, ?, ?, ?)
    """, (nome, descricao, preco, id_categoria, quantidade))
    conn.commit()
    conn.close()

def excluir_produto_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produto WHERE nome = ?", (nome,))
    afetados = cursor.rowcount
    conn.commit()
    conn.close()
    return afetados > 0

def buscar_produto_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.nome, p.descricao, p.preco, c.nome, p.quantidade
    FROM produto p
    LEFT JOIN categoria c ON p.id_categoria = c.id
    WHERE p.nome = ?
    """, (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def atualizar_produto(nome_original, novo_nome, descricao, preco, id_categoria, quantidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE produto
    SET nome = ?, descricao = ?, preco = ?, id_categoria = ?, quantidade = ?
    WHERE nome = ?
    """, (novo_nome, descricao, preco, id_categoria, quantidade, nome_original))
    afetados = cursor.rowcount
    conn.commit()
    conn.close()
    return afetados > 0

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.nome, p.descricao, c.nome, p.preco, p.quantidade
    FROM produto p
    LEFT JOIN categoria c ON p.id_categoria = c.id
    ORDER BY p.nome
    """)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# --- Funções financeiras ---

def inserir_transacao(tipo, valor, descricao, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO transacao (tipo, valor, descricao, data) VALUES (?, ?, ?, ?)
    """, (tipo, valor, descricao, data))
    conn.commit()
    conn.close()

def listar_transacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, tipo, valor, descricao, data FROM transacao ORDER BY data DESC")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# --- Interface gráfica ---

criar_tabelas()

root = tk.Tk()
root.title("Loja de Roupas - Produtos e Financeiro")
root.geometry("1000x900")
root.configure(bg="#e0e0e0")

# ---------- Funções interface produtos -----------

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

    id_categoria = inserir_categoria(categoria)
    inserir_produto(nome, descricao, preco, id_categoria, quantidade)

    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
    limpar_campos_produto()

def limpar_campos_produto():
    entry_nome.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    combo_categoria.set('')
    entry_excluir.delete(0, tk.END)
    entry_atualizar_nome.delete(0, tk.END)

def excluir_produto():
    nome = entry_excluir.get()
    if not nome:
        messagebox.showwarning("Atenção", "Informe o nome do produto a ser excluído.")
        return

    sucesso = excluir_produto_por_nome(nome)
    if sucesso:
        messagebox.showinfo("Sucesso", f"Produto '{nome}' excluído.")
    else:
        messagebox.showerror("Erro", f"Produto '{nome}' não encontrado.")
    entry_excluir.delete(0, tk.END)

def carregar_dados_produto():
    nome_original = entry_atualizar_nome.get()
    if not nome_original:
        messagebox.showwarning("Atenção", "Informe o nome do produto que deseja editar.")
        return

    resultado = buscar_produto_por_nome(nome_original)
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

    if not nome_original or not novo_nome or not preco or not categoria or not quantidade:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos obrigatórios!")
        return

    try:
        preco = float(preco)
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showerror("Erro", "Preço ou quantidade inválida.")
        return

    id_categoria = inserir_categoria(categoria)
    sucesso = atualizar_produto(nome_original, novo_nome, descricao, preco, id_categoria, quantidade)
    if sucesso:
        messagebox.showinfo("Sucesso", f"Produto '{nome_original}' atualizado.")
        limpar_campos_produto()
    else:
        messagebox.showerror("Erro", f"Produto '{nome_original}' não encontrado.")

def mostrar_produtos():
    produtos = listar_produtos()
    janela = tk.Toplevel(root)
    janela.title("Produtos Cadastrados")
    janela.geometry("900x400")

    tree = ttk.Treeview(janela, columns=("Nome", "Descrição", "Categoria", "Preço", "Quantidade"), show="headings")
    for col in ("Nome", "Descrição", "Categoria", "Preço", "Quantidade"):
        tree.heading(col, text=col)
        tree.column(col, width=150)

    for produto in produtos:
        tree.insert("", tk.END, values=produto)

    tree.pack(fill="both", expand=True)

# ---------- Funções interface financeira -----------

def adicionar_transacao():
    tipo = combo_tipo.get()
    valor = entry_valor.get()
    descricao = entry_descricao_transacao.get()

    if not tipo or not valor:
        messagebox.showwarning("Campos obrigatórios", "Preencha tipo e valor!")
        return

    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido!")
        return

    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    inserir_transacao(tipo, valor, descricao, data)

    messagebox.showinfo("Sucesso", "Transação registrada!")
    limpar_campos_financeiro()
    mostrar_transacoes()

def limpar_campos_financeiro():
    combo_tipo.set('')
    entry_valor.delete(0, tk.END)
    entry_descricao_transacao.delete(0, tk.END)

def mostrar_transacoes():
    transacoes = listar_transacoes()
    janela = tk.Toplevel(root)
    janela.title("Transações Financeiras")
    janela.geometry("900x400")

    tree = ttk.Treeview(janela, columns=("ID", "Tipo", "Valor", "Descrição", "Data"), show="headings")
    for col in ("ID", "Tipo", "Valor", "Descrição", "Data"):
        tree.heading(col, text=col)
        tree.column(col, width=150)

    for t in transacoes:
        tree.insert("", tk.END, values=t)

    tree.pack(fill="both", expand=True)

# ---------- Interface Gráfica ----------

# Título e frame do cadastro de produtos
tk.Label(root, text="Cadastro de Produtos", font=("Arial", 20, "bold"), bg="#e0e0e0").pack(pady=15)
form = tk.Frame(root, bg="#e0e0e0")
form.pack(pady=10)

labels = ["Nome:", "Descrição:", "Preço (R$):", "Quantidade:", "Categoria:"]
for i, texto in enumerate(labels):
    tk.Label(form, text=texto, bg="#e0e0e0").grid(row=i, column=0, sticky="e", padx=10, pady=5)

entry_nome = ttk.Entry(form, width=40)
entry_nome.grid(row=0, column=1)
entry_descricao = ttk.Entry(form, width=40)
entry_descricao.grid(row=1, column=1)
entry_preco = ttk.Entry(form, width=20)
entry_preco.grid(row=2, column=1, sticky="w")
entry_quantidade = ttk.Entry(form, width=20)
entry_quantidade.grid(row=3, column=1, sticky="w")
combo_categoria = ttk.Combobox(form, values=["Camisa", "Calça", "Vestido", "Jaqueta", "Acessório"], width=37)
combo_categoria.grid(row=4, column=1)

btn_frame = tk.Frame(root, bg="#e0e0e0")
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Salvar Produto", command=adicionar_produto).grid(row=0, column=0, padx=10)

entry_excluir = ttk.Entry(btn_frame, width=25)
entry_excluir.grid(row=1, column=0, padx=10)
ttk.Button(btn_frame, text="Excluir Produto", command=excluir_produto).grid(row=1, column=1, padx=10)

entry_atualizar_nome = ttk.Entry(btn_frame, width=25)
entry_atualizar_nome.grid(row=2, column=0, padx=10)
ttk.Button(btn_frame, text="Carregar Dados", command=carregar_dados_produto).grid(row=2, column=1, padx=10)
ttk.Button(btn_frame, text="Salvar Alterações", command=salvar_alteracoes_produto).grid(row=2, column=2, padx=10)

ttk.Button(root, text="Visualizar Produtos", command=mostrar_produtos).pack(pady=10)

# Interface financeira
tk.Label(root, text="Controle Financeiro", font=("Arial", 20, "bold"), bg="#e0e0e0").pack(pady=15)
financeiro_frame = tk.Frame(root, bg="#e0e0e0")
financeiro_frame.pack(pady=10)

tk.Label(financeiro_frame, text="Tipo (Receita/Despesa):", bg="#e0e0e0").grid(row=0, column=0, sticky="e", padx=10, pady=5)
combo_tipo = ttk.Combobox(financeiro_frame, values=["receita", "despesa"], width=37)
combo_tipo.grid(row=0, column=1)

tk.Label(financeiro_frame, text="Valor (R$):", bg="#e0e0e0").grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_valor = ttk.Entry(financeiro_frame, width=40)
entry_valor.grid(row=1, column=1)

tk.Label(financeiro_frame, text="Descrição:", bg="#e0e0e0").grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_descricao_transacao = ttk.Entry(financeiro_frame, width=40)
entry_descricao_transacao.grid(row=2, column=1)

ttk.Button(financeiro_frame, text="Adicionar Transação", command=adicionar_transacao).grid(row=3, column=1, pady=10, sticky="w")

ttk.Button(root, text="Visualizar Transações", command=mostrar_transacoes).pack(pady=10)

root.mainloop()
