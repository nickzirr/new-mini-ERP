# produtos/main.py

import sys
import os

# Garante que o diretório pai (onde está a pasta model) esteja no caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from model.database import (
    criar_tabelas, inserir_categoria, inserir_produto,
    excluir_produto_por_nome, buscar_produto_por_nome,
    atualizar_produto, listar_produtos
)

criar_tabelas()

root = tk.Tk()
root.title("Cadastro de Produtos - Loja de Roupas")
root.geometry("1920x1080")
root.configure(bg="#e0e0e0")

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
    limpar_campos()

def limpar_campos():
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
        limpar_campos()
    else:
        messagebox.showerror("Erro", f"Produto '{nome_original}' não encontrado.")

def mostrar_produtos():
    produtos = listar_produtos()
    janela = tk.Toplevel(root)
    janela.title("Produtos Cadastrados")
    janela.geometry("1000x500")

    tree = ttk.Treeview(janela, columns=("Nome", "Descrição", "Categoria", "Preço", "Quantidade"), show="headings")
    for col in ("Nome", "Descrição", "Categoria", "Preço", "Quantidade"):
        tree.heading(col, text=col)
        tree.column(col, width=180)

    for produto in produtos:
        tree.insert("", tk.END, values=produto)

    tree.pack(fill="both", expand=True)

# Interface Gráfica

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

# Excluir produto
entry_excluir = ttk.Entry(btn_frame, width=25)
entry_excluir.grid(row=1, column=0, padx=10)
ttk.Button(btn_frame, text="Excluir Produto", command=excluir_produto).grid(row=1, column=1, padx=10)

# Atualizar produto
entry_atualizar_nome = ttk.Entry(btn_frame, width=25)
entry_atualizar_nome.grid(row=2, column=0, padx=10)
ttk.Button(btn_frame, text="Carregar Dados", command=carregar_dados_produto).grid(row=2, column=1, padx=10)
ttk.Button(btn_frame, text="Salvar Alterações", command=salvar_alteracoes_produto).grid(row=2, column=2, padx=10)

# Visualizar produtos
ttk.Button(root, text="Visualizar Produtos", command=mostrar_produtos).pack(pady=10)

root.mainloop()
