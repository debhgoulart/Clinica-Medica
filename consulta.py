from utils import limpar_tela
import pacientes
import medicos

consultas = []

def cadastrar_consulta():
    limpar_tela()

    paciente = obter_paciente_por_cpf()
    if not paciente:
        input("Não foi possível obter paciente. Pressione Enter para voltar...")
        limpar_tela()
        return

    medico = obter_medico_por_crm()
    if not medico:
        input("Não foi possível obter médico. Pressione Enter para voltar...")
        limpar_tela()
        return

    data = input("Data da consulta (DD/MM/AAAA): ")
    horario = input("Horário da consulta (HH:MM): ")
    observacoes = input("Observações: ")

    consulta = {
        "paciente_nome": paciente["nome"],
        "paciente_cpf": paciente["cpf"],
        "medico_nome": medico["nome"],
        "medico_crm": medico["crm"],
        "especialidade": medico["especialidade"],
        "data": data,
        "horario": horario,
        "observacoes": observacoes
    }

    consultas.append(consulta)
    print("Consulta cadastrada com sucesso!\n")
    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

def listar_consultas():
    limpar_tela()
    if not consultas:
        print("Nenhuma consulta agendada.\n")
    else:
        print("======== Lista de Consultas ========")
        for i, consulta in enumerate(consultas):
            print(f"{i+1}. Paciente: {consulta['paciente_nome']} (CPF: {consulta['paciente_cpf']})")
            print(f"    Médico: Dr(a). {consulta['medico_nome']} (CRM: {consulta['medico_crm']} - {consulta['especialidade']})")
            print(f"    Data: {consulta['data']} - Horário: {consulta['horario']}")
            print(f"    Observações: {consulta['observacoes']}\n")
    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

def editar_consulta():
    limpar_tela()
    listar_consultas()
    try:
        indice = int(input("Digite o número da consulta que deseja editar: ")) - 1
        if 0 <= indice < len(consultas):
            print("Deixe em branco para manter o valor atual.\n")

            if input("Deseja alterar o paciente? (s/n): ").strip().lower() == 's':
                paciente = obter_paciente_por_cpf()
                if paciente:
                    consultas[indice]['paciente_nome'] = paciente['nome']
                    consultas[indice]['paciente_cpf'] = paciente['cpf']

            if input("Deseja alterar o médico? (s/n): ").strip().lower() == 's':
                medico = obter_medico_por_crm()
                if medico:
                    consultas[indice]['medico_nome'] = medico['nome']
                    consultas[indice]['medico_crm'] = medico['crm']
                    consultas[indice]['especialidade'] = medico['especialidade']

            data = input(f"Nova data ({consultas[indice]['data']}): ").strip() or consultas[indice]['data']
            horario = input(f"Novo horário ({consultas[indice]['horario']}): ").strip() or consultas[indice]['horario']
            observacoes = input(f"Novas observações ({consultas[indice]['observacoes']}): ").strip() or consultas[indice]['observacoes']

            consultas[indice]['data'] = data
            consultas[indice]['horario'] = horario
            consultas[indice]['observacoes'] = observacoes

            print("Consulta atualizada com sucesso!\n")
        else:
            print("Número inválido.\n")
    except ValueError:
        print("Entrada inválida.\n")
    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

def excluir_consulta():
    limpar_tela()
    listar_consultas()
    try:
        indice = int(input("Digite o número da consulta que deseja excluir: ")) - 1
        if 0 <= indice < len(consultas):
            consulta_removida = consultas.pop(indice)
            print(f"Consulta com {consulta_removida['paciente_nome']} removida com sucesso.\n")
        else:
            print("Número inválido.\n")
    except ValueError:
        print("Entrada inválida.\n")
    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

def obter_paciente_por_cpf():
    cpf = input("CPF do paciente: ").strip()
    paciente = pacientes.get_paciente_por_cpf(cpf)
    if not paciente:
        print("Paciente não encontrado.")
        opcao = input("Deseja cadastrar esse paciente? (s/n): ").strip().lower()
        if opcao == 's':
            pacientes.cadastrar_paciente()
            paciente = pacientes.get_paciente_por_cpf(cpf)
            if not paciente:
                print("Erro ao cadastrar paciente.")
    return paciente

def obter_medico_por_crm():
    crm = input("CRM do médico responsável: ").strip()
    medico = medicos.get_medico_por_crm(crm)
    if not medico:
        print("Médico não encontrado.")
        opcao = input("Deseja cadastrar esse médico? (s/n): ").strip().lower()
        if opcao == 's':
            medicos.cadastrar_medico()
            medico = medicos.get_medico_por_crm(crm)
            if not medico:
                print("Erro ao cadastrar médico.")
    return medico

def menu():
    while True:
        print("====== Gerenciamento de Consultas ======")
        print("1. Cadastrar consulta")
        print("2. Listar consultas")
        print("3. Editar consulta")
        print("4. Excluir consulta")
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
            limpar_tela()
            break
        else:
            print("Opção inválida. Tente novamente.\n")
            input("Pressione Enter para continuar...")
            limpar_tela()
