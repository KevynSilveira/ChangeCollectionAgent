import pyodbc
import pandas as pd
import os

conn = None  # Variável global para armazenar a conexão com o banco de dados
cursor = None  # Variável global para armazenar o cursor

def access_db():
    """Acessa o banco de dados SQL Server usando as configurações do arquivo config.ini."""
    global conn, cursor  # Utiliza as variáveis globais

    try:
        server = ""
        database = ""
        username = ""
        password = ""

        # Monta os dados para enviar para o banco de dados (credenciais)
        conn_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        print("Conexão concluida!")
    except:
        print("Erro ao conectar no banco")
    return conn, cursor

def close_db(): # Fecha a conexão com o banco de dados.
    global conn, cursor  # Utiliza as variáveis globais
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()

def query_count_db(cliente, agente, estabelecimento, data_inicio, data_fim): # Faz a consulta no banco e traz o resultado desejado

    try:
        query = f"DECLARE @cliente INT = {cliente};" \
                f"DECLARE @filial INT = (SELECT cgc_matriz FROM CLIEN WHERE codigo = @cliente);" \
                f"DECLARE @agente INT = {agente};" \
                f"DECLARE @estabelecimento INT = {estabelecimento};" \
                f"DECLARE @datainicio DATE = '{data_inicio}'" \
                f"DECLARE @datafim DATE = '{data_fim}'" \
                f" ; WITH ResultadoConsulta AS (" \
                f" SELECT cod_documento FROM CTREC" \
                f" WHERE cod_estabe = @estabelecimento" \
                f" AND cod_agente = @agente" \
                f" AND status = 'A'" \
                f" AND dat_vencimento BETWEEN @datainicio AND @datafim" \
                f" AND (cod_cliente = @cliente OR cgc_matriz = @filial)" \
                f")" \
                f" SELECT COUNT (*) AS Quantidadetotal" \
                f" FROM ResultadoConsulta;"

        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)


def query_db(cliente, agente, estabelecimento, data_inicio, data_fim): # Faz a consulta no banco e traz o resultado desejado

    try:
        query = f"DECLARE @cliente INT = {cliente};" \
                f"DECLARE @filial INT = (SELECT cgc_matriz FROM CLIEN WHERE codigo = @cliente);" \
                f"DECLARE @agente INT = {agente};" \
                f"DECLARE @estabelecimento INT = {estabelecimento};" \
                f"DECLARE @datainicio DATE = '{data_inicio}'" \
                f"DECLARE @datafim DATE = '{data_fim}'" \
                f" SELECT  num_documento, dat_vencimento, vlr_documento" \
                f" FROM CTREC" \
                f" WHERE cod_estabe = @estabelecimento" \
                f" AND cod_agente = @agente" \
                f" AND status = 'A'" \
                f" AND dat_vencimento BETWEEN @datainicio AND @datafim" \
                f" AND (cod_cliente = @cliente OR cgc_matriz = @filial)" \

        cursor.execute(query)
        result = cursor.fetchall()

        # Criar uma lista de dicionários representando os registros
        records = []
        for row in result:
            record = {
                "DOCUMENTO": row[0],
                "VENCIMENTO": row[1],
                "VALOR": row[2],
            }
            records.append(record)

        # Criar o DataFrame com base na lista de dicionários
        df = pd.DataFrame(records)
        # Salvar o DataFrame em um arquivo Excel
        nome_arquivo = "Troca agente cobrador FDIC.xlsx"

        # Verificar se o arquivo já existe e excluí-lo, se necessário
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)

        df.to_excel(nome_arquivo, index=False)

        print(f"Resultados salvos em '{nome_arquivo}'")
        return result

    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)
def update_db(): # Faz o update no banco
    global cursor

    try:
        update = f""
        cursor.execute(update)
        result = cursor.fetchall()
        print(result)

    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)


#access_db()
#query_db(49918, 2747, 1, '27/07/2023', '27/07/2023')