import psycopg2

conn = psycopg2.connect(
        dbname="real-estate-db",
        user="user",
        password="passwd",
        host="localhost",
        port="5432"
    )
cursor = conn.cursor()

def unique_bairros():
    sql_query = """
    SELECT distinct bairro from propriedades_venda 
    """
    cursor.execute(sql_query)
    bairros = cursor.fetchall()

    return bairros

lista_bairros = unique_bairros()
for bairro in lista_bairros:
    print(bairro[0])