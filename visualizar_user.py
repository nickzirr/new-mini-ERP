import tkinter as tk
from tkinter import ttk
import sqlite3
import os

DB_PATH = os.path.join("db", "loja_roupas.db")

def mostrar_tela_usuario(nome_usuario):
    root = tk.Tk()
    root.title(f"Bem-vindo, {nome_usuario}")
    root.geometry("700x400")
    root.configure(bg="#f8f8f8")

    tk.Label(root, text=f"Produtos disponíveis", font=("Arial", 16, "bold"), bg="#f8f8f8").pack(pady=10)

    frame = tk.Frame(root, bg="#f8f8f8")
    frame.pack(pady=10, fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#e8e8e8")
    style.configure("Treeview", font=("Arial", 10), rowheight=28)

    cols = ("Nome", "Descrição", "Preço (R$)", "Categoria")
    tree = ttk.Treeview(frame, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # Carregar produtos do banco
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.nome, p.descricao, p.preco, c.nome
        FROM produtos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        ORDER BY p.nome ASC
    ''')
    produtos = cursor.fetchall()
    conn.close()

    for produto in produtos:
        tree.insert("", "end", values=produto)

    root.mainloop()
