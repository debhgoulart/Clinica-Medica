import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar

def carregar_pacientes():
    conexao = conectar()
    if conexao is None:
        return []

    cursor = conexao.cursor()
    query = "SELECT cpf, nome, nascimento, telefone, endereco FROM pacientes WHERE ativo = TRUE"
    cursor.execute(query)
    pacientes = cursor.fetchall()

    cursor.close()
    conexao.close()
    return pacientes

def inativar_paciente(cpf):
    conexao = conectar()
    if conexao is None:
        return False

    try:
        cursor = conexao.cursor()
        query = "UPDATE pacientes SET ativo = FALSE WHERE cpf = %s"
        cursor.execute(query, (cpf,))
        conexao.commit()
        return True
    except Exception as e:
        print(f"Erro ao inativar paciente: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()

def atualizar_paciente(cpf, nome, nascimento, telefone, endereco):
    conexao = conectar()
    if conexao is None:
        return False

    try:
        cursor = conexao.cursor()
        query = """
            UPDATE pacientes
            SET nome = %s, nascimento = %s, telefone = %s, endereco = %s
            WHERE cpf = %s
        """
        cursor.execute(query, (nome, nascimento, telefone, endereco, cpf))
        conexao.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar paciente: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()

def abrir_tela_edicao(janela_pai, paciente, atualizar_lista):
    cpf, nome, nascimento, telefone, endereco = paciente

    janela_edicao = tk.Toplevel(janela_pai)
    janela_edicao.title("Editar Paciente")
    janela_edicao.geometry("400x400")
    janela_edicao.configure(bg="#f0f0f0")
    janela_edicao.resizable(False, False)

    tk.Label(janela_edicao, text="Editar Paciente", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    campos = {}
    labels = ["Nome", "Nascimento (AAAA-MM-DD)", "Telefone", "Endereço"]
    valores = [nome, nascimento, telefone, endereco]

    for i, (label_text, valor) in enumerate(zip(labels, valores)):
        tk.Label(janela_edicao, text=label_text, bg="#f0f0f0", font=("Arial", 12)).pack()
        entrada = tk.Entry(janela_edicao, font=("Arial", 12))
        entrada.insert(0, str(valor))
        entrada.pack(pady=5, padx=20, fill="x")
        campos[label_text] = entrada

    def salvar_edicao():
        novo_nome = campos["Nome"].get()
        nova_data = campos["Nascimento (AAAA-MM-DD)"].get()
        novo_tel = campos["Telefone"].get()
        novo_end = campos["Endereço"].get()

        if atualizar_paciente(cpf, novo_nome, nova_data, novo_tel, novo_end):
            messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso.", parent=janela_edicao)
            janela_edicao.destroy()
            atualizar_lista()
        else:
            messagebox.showerror("Erro", "Erro ao atualizar paciente.", parent=janela_edicao)

    tk.Button(janela_edicao, text="Salvar Alterações", command=salvar_edicao, bg="#1565c0", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

def abrir_tela_gerenciar_pacientes(janela_pai):
    janela_pacientes = tk.Toplevel(janela_pai)
    janela_pacientes.title("Gerenciar Pacientes")
    janela_pacientes.geometry("800x500")
    janela_pacientes.configure(bg="#f0f0f0")
    janela_pacientes.resizable(False, False)

    tk.Label(janela_pacientes, text="Lista de Pacientes Ativos", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    frame_lista = tk.Frame(janela_pacientes, bd=1, relief="solid")
    frame_lista.pack(padx=20, pady=10, fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical")
    listbox = tk.Listbox(frame_lista, font=("Arial", 12), yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.pack(side="left", fill="both", expand=True)

    pacientes_dados = []

    def atualizar_lista():
        nonlocal pacientes_dados
        listbox.delete(0, tk.END)
        pacientes_dados = carregar_pacientes()
        for paciente in pacientes_dados:
            nome = paciente[1]
            cpf = paciente[0]
            listbox.insert(tk.END, f"{nome} - CPF: {cpf}")

    def editar_paciente():
        selecionado = listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um paciente para editar.")
            return
        indice = selecionado[0]
        paciente = pacientes_dados[indice]
        abrir_tela_edicao(janela_pacientes, paciente, atualizar_lista)

    def excluir_paciente():
        selecionado = listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um paciente para inativar.")
            return
        indice = selecionado[0]
        paciente = pacientes_dados[indice]
        cpf = paciente[0]

        if messagebox.askyesno("Confirmar", "Deseja realmente inativar este paciente?"):
            if inativar_paciente(cpf):
                messagebox.showinfo("Sucesso", "Paciente inativado com sucesso.")
                atualizar_lista()
            else:
                messagebox.showerror("Erro", "Erro ao inativar paciente.")

    frame_botoes = tk.Frame(janela_pacientes, bg="#f0f0f0")
    frame_botoes.pack(pady=10)

    btn_editar = tk.Button(frame_botoes, text="Editar Paciente", command=editar_paciente, bg="#1565c0", fg="white", font=("Arial", 12, "bold"))
    btn_editar.pack(side="left", padx=10)

    btn_excluir = tk.Button(frame_botoes, text="Inativar Paciente", command=excluir_paciente, bg="#e53935", fg="white", font=("Arial", 12, "bold"))
    btn_excluir.pack(side="left", padx=10)

    atualizar_lista()
