import os
from utils import limpar_tela

pacientes = []

def cadastrar_paciente():
    limpar_tela()
    nome = input("Nome: ")
    cpf = input("CPF: ")
    nascimento = input("Data de nascimento (DD/MM/AAAA): ")
    telefone = input("Telefone: ")
    endereco = input("Endereço: ")

    paciente = {
        "nome": nome,
        "cpf": cpf,
        "nascimento": nascimento,
        "telefone": telefone,
        "endereco": endereco
    }
    pacientes.append(paciente)
    print("Paciente cadastrado com sucesso!\n")
    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

def listar_pacientes():
    limpar_tela()
    if not pacientes:
        print("Nenhum paciente cadastrado.\n")
    else:
        print("======== Lista de Pacientes ========")
        for i, paciente in enumerate(pacientes):
            print(f"{i+1}. {paciente['nome']} - CPF: {paciente['cpf']}")
    print()
    print("")
    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

def editar_paciente():
    limpar_tela()
    listar_pacientes()
    try:
        indice = int(input("Digite o número do paciente que deseja editar: ")) - 1
        if 0 <= indice < len(pacientes):
            print("Deixe em branco para manter o valor atual.")
            nome = input(f"Novo nome ({pacientes[indice]['nome']}): ") or pacientes[indice]['nome']
            cpf = input(f"Novo CPF ({pacientes[indice]['cpf']}): ") or pacientes[indice]['cpf']
            nascimento = input(f"Nova data de nascimento ({pacientes[indice]['nascimento']}): ") or pacientes[indice]['nascimento']
            telefone = input(f"Novo telefone ({pacientes[indice]['telefone']}): ") or pacientes[indice]['telefone']
            endereco = input(f"Novo endereço ({pacientes[indice]['endereco']}): ") or pacientes[indice]['endereco']

            pacientes[indice].update({
                "nome": nome,
                "cpf": cpf,
                "nascimento": nascimento,
                "telefone": telefone,
                "endereco": endereco
            })
            print("Paciente atualizado com sucesso!\n")
        else:
            print("Número inválido.\n")
    except ValueError:
        print("Entrada inválida.\n")
    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

def excluir_paciente():
    limpar_tela()
    listar_pacientes()
    try:
        indice = int(input("Digite o número do paciente que deseja excluir: ")) - 1
        if 0 <= indice < len(pacientes):
            paciente_removido = pacientes.pop(indice)
            print(f"Paciente {paciente_removido['nome']} removido com sucesso.\n")
        else:
            print("Número inválido.\n")
    except ValueError:
        print("Entrada inválida.\n")
    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

def get_paciente_por_cpf(cpf):
    for paciente in pacientes:
        if paciente["cpf"] == cpf:
            return paciente
    return None

def get_lista_pacientes():
    return pacientes


def menu():
    while True:
        print("====== Gerenciamento de Pacientes ======")
        print("1. Cadastrar paciente")
        print("2. Listar pacientes")
        print("3. Editar paciente")
        print("4. Excluir paciente")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_paciente()
        elif opcao == "2":
            listar_pacientes()
        elif opcao == "3":
            editar_paciente()
        elif opcao == "4":
            excluir_paciente()
        elif opcao == "5":
            limpar_tela()
            break
        else:
            print("Opção inválida. Tente novamente.\n")
            input("Pressione Enter para continuar...")
            limpar_tela()
