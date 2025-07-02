import tkinter as tk

def abrir_tela_gerenciar_pacientes(janela_pai):
    janela_pacientes = tk.Toplevel(janela_pai)
    janela_pacientes.title("Gerenciar Pacientes")
    janela_pacientes.geometry("600x400")
    janela_pacientes.configure(bg="#f0f0f0")
    janela_pacientes.resizable(False, False)
