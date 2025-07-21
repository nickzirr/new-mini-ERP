import os
import sqlite3
import tkinter as tk
from tkinter import ttk

DB_PATH = os.path.join("db", "loja_roupas.db")

# Função para conectar e buscar os dados
def carregar_produtos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.nome, p.descricao, p.preco, c.nome
        FROM produtos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        ORDER BY p.id DESC
    ''')
    dados = cursor.fetchall()
    conn.close()

    for item in tree.get_children():
        tree.delete(item)

    for produto in dados:
        tree.insert("", "end", values=produto)

# Interface Tkinter
root = tk.Tk()
root.title("Produtos Cadastrados")
root.geometry("700x400")
root.configure(bg="#f5f5f5")

tk.Label(root, text="Lista de Produtos", font=("Arial", 18, "bold"), bg="#f5f5f5").pack(pady=15)

# Frame para a tabela
frame = tk.Frame(root, bg="#f5f5f5")
frame.pack(pady=10)

# Estilo
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#e0e0e0")
style.configure("Treeview", font=("Arial", 10), rowheight=28)

# Tabela
cols = ("Nome", "Descrição", "Preço (R$)", "Categoria")
tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(side="left", fill="both", expand=True)

# Scroll
scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scroll.set)
scroll.pack(side="right", fill="y")

# Botão atualizar
ttk.Button(root, text="Atualizar Lista", command=carregar_produtos).pack(pady=10)

# Carrega dados ao iniciar
carregar_produtos()

root.mainloop()
