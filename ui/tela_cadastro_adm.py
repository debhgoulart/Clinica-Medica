import tkinter as tk
from tkinter import messagebox
from database import conectar
import mysql.connector

COR_FUNDO = "#FFFFFF"
COR_PRINCIPAL = "#2E8B57"
COR_TEXTO = "#000000"
COR_BOTAO_TEXTO = "#FFFFFF"
FONTE_TITULO = ("Arial", 24, "bold")
FONTE_LABEL = ("Arial", 12)
FONTE_BOTAO = ("Arial", 12, "bold")

def cadastrar_administrador():
    email = email_entry.get()
    senha = senha_entry.get()

    if not email or email == "Email" or not senha or senha == "Senha":
        messagebox.showwarning("Campos Vazios", "Por favor, preencha o email e a senha.")
        return

    conn = None
    cursor = None
    try:
        conn = conectar()
        if conn is None:
            return 

        cursor = conn.cursor()

        sql = "INSERT INTO usuarios (email, senha, tipo) VALUES (%s, %s, 'administrador')"
        val = (email, senha)
        cursor.execute(sql, val)
        conn.commit()

        messagebox.showinfo("Sucesso", "Administrador cadastrado com sucesso!")
        tela_adm.destroy()

    except mysql.connector.Error as err:
        messagebox.showerror("Erro no Cadastro", f"Ocorreu um erro: {err}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def on_entry_click(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.config(fg='black')
        if placeholder == 'Senha':
            entry.config(show='*')

def on_focusout(event, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg='grey')
        if placeholder == 'Senha':
            entry.config(show='')

def abrir_tela_cadastro_adm(janela_pai):
    global tela_adm, email_entry, senha_entry
    
    tela_adm = tk.Toplevel(janela_pai)
    tela_adm.title("Cadastro de Administrador")
    tela_adm.geometry("400x400")
    tela_adm.configure(bg=COR_FUNDO)
    tela_adm.resizable(False, False)
    tela_adm.transient(janela_pai)
    tela_adm.grab_set()

    main_frame = tk.Frame(tela_adm, bg=COR_FUNDO)
    main_frame.pack(expand=True, padx=20, pady=20)

    title_label = tk.Label(main_frame, text="Cadastro de ADM", font=FONTE_TITULO, fg=COR_TEXTO, bg=COR_FUNDO)
    title_label.pack(pady=(0, 20))

    email_entry = tk.Entry(main_frame, font=FONTE_LABEL, width=30, relief="solid", bd=1, fg='grey')
    email_entry.insert(0, "Email")
    email_entry.bind('<FocusIn>', lambda event: on_entry_click(event, email_entry, "Email"))
    email_entry.bind('<FocusOut>', lambda event: on_focusout(event, email_entry, "Email"))
    email_entry.pack(pady=10, ipady=5)

    senha_entry = tk.Entry(main_frame, font=FONTE_LABEL, width=30, relief="solid", bd=1, fg='grey')
    senha_entry.insert(0, "Senha")
    senha_entry.bind('<FocusIn>', lambda event: on_entry_click(event, senha_entry, "Senha"))
    senha_entry.bind('<FocusOut>', lambda event: on_focusout(event, senha_entry, "Senha"))
    senha_entry.pack(pady=10, ipady=5)

    cadastrar_btn = tk.Button(
        main_frame,
        text="Finalizar Cadastro",
        font=FONTE_BOTAO,
        bg=COR_PRINCIPAL,
        fg=COR_BOTAO_TEXTO,
        relief="flat",
        width=28,
        pady=8,
        activebackground="#3CB371",
        command=cadastrar_administrador
    )
    cadastrar_btn.pack(pady=20)
