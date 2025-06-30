from utils import limpar_tela
medicos = []

def cadastrar_medico():
    print("\n--- Cadastro de Novo Médico ---")
    nome = input("Nome do médico: ")
    crm = input("CRM do médico: ")
    for medico in medicos:
        if medico['crm'] == crm:
            print("Erro: Já existe um médico cadastrado com este CRM.")
            return

    especialidade = input("Especialidade: ")
    print("Informe os horários de atendimento (ex: Seg 08h-12h, Ter 14h-18h):")
    horarios = input("Horários: ")

    medico = {
        'nome': nome,
        'crm': crm,
        'especialidade': especialidade,
        'horarios': horarios
    }
    medicos.append(medico)
    print(f"Médico {nome} cadastrado com sucesso!")

def consultar_medicos():
    print("\n--- Consulta de Médicos ---")
    if not medicos:
        print("Nenhum médico cadastrado no sistema.")
        return

    crm_busca = input("Digite o CRM do médico para buscar (ou deixe em branco para listar todos): ")

    encontrou_medico = False
    for medico in medicos:
        if not crm_busca or medico['crm'] == crm_busca:
            print("\n-------------------------")
            print(f"Nome: {medico['nome']}")
            print(f"CRM: {medico['crm']}")
            print(f"Especialidade: {medico['especialidade']}")
            print(f"Horários: {medico['horarios']}")
            print("-------------------------")
            encontrou_medico = True
            if crm_busca: # Se buscou por CRM específico, para após encontrar
                break
    
    if not encontrou_medico and crm_busca:
        print(f"Nenhum médico encontrado com o CRM {crm_busca}.")
    elif not crm_busca and not medicos: # Caso tenha entrado no if not medicos e depois aqui
        pass # Mensagem já foi dada
    elif not encontrou_medico and not crm_busca and medicos: # Listou todos, não precisa de msg de erro
        pass


def atualizar_medico():
    print("\n--- Atualização de Médico ---")
    if not medicos:
        print("Nenhum médico cadastrado para atualizar.")
        return

    crm_atualizar = input("Digite o CRM do médico que deseja atualizar: ")
    
    medico_encontrado = None
    indice_medico = -1

    for i, medico in enumerate(medicos):
        if medico['crm'] == crm_atualizar:
            medico_encontrado = medico
            indice_medico = i
            break

    if medico_encontrado:
        print("\nInformações atuais do médico:")
        print(f"1. Nome: {medico_encontrado['nome']}")
        print(f"2. Especialidade: {medico_encontrado['especialidade']}")
        print(f"3. Horários: {medico_encontrado['horarios']}")
        # CRM não é usualmente alterado, mas pode ser adicionado se necessário.

        while True:
            try:
                campo_escolha = int(input("Qual informação deseja atualizar? (Digite o número ou 0 para cancelar): "))
                if 0 <= campo_escolha <= 3:
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        
        if campo_escolha == 0:
            print("Atualização cancelada.")
            return

        if campo_escolha == 1:
            novo_nome = input(f"Novo nome (anterior: {medico_encontrado['nome']}): ")
            medicos[indice_medico]['nome'] = novo_nome if novo_nome else medico_encontrado['nome']
        elif campo_escolha == 2:
            nova_especialidade = input(f"Nova especialidade (anterior: {medico_encontrado['especialidade']}): ")
            medicos[indice_medico]['especialidade'] = nova_especialidade if nova_especialidade else medico_encontrado['especialidade']
        elif campo_escolha == 3:
            novos_horarios = input(f"Novos horários (anterior: {medico_encontrado['horarios']}): ")
            medicos[indice_medico]['horarios'] = novos_horarios if novos_horarios else medico_encontrado['horarios']
        
        print("Informações do médico atualizadas com sucesso!")
    else:
        print(f"Médico com CRM {crm_atualizar} não encontrado.")

def remover_medico():
    print("\n--- Remoção de Médico ---")
    if not medicos:
        print("Nenhum médico cadastrado para remover.")
        return

    crm_remover = input("Digite o CRM do médico que deseja remover: ")

    medico_encontrado = None
    indice_medico = -1

    for i, medico in enumerate(medicos):
        if medico['crm'] == crm_remover:
            medico_encontrado = medico
            indice_medico = i
            break
            
    if medico_encontrado:
        print("\nInformações do médico a ser removido:")
        print(f"Nome: {medico_encontrado['nome']}")
        print(f"CRM: {medico_encontrado['crm']}")
        print(f"Especialidade: {medico_encontrado['especialidade']}")
        
        confirmacao = input("Tem certeza que deseja remover este médico? (s/n): ").lower()
        if confirmacao == 's':
            medicos.pop(indice_medico)
            print(f"Médico {medico_encontrado['nome']} removido com sucesso.")
        else:
            print("Remoção cancelada.")
    else:
        print(f"Médico com CRM {crm_remover} não encontrado.")

def get_medico_por_crm(crm):
    for medico in medicos:
        if medico['crm'] == crm:
            return medico
    return None

def menu():
    while True:
        print("--- Clínica Médica - Gerenciamento de Médicos ---")
        print("1. Cadastrar Médico")
        print("2. Consultar Médico(s)")
        print("3. Atualizar Médico")
        print("4. Remover Médico")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            limpar_tela()
            cadastrar_medico()
        elif escolha == '2':
            limpar_tela()
            consultar_medicos()
        elif escolha == '3':
            limpar_tela()
            atualizar_medico()
        elif escolha == '4':
            limpar_tela()
            remover_medico()
        elif escolha == '5':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")