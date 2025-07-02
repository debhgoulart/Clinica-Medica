import tkinter as tk

def abrir_tela_home_adm():
    janela_adm = tk.Toplevel()
    janela_adm.title("Administrador - Clínica Médica")
    janela_adm.geometry("400x300")
    tk.Label(janela_adm, text="Bem-vindo, Administrador!").pack(pady=50)
