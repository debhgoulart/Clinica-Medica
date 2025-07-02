import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import conectar

def buscar_info_medico(crm):
    conexao = conectar() 
    if conexao is None:
        return None
    
    # O cursor agora retorna tuplas em vez de dicionários
    cursor = conexao.cursor()
    # Query atualizada para buscar também os horários
    query = "SELECT nome, crm, especialidade, horarios FROM medicos WHERE crm = %s"
    cursor.execute(query, (crm,))
    medico = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    return medico

def buscar_consultas(crm):
    conexao = conectar()
    if conexao is None:
        return [], []

    # O cursor agora retorna tuplas em vez de dicionários
    cursor = conexao.cursor()
    # A ordem no SELECT é importante: 0:id, 1:data, 2:horario, 3:nome_paciente
    query = """
        SELECT c.id, c.data_consulta, c.horario_consulta, p.nome AS nome_paciente
        FROM consultas c
        JOIN pacientes p ON c.paciente_cpf = p.cpf
        WHERE c.medico_crm = %s AND c.ativo = TRUE
    """
    cursor.execute(query, (crm,))
    consultas = cursor.fetchall()
    
    consultas_para_realizar = []
    consultas_finalizadas = []
    data_hoje = datetime.now().date()

    for consulta in consultas:
        # Acessando os dados por índice
        data_da_consulta = consulta[1]
        if data_da_consulta:
            data_formatada = data_da_consulta.strftime('%d/%m/%Y')
            info_str = f"{data_formatada} às {str(consulta[2])} - Paciente: {consulta[3]}"
            
            # Criamos um dicionário para guardar o ID e o texto da consulta
            dados_consulta = {'id': consulta[0], 'info_str': info_str}

            if data_da_consulta >= data_hoje:
                consultas_para_realizar.append(dados_consulta)
            else:
                consultas_finalizadas.append(dados_consulta)
            
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

def criar_tela_medico(crm_medico):
    janela = tk.Tk()
    janela.title("Painel do Médico")
    janela.geometry("1000x600")
    janela.configure(bg="#f0f0f0")
    janela.resizable(False, False)

    sidebar = tk.Frame(janela, bg="#00c853", width=250, height=600)
    sidebar.place(x=0, y=0)

    # Ícone de "+" no lugar do círculo
    label_icone = tk.Label(sidebar, text="+", font=("Arial", 80), bg="#00c853", fg="white")
    label_icone.place(relx=0.5, y=90, anchor="center")
    
    medico = buscar_info_medico(crm_medico)
    if medico:
        # Acessando os dados por índice
        nome_medico = medico[0]
        crm = medico[1]
        especialidade = medico[2]
        horarios = medico[3] if medico[3] else "Não definido"
    else:
        nome_medico = "Médico não encontrado"
        crm = "N/A"
        especialidade = "N/A"
        horarios = "N/A"

    label_nome = tk.Label(sidebar, text=nome_medico, bg="#00c853", fg="white", font=("Arial", 14, "bold"))
    label_nome.place(x=10, y=180, width=230)

    label_crm = tk.Label(sidebar, text=f"CRM: {crm}", bg="#00c853", fg="white", font=("Arial", 12))
    label_crm.place(x=10, y=210, width=230)

    label_especialidade = tk.Label(sidebar, text=especialidade, bg="#00c853", fg="white", font=("Arial", 12, "italic"))
    label_especialidade.place(x=10, y=240, width=230)
    
    # Novo label para exibir os horários
    label_horarios = tk.Label(sidebar, text=horarios, bg="#00c853", fg="white", font=("Arial", 11))
    label_horarios.place(x=10, y=270, width=230)
    
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

    # Armazenamos os dados completos aqui para podermos pegar o ID depois
    dados_consultas_realizar = []

    def atualizar_listas():
        nonlocal dados_consultas_realizar
        listbox_realizar.delete(0, tk.END)
        listbox_finalizadas.delete(0, tk.END)

        dados_consultas_realizar, consultas_finalizadas = buscar_consultas(crm_medico)

        for consulta in dados_consultas_realizar:
            listbox_realizar.insert(tk.END, consulta['info_str'])

        for consulta in consultas_finalizadas:
            listbox_finalizadas.insert(tk.END, consulta['info_str'])

    def abrir_janela_confirmacao(id_consulta):
        janela_conf = tk.Toplevel(janela)
        janela_conf.title("Confirmar Ação")
        janela_conf.geometry("350x120")
        janela_conf.resizable(False, False)
        janela_conf.transient(janela) # Mantém a janela no topo

        label = tk.Label(janela_conf, text="Tem certeza que deseja desmarcar esta consulta?", wraplength=300)
        label.pack(pady=20)

        def confirmar():
            if desmarcar_consulta_db(id_consulta):
                messagebox.showinfo("Sucesso", "Consulta desmarcada com sucesso.", parent=janela_conf)
                janela_conf.destroy()
                atualizar_listas()
            else:
                messagebox.showerror("Erro", "Não foi possível desmarcar a consulta.", parent=janela_conf)

        frame_botoes = tk.Frame(janela_conf)
        frame_botoes.pack(pady=5)
        
        btn_confirmar = tk.Button(frame_botoes, text="Confirmar", command=confirmar, bg="#00c853", fg="white")
        btn_confirmar.pack(side="left", padx=10)
        
        btn_cancelar = tk.Button(frame_botoes, text="Cancelar", command=janela_conf.destroy)
        btn_cancelar.pack(side="left", padx=10)

    def desmarcar_selecionada():
        selecionado = listbox_realizar.curselection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione uma consulta para desmarcar.")
            return
        
        indice = selecionado[0]
        id_da_consulta = dados_consultas_realizar[indice]['id']
        abrir_janela_confirmacao(id_da_consulta)

    btn_desmarcar = tk.Button(main_content, text="Desmarcar Consulta Selecionada", command=desmarcar_selecionada, bg="#e53935", fg="white", font=("Arial", 10, "bold"))
    btn_desmarcar.place(x=520, y=315)

    atualizar_listas()
    janela.mainloop()

if __name__ == "__main__":
    crm_do_medico_logado = "123456/SP"
    criar_tela_medico(crm_do_medico_logado)
