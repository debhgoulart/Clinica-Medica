import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
import mysql.connector

def abrir_tela_gerenciar_consultas(janela_pai):
    janela_consultas = tk.Toplevel(janela_pai)
    janela_consultas.title("Gerenciar Consultas")
    janela_consultas.geometry("600x400")
    janela_consultas.configure(bg="#f0f0f0")
    janela_consultas.resizable(False, False)
    GerenciarConsultas(janela_consultas)

class GerenciarConsultas:

    def __init__(self, root):
        self.root = root

        self.tree = ttk.Treeview(root, columns=("ID", "Paciente", "Médico", "Data", "Hora", "Observações"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=0, columnspan=2)

        self.btn_nova = ttk.Button(root, text="Agendar Nova Consulta", command=self.abrir_agendamento)
        self.btn_nova.grid(row=1, column=0, pady=10)

        self.tree.bind("<Double-1>", self.abrir_edicao)

        self.carregar_consultas()

    def carregar_consultas(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, paciente_cpf, medico_crm, data_consulta, horario_consulta, observacoes FROM consultas WHERE ativo=TRUE")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        finally:
            cursor.close()
            conn.close()

    def abrir_edicao(self, event):
        selected = self.tree.selection()[0]
        dados = self.tree.item(selected)['values']
        self.agendamento_window(dados)

    def abrir_agendamento(self):
        self.agendamento_window(None)

    def agendamento_window(self, dados):
        win = tk.Toplevel(self.root)
        win.title("Agendar Consulta" if not dados else "Editar Consulta")

        campos = ["CPF Paciente", "Nome", "Nascimento", "Telefone", "Endereço",
                    "CRM Médico", "Nome Médico", "Especialidade", "Horários",
                    "Data da Consulta", "Hora", "Observações"]
        entries = {}
        for i, campo in enumerate(campos):
            ttk.Label(win, text=campo).grid(row=i, column=0, sticky="w")
            ent = ttk.Entry(win)
            ent.grid(row=i, column=1, pady=2, padx=5)
            entries[campo] = ent

        def preencher_paciente(*_):
            cpf = entries["CPF Paciente"].get()
            if not cpf:
                return
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT nome, nascimento, telefone, endereco FROM pacientes WHERE cpf=%s", (cpf,))
                resultado = cursor.fetchone()
                if resultado:
                    entries["Nome"].delete(0, tk.END)
                    entries["Nascimento"].delete(0, tk.END)
                    entries["Telefone"].delete(0, tk.END)
                    entries["Endereço"].delete(0, tk.END)
                    entries["Nome"].insert(0, resultado[0])
                    entries["Nascimento"].insert(0, resultado[1])
                    entries["Telefone"].insert(0, resultado[2])
                    entries["Endereço"].insert(0, resultado[3])
            finally:
                cursor.close()
                conn.close()

        def preencher_medico(*_):
            crm = entries["CRM Médico"].get()
            if not crm:
                return
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT nome, especialidade, horarios FROM medicos WHERE crm=%s", (crm,))
                resultado = cursor.fetchone()
                if resultado:
                    entries["Nome Médico"].delete(0, tk.END)
                    entries["Especialidade"].delete(0, tk.END)
                    entries["Horários"].delete(0, tk.END)
                    entries["Nome Médico"].insert(0, resultado[0])
                    entries["Especialidade"].insert(0, resultado[1])
                    entries["Horários"].insert(0, resultado[2])
                else:
                    messagebox.showerror("Erro", "Médico não cadastrado!")
            finally:
                cursor.close()
                conn.close()

        entries["CPF Paciente"].bind("<FocusOut>", preencher_paciente)
        entries["CRM Médico"].bind("<FocusOut>", preencher_medico)

        def salvar():
            try:
                conn = conectar()
                cursor = conn.cursor()
                cpf = entries["CPF Paciente"].get()
                cursor.execute("SELECT * FROM pacientes WHERE cpf=%s", (cpf,))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO pacientes (cpf, nome, nascimento, telefone, endereco) VALUES (%s, %s, %s, %s, %s)",
                                    (cpf, entries["Nome"].get(), entries["Nascimento"].get(),
                                    entries["Telefone"].get(), entries["Endereço"].get()))

                crm = entries["CRM Médico"].get()
                cursor.execute("SELECT * FROM medicos WHERE crm=%s", (crm,))
                if not cursor.fetchone():
                    messagebox.showerror("Erro", "CRM inválido. Médicos precisam estar cadastrados.")
                    return

                if not dados:
                    cursor.execute("INSERT INTO consultas (paciente_cpf, medico_crm, data_consulta, horario_consulta, observacoes) VALUES (%s, %s, %s, %s, %s)",
                                    (cpf, crm, entries["Data da Consulta"].get(), entries["Hora"].get(), entries["Observações"].get()))
                else:
                    cursor.execute("UPDATE consultas SET paciente_cpf=%s, medico_crm=%s, data_consulta=%s, horario_consulta=%s, observacoes=%s WHERE id=%s",
                                    (cpf, crm, entries["Data da Consulta"].get(), entries["Hora"].get(), entries["Observações"].get(), dados[0]))

                conn.commit()
                messagebox.showinfo("Sucesso", "Consulta salva com sucesso!")
                win.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao salvar consulta: {err}")
                if conn:
                    conn.rollback()
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        ttk.Button(win, text="Salvar", command=salvar).grid(row=len(campos), column=0, columnspan=2, pady=10)

# Nenhum bloco __main__ necessário; integração feita via função abrir_tela_gerenciar_consultas
