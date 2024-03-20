
import pandas as pd
import psycopg2

conn = psycopg2.connect(
        dbname="real-estate-db",
        user="user",
        password="passwd",
        host="localhost",
        port="5432"
    )

def bairros_contagem():
    sql_query = """
    SELECT 
		cidade,
        bairro,
        COUNT(bairro) AS contagem,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY valor) AS median_value,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY area) AS median_area
    FROM 
        propriedades_venda pv
    GROUP BY 
        bairro, cidade
    ORDER BY 
        contagem DESC
    """
    df = pd.read_sql_query(sql_query, conn)

    return df

dados = bairros_contagem()

print(dados.columns)