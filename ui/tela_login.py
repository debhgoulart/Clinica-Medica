import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import messagebox
from database import conectar
from tela_home_adm import abrir_tela_home_adm

COR_FUNDO = "#FFFFFF"
COR_PRINCIPAL = "#2E8B57"
COR_TEXTO = "#000000"
COR_BOTAO_TEXTO = "#FFFFFF"
FONTE_TITULO = ("Arial", 24, "bold")
FONTE_LABEL = ("Arial", 12)
FONTE_BOTAO = ("Arial", 12, "bold")

def fazer_login():
    tipo = tipo_login_combo.get().lower()
    email = email_entry.get()
    senha = senha_entry.get()

    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM usuarios
            WHERE email = %s AND senha = %s AND tipo = %s AND ativo = TRUE
        """
        cursor.execute(query, (email, senha, tipo))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            if usuario['tipo'] == 'administrador':
                abrir_tela_home_adm()
            elif usuario['tipo'] == 'medico':
                messagebox.showinfo("Login", f"Login médico bem-sucedido! CRM: {usuario['medico_crm']}")
            else:
                messagebox.showerror("Erro", "Tipo de usuário desconhecido.")
        else:
            messagebox.showerror("Erro", "Credenciais inválidas ou usuário inativo.")

    except Exception as e:
        messagebox.showerror("Erro de conexão", f"Erro ao conectar: {e}")



def on_entry_click(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.insert(0, '')
        entry.config(fg='black')
        if placeholder == 'Senha':
            entry.config(show='*')

def on_focusout(event, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg='grey')
        if placeholder == 'Senha':
            entry.config(show='')


#janela
janela = tk.Tk()
janela.title("Login - Clínica Médica")
janela.geometry("400x550")
janela.configure(bg=COR_FUNDO)
janela.resizable(False, False)

main_frame = tk.Frame(janela, bg=COR_FUNDO)
main_frame.pack(expand=True)

#componentes de tela
logo_label = tk.Label(main_frame, text="+", font=("Arial", 60, "bold"), fg=COR_PRINCIPAL, bg=COR_FUNDO)
logo_label.pack(pady=(0, 10))

title_label = tk.Label(main_frame, text="Login", font=FONTE_TITULO, fg=COR_TEXTO, bg=COR_FUNDO)
title_label.pack(pady=(0, 20))

tipo_label = tk.Label(main_frame, text="Tipo de Login", font=FONTE_LABEL, bg=COR_FUNDO, fg='grey')
tipo_label.pack(pady=(10,0))

tipo_login_combo = ttk.Combobox(
    main_frame,
    values=["Médico", "Administrador"],
    font=FONTE_LABEL,
    width=28,
    state="readonly"
)
tipo_login_combo.set("Médico")
tipo_login_combo.pack(pady=5, ipady=3)

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

login_button = tk.Button(
    main_frame,
    text="Login",
    font=FONTE_BOTAO,
    bg=COR_PRINCIPAL,
    fg=COR_BOTAO_TEXTO,
    relief="flat",
    width=28,
    pady=8,
    activebackground="#3CB371",
    command=fazer_login
)
login_button.pack(pady=20)

janela.mainloop()