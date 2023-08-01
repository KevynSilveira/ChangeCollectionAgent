import pyodbc
import pandas as pd
import os

conn = None  # Variável global para armazenar a conexão com o banco de dados
cursor = None  # Variável global para armazenar o cursor

def access_db(): # Acessa o banco de dados
    global conn, cursor  # Utiliza as variáveis globais

    try:
        # Credenciais do banco de dados
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

        cursor.execute(query) # Executa a query
        result = cursor.fetchall() # Retorna os resultados do select

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
                f"  CONVERT(varchar, Dat_Emissao, 103) AS Emissao," \
                f"  CONVERT(varchar, Dat_Vencimento, 103) AS Vencimento," \
                f"  Cod_Agente AS Ag_Cobrador," \
                f"  CT.Cod_Cliente AS Cliente," \
                f"  V.Razao_Social AS Razao_Cocial," \
                f"  Par_Documento AS Parcela," \
                f"  FORMAT(Vlr_Documento, 'C') AS Preco" \
                f" FROM CTREC CT" \
                f" LEFT JOIN V_CLIEN V ON CT.Cod_Cliente = V.Cod_Cliente" \
                f" WHERE cod_estabe = @estabelecimento" \
                f"  AND cod_agente = @agente" \
                f"  AND status = 'A'" \
                f"  AND Par_Documento = @parcela" \
                f"  AND dat_vencimento BETWEEN @datainicio AND @datafim" \
                f"  AND (CT.cod_cliente = @cliente OR cgc_matriz = @filial)" \
                f" ORDER BY {ordena};"

        cursor.execute(query) # Executa a query
        result = cursor.fetchall() # Retorna os resultados do select

        records = []# Criar uma lista de dicionários representando os registros

        for row in result: # Faz a varredura e adiciona as linhas em uma lista
            record = {
                "COD_DOCUMENTO": row[0],
                "NUM_DOCUMENTO": row[1],
                "DATA_EMISSÃO": row[2],
                "DATA_VENCIMENTO": row[3],
                "COD_AGENTE": row[4],
                "COD_CLIENTE": row[5],
                "RAZÃO SOCIAL": row[6],
                "PARCELA": row[7],
                "PREÇO": row[8]
            }
            records.append(record)

        df = pd.DataFrame(records) # Criar o DataFrame com base na lista de dicionários

        nome_arquivo = "Troca agente cobrador.xlsx" # Nome do arquivo a ser salvo

        if os.path.exists(nome_arquivo): # Verificar se o arquivo já existe e excluí-lo, se necessário
            os.remove(nome_arquivo)

        df.to_excel(nome_arquivo, index=False)

        print(f"Arquivo '{nome_arquivo}' foi gerado!")
        return result

    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)


def update_db(cliente, agente, novo_agente, estabelecimento, parcela, data_inicio, data_fim, ordena): # Faz o update do novo agente cobrador
    global cursor # Pega o cursor global

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

        query_update = f"UPDATE CTE SET Ag_Cobrador = {novo_agente};"
        final_query = query_cte + query_update # Concatena as query

        cursor.execute(final_query) # Executa a query
        conn.commit() # Confirma o update

        rows_affected = cursor.rowcount # Verifica quantas linhas foram afetadas
        return rows_affected # Retorna o valor da linha para armazenar em uma variavel

    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)
