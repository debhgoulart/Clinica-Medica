from utils import limpar_tela
from ui.database import conectar
from mysql.connector import Error

def cadastrar_medico():
    limpar_tela()
    print("\n--- Cadastro de Novo Médico ---")
    nome = input("Nome do médico: ")
    crm = input("CRM do médico: ")
    especialidade = input("Especialidade: ")
    horarios = input("Horários de atendimento (ex: Seg 08h-12h): ")

    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = "INSERT INTO medicos (crm, nome, especialidade, horarios) VALUES (%s, %s, %s, %s)"
        dados = (crm, nome, especialidade, horarios)
        cursor.execute(sql, dados)
        
        conexao.commit()
        print(f"Médico {nome} cadastrado com sucesso!")

    except Error as e:
        if e.errno == 1062: # erro de entrada duplicada
            print("Erro: Já existe um médico cadastrado com este CRM.")
        else:
            print(f"Erro ao cadastrar médico: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
    
    input("\nPressione Enter para continuar...")

def consultar_medicos():
    limpar_tela()
    print("\n--- Consulta de Médicos ---")
    crm_busca = input("Digite o CRM do médico para buscar (ou deixe em branco para listar todos): ")

    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = "SELECT crm, nome, especialidade, horarios FROM medicos WHERE ativo IS TRUE"

        if crm_busca:
            sql += " AND crm = %s"
            cursor.execute(sql, (crm_busca,))
        else:
            sql += " ORDER BY nome"
            cursor.execute(sql)
        
        lista_medicos = cursor.fetchall()

        if not lista_medicos:
            print(f"Nenhum médico encontrado.")
        else:
            for medico in lista_medicos:
                print("\n-------------------------")
                # Acesso por índice numérico
                print(f"Nome: {medico[1]}")
                print(f"CRM: {medico[0]}")
                print(f"Especialidade: {medico[2]}")
                print(f"Horários: {medico[3]}")
                print("-------------------------")

    except Error as e:
        print(f"Erro ao consultar médicos: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

    input("\nPressione Enter para continuar...")

def atualizar_medico():
    limpar_tela()
    print("\n--- Atualização de Médico ---")
    crm_atualizar = input("Digite o CRM do médico que deseja atualizar: ")

    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT crm, nome, especialidade, horarios FROM medicos WHERE crm = %s AND ativo IS TRUE", (crm_atualizar,))
        medico_atual = cursor.fetchone()

        if not medico_atual:
            print("Médico não encontrado ou inativo.")
            input("Pressione Enter para continuar...")
            return

        print("\nDeixe em branco para manter o valor atual.")
        nome = input(f"Novo nome ({medico_atual[1]}): ") or medico_atual[1]
        especialidade = input(f"Nova especialidade ({medico_atual[2]}): ") or medico_atual[2]
        horarios = input(f"Novos horários ({medico_atual[3]}): ") or medico_atual[3]

        sql = """
            UPDATE medicos 
            SET nome = %s, especialidade = %s, horarios = %s
            WHERE crm = %s
        """
        dados = (nome, especialidade, horarios, crm_atualizar)
        cursor.execute(sql, dados)
        conexao.commit()

        print("Informações do médico atualizadas com sucesso!")

    except Error as e:
        print(f"Erro ao atualizar médico: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
    
    input("\nPressione Enter para continuar...")

def remover_medico():
    limpar_tela()
    print("\n--- Inativar Médico ---")
    crm_remover = input("Digite o CRM do médico que deseja inativar: ")

    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = "UPDATE medicos SET ativo = FALSE WHERE crm = %s"
        cursor.execute(sql, (crm_remover,))
        
        conexao.commit()

        if cursor.rowcount > 0:
            print(f"Médico com CRM {crm_remover} inativado com sucesso.")
        else:
            print("Nenhum médico encontrado com o CRM fornecido.")

    except Error as e:
        print(f"Erro ao inativar médico: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
            
    input("\nPressione Enter para continuar...")

def get_medico_por_crm(crm):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        sql = "SELECT crm, nome, especialidade, horarios FROM medicos WHERE crm = %s AND ativo IS TRUE"
        cursor.execute(sql, (crm,))
        medico = cursor.fetchone()
        return medico
    except Error as e:
        print(f"Erro ao buscar médico: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def menu():
    while True:
        limpar_tela()
        print("--- Clínica Médica - Gerenciamento de Médicos ---")
        print("1. Cadastrar Médico")
        print("2. Consultar Médico(s)")
        print("3. Atualizar Médico")
        print("4. Inativar Médico")
        print("5. Voltar ao menu principal")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            cadastrar_medico()
        elif escolha == '2':
            consultar_medicos()
        elif escolha == '3':
            atualizar_medico()
        elif escolha == '4':
            remover_medico()
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar...")