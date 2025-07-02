# database.py
import mysql.connector
from tkinter import messagebox

def conectar():
    """
    Função para conectar ao banco de dados MySQL.
    Retorna o objeto de conexão se for bem-sucedido, None caso contrário.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root", 
            database="clinica_medica"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror(
            "Erro de Conexão",
            f"Não foi possível conectar ao banco de dados: {err}"
        )
        return None
