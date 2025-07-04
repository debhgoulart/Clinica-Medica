import tkinter as tk
from tkinter import ttk
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

def cadastrar_medico():

    nome = nome_entry.get()
    crm = crm_entry.get()
    especialidade = especialidade_entry.get()
    horarios = horarios_entry.get()
    email = email_entry.get()
    senha = senha_entry.get()

    campos = [nome, crm, especialidade, horarios, email, senha]
    placeholders = ["Nome Completo", "CRM", "Especialidade", "Ex: Seg-Sex 08:00-12:00", "Email (será seu usuário)", "Senha"]
    
    for i, campo in enumerate(campos):
        if not campo or campo == placeholders[i]:
            messagebox.showwarning("Campo Vazio", f"Por favor, preencha o campo: {placeholders[i]}")
            return

    conn = None
    cursor = None
    try:
        conn = conectar()
        if conn is None:
            return

        cursor = conn.cursor()

        sql_medico = "INSERT INTO medicos (crm, nome, especialidade, horarios) VALUES (%s, %s, %s, %s)"
        val_medico = (crm, nome, especialidade, horarios)
        cursor.execute(sql_medico, val_medico)

        sql_usuario = "INSERT INTO usuarios (email, senha, tipo, medico_crm) VALUES (%s, %s, %s, %s)"
        val_usuario = (email, senha, 'medico', crm)
        cursor.execute(sql_usuario, val_usuario)

        conn.commit()

        messagebox.showinfo("Sucesso", "Médico cadastrado com sucesso!")
        tela.destroy()

    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro no Cadastro", f"Ocorreu um erro: {err}")
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

def abrir_tela_cadastro(janela_pai):
    global tela, nome_entry, crm_entry, especialidade_entry, horarios_entry, email_entry, senha_entry
    
    tela = tk.Toplevel(janela_pai)
    tela.title("Cadastro de Médico")
    tela.geometry("450x700")
    tela.configure(bg=COR_FUNDO)
    tela.resizable(False, False)
    tela.transient(janela_pai)
    tela.grab_set()

    main_frame = tk.Frame(tela, bg=COR_FUNDO)
    main_frame.pack(expand=True, padx=20, pady=20)

    title_label = tk.Label(main_frame, text="Cadastro de Médico", font=FONTE_TITULO, fg=COR_TEXTO, bg=COR_FUNDO)
    title_label.pack(pady=(0, 20))

    campos_para_criar = {
        "Nome Completo": "nome_entry",
        "CRM": "crm_entry",
        "Especialidade": "especialidade_entry",
        "Horários": "horarios_entry",
        "Email (será seu usuário)": "email_entry",
        "Senha": "senha_entry"
    }
    
    placeholders = {
        "Horários": "Ex: Seg-Sex 08:00-12:00"
    }

    for placeholder, var_name in campos_para_criar.items():
        entry_placeholder = placeholders.get(placeholder, placeholder)
        
        entry = tk.Entry(main_frame, font=FONTE_LABEL, width=35, relief="solid", bd=1, fg='grey')
        entry.insert(0, entry_placeholder)
        entry.bind('<FocusIn>', lambda event, e=entry, p=entry_placeholder: on_entry_click(event, e, p))
        entry.bind('<FocusOut>', lambda event, e=entry, p=entry_placeholder: on_focusout(event, e, p))
        entry.pack(pady=10, ipady=5)
        globals()[var_name] = entry

    cadastrar_btn = tk.Button(
        main_frame,
        text="Finalizar Cadastro",
        font=FONTE_BOTAO,
        bg=COR_PRINCIPAL,
        fg=COR_BOTAO_TEXTO,
        relief="flat",
        width=32,
        pady=8,
        activebackground="#3CB371",
        command=cadastrar_medico
    )
    cadastrar_btn.pack(pady=20)
