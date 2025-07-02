import tkinter as tk

def abrir_tela_gerenciar_consultas(janela_pai):
    janela_consultas = tk.Toplevel(janela_pai)
    janela_consultas.title("Gerenciar Consultas")
    janela_consultas.geometry("600x400")
    janela_consultas.configure(bg="#f0f0f0")
    janela_consultas.resizable(False, False)

