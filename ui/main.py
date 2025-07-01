import os
import ui.tela_pacientes as tela_pacientes
import ui.tela_medicos as tela_medicos
import ui.tela_consulta as tela_consulta
from utils import limpar_tela

def menu_principal():
    while True:
        limpar_tela()
        print("====== Sistema Hospitalar ======")
        print("1. Gerenciar Pacientes")
        print("2. Gerenciar Médicos")
        print("3. Gerenciar Consultas")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            limpar_tela()
            tela_pacientes.menu()
        elif opcao == "2":
            limpar_tela()
            tela_medicos.menu()
        elif opcao == "3":
            limpar_tela()
            tela_consulta.menu()            
        elif opcao == "4":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.\n")
            input("Pressione Enter para continuar...")
            limpar_tela()

limpar_tela()
menu_principal()
