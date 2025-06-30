import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="clinica_medica"
        )

        if conexao.is_connected():
            return conexao
            
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None