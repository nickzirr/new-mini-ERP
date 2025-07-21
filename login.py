import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# === CONFIGURAÇÕES ===
DB_PATH = os.path.join("db", "loja_roupas.db")


# === BANCO DE DADOS ===
def criar_tabela_usuarios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


# === AÇÕES ===
def cadastrar_usuario():
    nome = entry_nome.get()
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if not nome or not usuario or not senha:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (nome, usuario, senha) VALUES (?, ?, ?)",
                       (nome, usuario, senha))
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_usuario.delete(0, tk.END)
        entry_senha.delete(0, tk.END)
        frame_cadastro.pack_forget()
        frame_login.pack()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Nome de usuário já existe.")
    finally:
        conn.close()


def fazer_login():
    usuario = login_usuario.get()
    senha = login_senha.get()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        messagebox.showinfo("Login", f"Bem-vindo(a), {resultado[1]}!")
        root.destroy()
        from visualizar_user import mostrar_tela_usuario
        mostrar_tela_usuario(resultado[1])
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")


# === INTERFACE ===
def ir_para_cadastro():
    frame_login.pack_forget()
    frame_cadastro.pack()


def voltar_para_login():
    frame_cadastro.pack_forget()
    frame_login.pack()


# === INICIAR ===
criar_tabela_usuarios()

root = tk.Tk()
root.title("Login - Loja de Roupas")
root.geometry("400x350")
root.configure(bg="#f4f4f4")

# === TELA DE LOGIN ===
frame_login = tk.Frame(root, bg="#f4f4f4")
frame_login.pack()

tk.Label(frame_login, text="Login", font=("Arial", 18, "bold"), bg="#f4f4f4").pack(pady=20)

tk.Label(frame_login, text="Usuário:", bg="#f4f4f4").pack()
login_usuario = ttk.Entry(frame_login, width=30)
login_usuario.pack(pady=5)

tk.Label(frame_login, text="Senha:", bg="#f4f4f4").pack()
login_senha = ttk.Entry(frame_login, show="*", width=30)
login_senha.pack(pady=5)

ttk.Button(frame_login, text="Entrar", command=fazer_login).pack(pady=15)
ttk.Button(frame_login, text="Cadastrar novo usuário", command=ir_para_cadastro).pack()

# === TELA DE CADASTRO ===
frame_cadastro = tk.Frame(root, bg="#f4f4f4")

tk.Label(frame_cadastro, text="Cadastrar Usuário", font=("Arial", 18, "bold"), bg="#f4f4f4").pack(pady=20)

tk.Label(frame_cadastro, text="Nome completo:", bg="#f4f4f4").pack()
entry_nome = ttk.Entry(frame_cadastro, width=30)
entry_nome.pack(pady=5)

tk.Label(frame_cadastro, text="Usuário:", bg="#f4f4f4").pack()
entry_usuario = ttk.Entry(frame_cadastro, width=30)
entry_usuario.pack(pady=5)

tk.Label(frame_cadastro, text="Senha:", bg="#f4f4f4").pack()
entry_senha = ttk.Entry(frame_cadastro, show="*", width=30)
entry_senha.pack(pady=5)

ttk.Button(frame_cadastro, text="Salvar cadastro", command=cadastrar_usuario).pack(pady=15)
ttk.Button(frame_cadastro, text="Voltar ao login", command=voltar_para_login).pack()

root.mainloop()
