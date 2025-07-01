from utils import limpar_tela
import ui.tela_pacientes as tela_pacientes
import ui.tela_medicos as tela_medicos
from database import conectar
from mysql.connector import Error
from datetime import datetime

def cadastrar_consulta():
    limpar_tela()
    print("--- Agendar Nova Consulta ---")

    paciente = obter_paciente_por_cpf()
    if not paciente:
        input("Não foi possível obter paciente. Pressione Enter para voltar...")
        return

    medico = obter_medico_por_crm()
    if not medico:
        input("Não foi possível obter médico. Pressione Enter para voltar...")
        return

    data_str = input("Data da consulta (DD/MM/AAAA): ")
    horario = input("Horário da consulta (HH:MM): ")
    observacoes = input("Observações: ")
    
    try:
        data_mysql = datetime.strptime(data_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        print("\nFormato de data inválido! Use DD/MM/AAAA.")
        input("Pressione Enter para voltar...")
        return

    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        sql = "INSERT INTO consultas (paciente_cpf, medico_crm, data_consulta, horario_consulta, observacoes) VALUES (%s, %s, %s, %s, %s)"
        dados = (paciente[0], medico[0], data_mysql, horario, observacoes)
        cursor.execute(sql, dados)
        
        conexao.commit()
        print("\nConsulta cadastrada com sucesso!")

    except Error as e:
        print(f"\nErro ao agendar consulta: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

    input("Pressione Enter para voltar ao menu...")

def listar_consultas():
    limpar_tela()
    conexao = None
    cursor = None
    lista_consultas = []
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        sql = """
            SELECT
                c.id, p.nome, p.cpf, m.nome, m.crm, m.especialidade,
                c.data_consulta, c.horario_consulta, c.observacoes
            FROM consultas AS c
            JOIN pacientes AS p ON c.paciente_cpf = p.cpf
            JOIN medicos AS m ON c.medico_crm = m.crm
            WHERE c.ativo IS TRUE
            ORDER BY c.data_consulta, c.horario_consulta
        """
        cursor.execute(sql)
        lista_consultas = cursor.fetchall()

        if not lista_consultas:
            print("Nenhuma consulta agendada.\n")
        else:
            print("======== Lista de Consultas Agendadas ========")
            for consulta in lista_consultas:
                data_obj = consulta[6]
                data_br = data_obj.strftime('%d/%m/%Y') if data_obj else 'N/A'
                print(f"\nID da Consulta: {consulta[0]}")
                print(f"  Paciente: {consulta[1]} (CPF: {consulta[2]})")
                print(f"  Médico: Dr(a). {consulta[3]} (CRM: {consulta[4]} - {consulta[5]})")
                print(f"  Data: {data_br} - Horário: {consulta[7]}")
                print(f"  Observações: {consulta[8]}")

    except Error as e:
        print(f"\nErro ao listar consultas: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
    
    input("\nPressione Enter para voltar ao menu...")
    return lista_consultas

def editar_consulta():
    limpar_tela()
    listar_consultas()
    
    try:
        id_editar = int(input("\nDigite o ID da consulta que deseja editar: "))
    except ValueError:
        print("Entrada inválida. Digite um número.")
        input("Pressione Enter para voltar...")
        return

    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT paciente_cpf, medico_crm, data_consulta, horario_consulta, observacoes FROM consultas WHERE id = %s AND ativo IS TRUE", (id_editar,))
        consulta_atual = cursor.fetchone()

        if not consulta_atual:
            print("Consulta não encontrada ou inativa.")
            input("Pressione Enter para voltar...")
            return

        paciente_cpf = consulta_atual[0]
        medico_crm = consulta_atual[1]
        data_atual_obj = consulta_atual[2]
        horario = consulta_atual[3]
        observacoes = consulta_atual[4]

        data_atual_br = data_atual_obj.strftime('%d/%m/%Y') if data_atual_obj else 'N/A'

        print("\nDeixe em branco para manter o valor atual.")
        if input("Deseja alterar o paciente? (s/n): ").strip().lower() == 's':
            paciente = obter_paciente_por_cpf()
            if paciente:
                paciente_cpf = paciente[0]

        if input("Deseja alterar o médico? (s/n): ").strip().lower() == 's':
            medico = obter_medico_por_crm()
            if medico:
                medico_crm = medico[0]

        nova_data_str = input(f"Nova data ({data_atual_br}): ").strip()
        novo_horario = input(f"Novo horário ({horario}): ").strip() or horario
        novas_observacoes = input(f"Novas observações ({observacoes}): ").strip() or observacoes
        
        data_para_update = data_atual_obj
        if nova_data_str:
            try:
                data_para_update = datetime.strptime(nova_data_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                print("\nFormato de data inválido. A data não será alterada.")

        sql = "UPDATE consultas SET paciente_cpf=%s, medico_crm=%s, data_consulta=%s, horario_consulta=%s, observacoes=%s WHERE id=%s"
        dados = (paciente_cpf, medico_crm, data_para_update, novo_horario, novas_observacoes, id_editar)
        cursor.execute(sql, dados)
        conexao.commit()
        
        print("\nConsulta atualizada com sucesso!")

    except Error as e:
        print(f"\nErro ao editar consulta: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

    input("Pressione Enter para voltar ao menu...")

def excluir_consulta():
    limpar_tela()
    listar_consultas()

    try:
        id_excluir = int(input("\nDigite o ID da consulta que deseja cancelar (inativar): "))
    except ValueError:
        print("Entrada inválida. Digite um número.")
        input("Pressione Enter para voltar...")
        return
        
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        sql = "UPDATE consultas SET ativo = FALSE WHERE id = %s"
        cursor.execute(sql, (id_excluir,))
        conexao.commit()
        
        if cursor.rowcount > 0:
            print("\nConsulta cancelada com sucesso.")
        else:
            print("\nNenhuma consulta encontrada com o ID fornecido.")
            
    except Error as e:
        print(f"\nErro ao cancelar consulta: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

    input("Pressione Enter para voltar ao menu...")

def obter_paciente_por_cpf():
    cpf = input("CPF do paciente: ").strip()
    paciente = tela_pacientes.get_paciente_por_cpf(cpf)
    if not paciente:
        print("Paciente não encontrado.")
        opcao = input("Deseja cadastrar esse paciente? (s/n): ").strip().lower()
        if opcao == 's':
            tela_pacientes.cadastrar_paciente()
            paciente = tela_pacientes.get_paciente_por_cpf(cpf)
            if not paciente:
                print("Erro ao cadastrar paciente.")
    return paciente

def obter_medico_por_crm():
    crm = input("CRM do médico responsável: ").strip()
    medico = tela_medicos.get_medico_por_crm(crm)
    if not medico:
        print("Médico não encontrado.")
        opcao = input("Deseja cadastrar esse médico? (s/n): ").strip().lower()
        if opcao == 's':
            tela_medicos.cadastrar_medico()
            medico = tela_medicos.get_medico_por_crm(crm)
            if not medico:
                print("Erro ao cadastrar médico.")
    return medico

def menu():
    while True:
        limpar_tela()
        print("====== Gerenciamento de Consultas ======")
        print("1. Agendar nova consulta")
        print("2. Listar consultas agendadas")
        print("3. Editar consulta")
        print("4. Cancelar consulta")
        print("5. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_consulta()
        elif opcao == "2":
            listar_consultas()
        elif opcao == "3":
            editar_consulta()
        elif opcao == "4":
            excluir_consulta()
        elif opcao == "5":
            break
        else:
            print("Opção inválida. Tente novamente.\n")
            input("Pressione Enter para continuar...")