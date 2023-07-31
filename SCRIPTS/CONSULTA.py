import pyodbc
import pandas as pd
import os

conn = None  # Variável global para armazenar a conexão com o banco de dados
cursor = None  # Variável global para armazenar o cursor

def access_db():
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

def query_count_db(cliente, agente, estabelecimento, parcela, data_inicio, data_fim, ordena): # Faz a consulta no banco e traz o resultado desejado

    try:
        query = f"DECLARE @cliente INT = {cliente};" \
                f"DECLARE @filial INT = (SELECT cgc_matriz FROM CLIEN WHERE codigo = @cliente);" \
                f"DECLARE @agente INT = {agente};" \
                f"DECLARE @estabelecimento INT = {estabelecimento};" \
                f"DECLARE @datainicio DATE = '{data_inicio}';" \
                f"DECLARE @datafim DATE = '{data_fim}';" \
                f"DECLARE @parcela varchar = '{parcela}';" \
                f"WITH ResultadoConsulta AS (" \
                f" SELECT TOP 800" \
                f"  Cod_Documento" \
                f" FROM CTREC" \
                f" WHERE cod_estabe = @estabelecimento" \
                f"  AND cod_agente = @agente" \
                f"  AND status = 'A'" \
                f"  AND Par_Documento = @parcela" \
                f"  AND dat_vencimento BETWEEN @datainicio AND @datafim" \
                f"  AND (cod_cliente = @cliente OR cgc_matriz = @filial)" \
                f")" \
                f"SELECT COUNT(*) AS Quantidadetotal FROM ResultadoConsulta;"

        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)


def query_db(cliente, agente, estabelecimento, parcela, data_inicio, data_fim, ordena): # Faz a consulta no banco e traz o resultado desejado

    try:
        query =f"DECLARE @cliente INT = {cliente};" \
                f"DECLARE @filial INT = (SELECT cgc_matriz FROM CLIEN WHERE codigo = @cliente);" \
                f"DECLARE @agente INT = {agente};" \
                f"DECLARE @estabelecimento INT = {estabelecimento};" \
                f"DECLARE @datainicio DATE = '{data_inicio}';" \
                f"DECLARE @datafim DATE = '{data_fim}';" \
                f"DECLARE @parcela varchar = '{parcela}';" \
                f"SELECT TOP 800" \
                f"  Cod_Documento AS Código," \
                f"  Num_Documento AS Documento," \
                f"  dat_vencimento AS Vencimento," \
                f"  Par_Documento AS Parcela," \
                f"  Cod_Agente AS Ag_Cobrador," \
                f"  Cod_Cliente AS Cliente," \
                f"  FORMAT(Vlr_Documento, 'C') AS Preco" \
                f" FROM CTREC" \
                f" WHERE cod_estabe = @estabelecimento" \
                f"  AND cod_agente = @agente" \
                f"  AND status = 'A'" \
                f"  AND Par_Documento = @parcela" \
                f"  AND dat_vencimento BETWEEN @datainicio AND @datafim" \
                f"  AND (cod_cliente = @cliente OR cgc_matriz = @filial)" \
                f" ORDER BY {ordena};"

        cursor.execute(query)
        result = cursor.fetchall()

        print(result)

        # Criar uma lista de dicionários representando os registros
        records = []
        for row in result:
            record = {
                "COD_DOCUMENTO": row[0],
                "NUM_DOCUMENTO": row[1],
                "DATA_VENCIMENTO": row[2],
                "PARCELA": row[3],
                "COD_AGENTE": row[4],
                "COD_CLIENTE": row[5],
                "VALOR": row[6]
            }
            records.append(record)

        # Criar o DataFrame com base na lista de dicionários
        df = pd.DataFrame(records)
        # Salvar o DataFrame em um arquivo Excel
        nome_arquivo = "Troca agente cobrador.xlsx"

        # Verificar se o arquivo já existe e excluí-lo, se necessário
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)

        df.to_excel(nome_arquivo, index=False)

        print(f"Resultados salvos em '{nome_arquivo}'")
        return result

    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)
def update_db(cliente, agente, novo_agente, estabelecimento, parcela, data_inicio, data_fim, ordena): # Faz o update no banco
    global cursor


    try:
        query_cte = f"DECLARE @cliente INT = {cliente}; " \
                    f"DECLARE @filial INT = (SELECT cgc_matriz FROM CLIEN WHERE codigo = @cliente); " \
                    f"DECLARE @agente INT = {agente}; " \
                    f"DECLARE @estabelecimento INT = {estabelecimento}; " \
                    f"DECLARE @datainicio DATE = '{data_inicio}'; " \
                    f"DECLARE @datafim DATE = '{data_fim}'; " \
                    f"DECLARE @parcela varchar(255) = '{parcela}'; " \
                    f"WITH CTE AS ( " \
                    f" SELECT TOP 800" \
                    f"  Cod_Documento AS Código," \
                    f"  Num_Documento AS Documento," \
                    f"  dat_vencimento AS Vencimento," \
                    f"  Par_Documento AS Parcela," \
                    f"  Cod_Agente AS Ag_Cobrador," \
                    f"  Cod_Cliente AS Cliente," \
                    f"  FORMAT(Vlr_Documento, 'C') AS Preco" \
                    f" FROM CTREC" \
                    f" WHERE cod_estabe = @estabelecimento" \
                    f"  AND cod_agente = @agente" \
                    f"  AND status = 'A'" \
                    f"  AND Par_Documento = @parcela" \
                    f"  AND dat_vencimento BETWEEN @datainicio AND @datafim" \
                    f"  AND (cod_cliente = @cliente OR cgc_matriz = @filial)" \
                    f" ORDER BY {ordena}" \
                    f") "

        query_update = f"UPDATE CTE " \
                       f"SET Ag_Cobrador = {novo_agente};"

        final_query = query_cte + query_update

        cursor.execute(final_query)
        conn.commit()

        rows_affected = cursor.rowcount
        return rows_affected

    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)
