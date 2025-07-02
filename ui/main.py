import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import messagebox
from database import conectar
from tela_home_medico import abrir_tela_medico
from tela_home_adm import abrir_tela_admin

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

    if not email or not senha or email == "Email" or senha == "Senha":
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
        return

    try:
        conn = conectar()
        if conn is None:
            return

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM usuarios
            WHERE email = %s AND senha = %s AND tipo = %s AND ativo = TRUE
        """
        cursor.execute(query, (email, senha, tipo))
        usuario = cursor.fetchone()

        if usuario:
            janela.destroy()

            if usuario['tipo'] == 'administrador':
                abrir_tela_admin(usuario['id'])
            
            elif usuario['tipo'] == 'medico':
                abrir_tela_medico(usuario['medico_crm'])
        else:
            messagebox.showerror("Erro de Login", "Credenciais inválidas ou usuário inativo.")

    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao processar o login: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def abrir_tela_de_cadastro_correta():
    tipo_selecionado = tipo_login_combo.get()
    
    if tipo_selecionado == "Médico":
        from tela_cadastro import abrir_tela_cadastro 
        abrir_tela_cadastro(janela)
    elif tipo_selecionado == "Administrador":
        from tela_cadastro_adm import abrir_tela_cadastro_adm
        abrir_tela_cadastro_adm(janela)
    else:
        messagebox.showwarning("Seleção Inválida", "Por favor, selecione um tipo de login para se cadastrar.")


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

janela = tk.Tk()
janela.title("Login - Clínica Médica")
janela.geometry("400x550")
janela.configure(bg=COR_FUNDO)
janela.resizable(False, False)

largura_janela = 400
altura_janela = 550
largura_ecra = janela.winfo_screenwidth()
altura_ecra = janela.winfo_screenheight()
pos_x = (largura_ecra // 2) - (largura_janela // 2)
pos_y = (altura_ecra // 2) - (altura_janela // 2)
janela.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')


main_frame = tk.Frame(janela, bg=COR_FUNDO)
main_frame.pack(expand=True, padx=20, pady=20)

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
login_button.pack(pady=(20, 10))

cadastro_button = tk.Button(
    main_frame,
    text="Cadastrar",
    font=FONTE_BOTAO,
    bg=COR_PRINCIPAL,
    fg=COR_BOTAO_TEXTO,
    relief="flat",
    width=28,
    pady=8,
    activebackground="#3CB371",
    command=abrir_tela_de_cadastro_correta
)
cadastro_button.pack(pady=10)

janela.mainloop()
