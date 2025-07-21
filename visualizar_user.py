import tkinter as tk
from tkinter import ttk
import sqlite3
import os

DB_PATH = os.path.join("db", "loja_roupas.db")

def mostrar_tela_usuario(nome_usuario):
    # === Funções internas ===
    def carregar_categorias():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM categorias ORDER BY nome ASC")
        categorias = [row[0] for row in cursor.fetchall()]
        conn.close()
        return ["Todas"] + categorias

    def carregar_produtos(categoria_selecionada="Todas"):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if categoria_selecionada == "Todas":
            cursor.execute('''
                SELECT p.nome, p.descricao, p.preco, c.nome
                FROM produtos p
                LEFT JOIN categorias c ON p.id_categoria = c.id
                ORDER BY p.nome ASC
            ''')
        else:
            cursor.execute('''
                SELECT p.nome, p.descricao, p.preco, c.nome
                FROM produtos p
                LEFT JOIN categorias c ON p.id_categoria = c.id
                WHERE c.nome = ?
                ORDER BY p.nome ASC
            ''', (categoria_selecionada,))
        
        produtos = cursor.fetchall()
        conn.close()

        # Limpar tabela
        for item in tree.get_children():
            tree.delete(item)
        
        # Preencher tabela
        for produto in produtos:
            tree.insert("", "end", values=produto)

    def filtrar():
        categoria = combo_categoria.get()
        carregar_produtos(categoria)

    # === Interface Tkinter ===
    root = tk.Tk()
    root.title(f"Bem-vindo, {nome_usuario}")
    root.geometry("1920x1080")
    root.configure(bg="#f9f9f9")

    tk.Label(root, text=f"Produtos Disponíveis", font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

    # Filtro de categoria
    frame_filtro = tk.Frame(root, bg="#f9f9f9")
    frame_filtro.pack(pady=5)

    tk.Label(frame_filtro, text="Filtrar por categoria:", bg="#f9f9f9").grid(row=0, column=0, padx=5)

    combo_categoria = ttk.Combobox(frame_filtro, values=carregar_categorias(), state="readonly", width=30)
    combo_categoria.grid(row=0, column=1, padx=5)
    combo_categoria.set("Todas")

    ttk.Button(frame_filtro, text="Filtrar", command=filtrar).grid(row=0, column=2, padx=5)

    # Tabela de produtos
    frame_tabela = tk.Frame(root, bg="#f9f9f9")
    frame_tabela.pack(pady=10, fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#e8e8e8")
    style.configure("Treeview", font=("Arial", 10), rowheight=28)

    colunas = ("Nome", "Descrição", "Preço (R$)", "Categoria")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # Carrega produtos ao iniciar
    carregar_produtos()

    root.mainloop()
