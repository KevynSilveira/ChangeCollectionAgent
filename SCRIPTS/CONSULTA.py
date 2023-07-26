import pyodbc

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

def query_db(): # Faz a consulta no banco e traz o resultado desejado

    global cursor  # Utiliza a variável global
    try:
        query = f"SELECT * FROM CLIEN WHERE Cod_GrpCli IN (145, 146, 147) and Cgc_Cpf"
        cursor.execute(query)
        result = cursor.fetchall()
    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)

def update_db(): # Faz o update no banco
    global cursor

    try:
        update = f""
        cursor.execute(update)
        result = cursor.fetchall()

    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)





