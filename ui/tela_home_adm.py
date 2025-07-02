import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import conectar

from tela_gerenciar_pacientes import abrir_tela_gerenciar_pacientes
from tela_gerenciar_consultas import abrir_tela_gerenciar_consultas

def buscar_info_admin(id_usuario):
    conexao = conectar()
    if conexao is None:
        return None
    
    cursor = conexao.cursor()
    query = "SELECT email FROM usuarios WHERE id = %s AND tipo = 'administrador'"
    cursor.execute(query, (id_usuario,))
    resultado = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    return resultado

def buscar_todas_consultas():
    conexao = conectar()
    if conexao is None:
        return [], []

    cursor = conexao.cursor()
    query = """
        SELECT c.id, c.data_consulta, c.horario_consulta, p.nome AS nome_paciente, m.nome AS nome_medico
        FROM consultas c
        JOIN pacientes p ON c.paciente_cpf = p.cpf
        JOIN medicos m ON c.medico_crm = m.crm
        WHERE c.ativo = TRUE
    """
    cursor.execute(query)
    consultas = cursor.fetchall()

    consultas_para_realizar = []
    consultas_finalizadas = []
    data_hoje = datetime.now().date()

    for consulta in consultas:
        data_consulta = consulta[1]
        if data_consulta:
            data_formatada = data_consulta.strftime('%d/%m/%Y')
            info_str = f"{data_formatada} às {str(consulta[2])} - Paciente: {consulta[3]} - Médico: {consulta[4]}"
            dados = {'id': consulta[0], 'info_str': info_str}

            if data_consulta >= data_hoje:
                consultas_para_realizar.append(dados)
            else:
                consultas_finalizadas.append(dados)

    cursor.close()
    conexao.close()
    return consultas_para_realizar, consultas_finalizadas

def desmarcar_consulta_db(id_consulta):
    conexao = conectar()
    if conexao is None:
        return False
    
    try:
        cursor = conexao.cursor()
        query = "UPDATE consultas SET ativo = FALSE WHERE id = %s"
        cursor.execute(query, (id_consulta,))
        conexao.commit()
        return True
    except Exception as e:
        print(f"Erro ao desmarcar consulta: {e}")
        return False
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

def abrir_tela_admin(id_usuario_admin):
    janela = tk.Tk()
    janela.title("Painel do Administrador")
    janela.geometry("1000x600")
    janela.configure(bg="#f0f0f0")
    janela.resizable(False, False)

    sidebar = tk.Frame(janela, bg="#1565c0", width=250, height=600)
    sidebar.place(x=0, y=0)

    label_icone = tk.Label(sidebar, text="+", font=("Arial", 80), bg="#1565c0", fg="white")
    label_icone.place(relx=0.5, y=90, anchor="center")

    admin_info = buscar_info_admin(id_usuario_admin)
    email_admin = admin_info[0] if admin_info else "Administrador Desconhecido"

    label_email = tk.Label(sidebar, text=email_admin, bg="#1565c0", fg="white", font=("Arial", 14, "bold"), wraplength=230)
    label_email.place(x=10, y=180, width=230)

    label_funcao = tk.Label(sidebar, text="Administrador", bg="#1565c0", fg="white", font=("Arial", 12, "italic"))
    label_funcao.place(x=10, y=210, width=230)

    btn_gerenciar_pacientes = tk.Button(
        sidebar,
        text="Gerenciar Pacientes",
        bg="white",
        fg="black",
        font=("Arial", 12, "bold"),
        command=lambda: abrir_tela_gerenciar_pacientes(janela)
    )
    btn_gerenciar_pacientes.place(x=20, y=500, width=210, height=40)

    btn_gerenciar_consultas = tk.Button(
        sidebar,
        text="Gerenciar Consultas",
        bg="white",
        fg="black",
        font=("Arial", 12, "bold"),
        command=lambda: abrir_tela_gerenciar_consultas(janela)
    )
    btn_gerenciar_consultas.place(x=20, y=550, width=210, height=40)

    main_content = tk.Frame(janela, bg="#f0f0f0", width=750, height=600)
    main_content.place(x=250, y=0)

    label_titulo_realizar = tk.Label(main_content, text="Consultas para Realizar", bg="#f0f0f0", fg="black", font=("Arial", 16, "bold"))
    label_titulo_realizar.place(x=30, y=20)

    frame_realizar = tk.Frame(main_content, bd=1, relief="solid")
    frame_realizar.place(x=30, y=60, width=690, height=250)

    listbox_realizar = tk.Listbox(frame_realizar, font=("Arial", 12), bd=0, highlightthickness=0)
    listbox_realizar.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    scrollbar_realizar = ttk.Scrollbar(frame_realizar, orient="vertical", command=listbox_realizar.yview)
    scrollbar_realizar.pack(side="right", fill="y")
    listbox_realizar.config(yscrollcommand=scrollbar_realizar.set)

    label_titulo_finalizadas = tk.Label(main_content, text="Consultas Finalizadas", bg="#f0f0f0", fg="black", font=("Arial", 16, "bold"))
    label_titulo_finalizadas.place(x=30, y=370)

    frame_finalizadas = tk.Frame(main_content, bd=1, relief="solid")
    frame_finalizadas.place(x=30, y=410, width=690, height=160)

    listbox_finalizadas = tk.Listbox(frame_finalizadas, font=("Arial", 12), bd=0, highlightthickness=0)
    listbox_finalizadas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    scrollbar_finalizadas = ttk.Scrollbar(frame_finalizadas, orient="vertical", command=listbox_finalizadas.yview)
    scrollbar_finalizadas.pack(side="right", fill="y")
    listbox_finalizadas.config(yscrollcommand=scrollbar_finalizadas.set)

    dados_consultas_realizar = []

    def atualizar_listas():
        nonlocal dados_consultas_realizar
        listbox_realizar.delete(0, tk.END)
        listbox_finalizadas.delete(0, tk.END)

        dados_consultas_realizar, consultas_finalizadas = buscar_todas_consultas()

        for consulta in dados_consultas_realizar:
            listbox_realizar.insert(tk.END, consulta['info_str'])

        for consulta in consultas_finalizadas:
            listbox_finalizadas.insert(tk.END, consulta['info_str'])

    def abrir_janela_confirmacao(id_consulta):
        janela_conf = tk.Toplevel(janela)
        janela_conf.title("Confirmar Ação")
        janela_conf.geometry("350x120")
        janela_conf.resizable(False, False)
        janela_conf.transient(janela)

        label = tk.Label(janela_conf, text="Deseja realmente desmarcar esta consulta?", wraplength=300)
        label.pack(pady=20)

        def confirmar():
            if desmarcar_consulta_db(id_consulta):
                messagebox.showinfo("Sucesso", "Consulta desmarcada com sucesso.", parent=janela_conf)
                janela_conf.destroy()
                atualizar_listas()
            else:
                messagebox.showerror("Erro", "Erro ao desmarcar consulta.", parent=janela_conf)

        frame_botoes = tk.Frame(janela_conf)
        frame_botoes.pack(pady=5)

        btn_confirmar = tk.Button(frame_botoes, text="Confirmar", command=confirmar, bg="#1565c0", fg="white")
        btn_confirmar.pack(side="left", padx=10)

        btn_cancelar = tk.Button(frame_botoes, text="Cancelar", command=janela_conf.destroy)
        btn_cancelar.pack(side="left", padx=10)

    def desmarcar_selecionada():
        selecionado = listbox_realizar.curselection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma consulta para desmarcar.")
            return
        
        indice = selecionado[0]
        id_da_consulta = dados_consultas_realizar[indice]['id']
        abrir_janela_confirmacao(id_da_consulta)

    btn_desmarcar = tk.Button(main_content, text="Desmarcar Consulta Selecionada", command=desmarcar_selecionada, bg="#e53935", fg="white", font=("Arial", 10, "bold"))
    btn_desmarcar.place(x=520, y=315)

    atualizar_listas()
    janela.mainloop()

if __name__ == "__main__":
    id_admin_logado = 1
    abrir_tela_admin(id_admin_logado)
