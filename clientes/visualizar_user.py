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
                SELECT p.nome, p.descricao, p.preco, c.nome, 
                       COALESCE(e.quantidade, 0)
                FROM produtos p
                LEFT JOIN categorias c ON p.id_categoria = c.id
                LEFT JOIN estoque e ON p.id = e.id_produto
                ORDER BY p.nome ASC
            ''')
        else:
            cursor.execute('''
                SELECT p.nome, p.descricao, p.preco, c.nome, 
                       COALESCE(e.quantidade, 0)
                FROM produtos p
                LEFT JOIN categorias c ON p.id_categoria = c.id
                LEFT JOIN estoque e ON p.id = e.id_produto
                WHERE c.nome = ?
                ORDER BY p.nome ASC
            ''', (categoria_selecionada,))
        
        produtos = cursor.fetchall()
        conn.close()

        for item in tree.get_children():
            tree.delete(item)
        
        for produto in produtos:
            tree.insert("", "end", values=produto)

    def filtrar():
        categoria = combo_categoria.get()
        carregar_produtos(categoria)

    # === Interface Tkinter ===
    root = tk.Tk()
    root.title(f"Bem-vindo, {nome_usuario}")
    root.geometry("1920x1080")
    root.configure(bg="#2e2e2e")

    # Título
    tk.Label(root, text="Produtos da Loja", font=("Arial", 24, "bold"), bg="#2e2e2e", fg="#cccccc").pack(pady=20)

    # Filtro de categoria
    frame_filtro = tk.Frame(root, bg="#2e2e2e")
    frame_filtro.pack(pady=10)

    tk.Label(frame_filtro, text="Filtrar por categoria:", font=("Arial", 12), bg="#2e2e2e", fg="#cccccc").grid(row=0, column=0, padx=10)

    combo_categoria = ttk.Combobox(frame_filtro, values=carregar_categorias(), state="readonly", width=30, font=("Arial", 11))
    combo_categoria.grid(row=0, column=1, padx=10)
    combo_categoria.set("Todas")

    ttk.Button(frame_filtro, text="Filtrar", command=filtrar).grid(row=0, column=2, padx=10)

    # Tabela
    frame_tabela = tk.Frame(root, bg="#2e2e2e")
    frame_tabela.pack(padx=20, pady=20, fill="both", expand=True)

    colunas = ("Nome", "Descrição", "Preço (R$)", "Categoria", "Estoque")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=30)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=200)

    # Estilo visual
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    font=("Arial", 12),
                    rowheight=30,
                    background="#3a3a3a",
                    foreground="#cccccc",
                    fieldbackground="#3a3a3a")
    style.configure("Treeview.Heading",
                    font=("Arial", 12, "bold"),
                    background="#444444",
                    foreground="#cccccc")

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(fill="both", expand=True)

    carregar_produtos()  # carrega tudo inicialmente

    root.mainloop()
