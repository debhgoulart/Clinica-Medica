import os
from database import conectar
from mysql.connector import Error
from utils import limpar_tela
from datetime import datetime

def exibir_lista_pacientes():
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "SELECT cpf, nome, nascimento FROM pacientes WHERE ativo IS TRUE ORDER BY nome"
        cursor.execute(sql)
        lista_pacientes = cursor.fetchall()

        if lista_pacientes:
            print("======== Lista de Pacientes Ativos ========")
            for i, paciente in enumerate(lista_pacientes):
                data_nasc = paciente[2]
                data_nasc_br = data_nasc.strftime('%d/%m/%Y') if data_nasc else 'N/A'
                print(f"{i+1}. Nome: {paciente[1]} | CPF: {paciente[0]} | Nasc.: {data_nasc_br}")
            print()
            return True
        else:
            print("Nenhum paciente ativo encontrado.")
            return False
    except Error as e:
        print(f"Erro ao listar pacientes: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def listar_pacientes():
    limpar_tela()
    exibir_lista_pacientes()
    print("")
    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

def editar_paciente():
    limpar_tela()
    if not exibir_lista_pacientes():
        input("\nPressione Enter para voltar ao menu...")
        limpar_tela()
        return

    cpf_editar = input("\nDigite o CPF do paciente da lista que deseja editar: ")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT cpf, nome, nascimento, telefone, endereco FROM pacientes WHERE cpf = %s AND ativo IS TRUE", (cpf_editar,))
        paciente_atual = cursor.fetchone()

        if not paciente_atual:
            print("Paciente não encontrado ou inativo.")
            input("Pressione Enter para continuar...")
            limpar_tela()
            return

        print("\nDeixe o campo em branco para manter o valor atual.")
        data_atual_obj = paciente_atual[2]
        data_atual_br = data_atual_obj.strftime('%d/%m/%Y') if data_atual_obj else 'N/A'
        
        nome = input(f"Novo nome ({paciente_atual[1]}): ") or paciente_atual[1]
        nascimento_str = input(f"Nova data de nascimento ({data_atual_br}): ")
        telefone = input(f"Novo telefone ({paciente_atual[3]}): ") or paciente_atual[3]
        endereco = input(f"Novo endereço ({paciente_atual[4]}): ") or paciente_atual[4]

        nascimento_mysql = data_atual_obj
        if nascimento_str:
            try:
                nascimento_mysql = datetime.strptime(nascimento_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                print("\nFormato de data inválido! A data não será alterada.")
        
        sql = "UPDATE pacientes SET nome = %s, nascimento = %s, telefone = %s, endereco = %s WHERE cpf = %s"
        dados = (nome, nascimento_mysql, telefone, endereco, cpf_editar)
        cursor.execute(sql, dados)
        conexao.commit()
        print("\nPaciente atualizado com sucesso!")

    except Error as e:
        print(f"Erro ao editar paciente: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

def excluir_paciente():
    limpar_tela()
    if not exibir_lista_pacientes():
        input("\nPressione Enter para voltar ao menu...")
        limpar_tela()
        return

    cpf_excluir = input("\nDigite o CPF do paciente da lista que deseja inativar: ")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "UPDATE pacientes SET ativo = FALSE WHERE cpf = %s"
        cursor.execute(sql, (cpf_excluir,))
        conexao.commit()

        if cursor.rowcount > 0:
            print("\nPaciente inativado com sucesso!")
        else:
            print("\nNenhum paciente encontrado com o CPF fornecido.")

    except Error as e:
        print(f"Erro ao inativar paciente: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
            
    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

# O restante do arquivo (cadastrar_paciente, get_paciente_por_cpf, menu) permanece igual.
def cadastrar_paciente():
    limpar_tela()
    print("--- Cadastro de Novo Paciente ---")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    nascimento_str = input("Data de nascimento (DD/MM/AAAA): ")
    telefone = input("Telefone: ")
    endereco = input("Endereço: ")

    try:
        data_nascimento_obj = datetime.strptime(nascimento_str, '%d/%m/%Y')
        nascimento_mysql = data_nascimento_obj.strftime('%Y-%m-%d')
    except ValueError:
        print("\nFormato de data inválido! Use DD/MM/AAAA.")
        input("Pressione Enter para voltar ao menu...")
        return

    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "INSERT INTO pacientes (cpf, nome, nascimento, telefone, endereco) VALUES (%s, %s, %s, %s, %s)"
        dados = (cpf, nome, nascimento_mysql, telefone, endereco)
        cursor.execute(sql, dados)
        conexao.commit()
        print("Paciente cadastrado com sucesso!\n")
    except Error as e:
        if e.errno == 1062:
            print("Erro: Já existe um paciente cadastrado com este CPF.")
        else:
            print(f"Erro ao cadastrar paciente: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
    input("Pressione Enter para voltar ao menu...")
    limpar_tela()

def get_paciente_por_cpf(cpf):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "SELECT * FROM pacientes WHERE cpf = %s AND ativo IS TRUE"
        cursor.execute(sql, (cpf,))
        paciente = cursor.fetchone()
        return paciente
    except Error as e:
        print(f"Erro ao buscar paciente: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

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