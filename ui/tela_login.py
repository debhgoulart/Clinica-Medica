import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk # Importa o módulo ttk

# --- CORES E FONTES ---
COR_FUNDO = "#FFFFFF"  # Branco
COR_PRINCIPAL = "#2E8B57" # Verde Mar (SeaGreen)
COR_TEXTO = "#000000"    # Preto
COR_BOTAO_TEXTO = "#FFFFFF" # Branco
FONTE_TITULO = ("Arial", 24, "bold")
FONTE_LABEL = ("Arial", 12)
FONTE_BOTAO = ("Arial", 12, "bold")


class LoginScreen:
    def __init__(self, master):
        self.master = master
        master.title("Login - Clínica Médica")
        master.geometry("400x550")
        master.configure(bg=COR_FUNDO)
        master.resizable(False, False)

        # --- ESTILO PARA O COMBOBOX (DROPDOWN) ---
        style = ttk.Style(master)
        # Configura a aparência do dropdown quando o mouse está sobre ele
        style.map('TCombobox', fieldbackground=[('readonly','white')])
        style.map('TCombobox', selectbackground=[('readonly', COR_PRINCIPAL)])
        style.map('TCombobox', selectforeground=[('readonly', 'white')])


        # --- FUNÇÕES PARA PLACEHOLDER ---
        def on_entry_click(event, entry, placeholder):
            """Função chamada quando a entrada é clicada."""
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.insert(0, '')
                entry.config(fg='black')
                if placeholder == 'Senha':
                    entry.config(show='*')

        def on_focusout(event, entry, placeholder):
            """Função chamada quando a entrada perde o foco."""
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(fg='grey')
                if placeholder == 'Senha':
                    entry.config(show='')

        # --- WIDGETS ---

        main_frame = tk.Frame(master, bg=COR_FUNDO)
        main_frame.pack(expand=True)

        logo_label = tk.Label(main_frame, text="+", font=("Arial", 60, "bold"), fg=COR_PRINCIPAL, bg=COR_FUNDO)
        logo_label.pack(pady=(0, 10))

        title_label = tk.Label(main_frame, text="Login", font=FONTE_TITULO, fg=COR_TEXTO, bg=COR_FUNDO)
        title_label.pack(pady=(0, 20))

        # NOVO: Label para o Combobox
        tipo_label = tk.Label(main_frame, text="Tipo de Login", font=FONTE_LABEL, bg=COR_FUNDO, fg='grey')
        tipo_label.pack(pady=(10,0))

        # NOVO: Combobox (Dropdown) para selecionar o tipo de usuário
        self.login_type_combo = ttk.Combobox(
            main_frame,
            values=["Médico", "Administrador"],
            font=FONTE_LABEL,
            width=28,
            state="readonly" # Impede que o usuário digite no campo
        )
        self.login_type_combo.set("Médico") # Define o valor padrão
        self.login_type_combo.pack(pady=5, ipady=3)

        self.email_entry = tk.Entry(main_frame, font=FONTE_LABEL, width=30, relief="solid", bd=1, fg='grey')
        self.email_entry.insert(0, "Email")
        self.email_entry.bind('<FocusIn>', lambda event: on_entry_click(event, self.email_entry, "Email"))
        self.email_entry.bind('<FocusOut>', lambda event: on_focusout(event, self.email_entry, "Email"))
        self.email_entry.pack(pady=10, ipady=5)

        self.password_entry = tk.Entry(main_frame, font=FONTE_LABEL, width=30, relief="solid", bd=1, fg='grey')
        self.password_entry.insert(0, "Senha")
        self.password_entry.bind('<FocusIn>', lambda event: on_entry_click(event, self.password_entry, "Senha"))
        self.password_entry.bind('<FocusOut>', lambda event: on_focusout(event, self.password_entry, "Senha"))
        self.password_entry.pack(pady=10, ipady=5)


        # Botão de Login
        login_button = tk.Button(
            main_frame, text="Login", font=FONTE_BOTAO, bg=COR_PRINCIPAL,
            fg=COR_BOTAO_TEXTO, relief="flat", width=28, pady=8,
            activebackground="#3CB371", activeforeground=COR_BOTAO_TEXTO,
            command=self.fazer_login
        )
        login_button.pack(pady=20)

    def fazer_login(self):
        """
        Função de login que agora obtém o valor do Combobox.
        """
        email = self.email_entry.get()
        senha = self.password_entry.get()
        # NOVO: Obtém o valor selecionado no Combobox
        tipo_login = self.login_type_combo.get()

        print(f"Tentativa de login como: {tipo_login}")
        print(f"Email: {email} | Senha: {senha}")

        # A lógica de verificação no banco de dados continua a mesma
        # if tipo_login == "Médico":
        #     # db.verificar_login_medico(email, senha)
        # elif tipo_login == "Administrador":
        #     # db.verificar_login_admin(email, senha)


# --- INICIAR A APLICAÇÃO ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()