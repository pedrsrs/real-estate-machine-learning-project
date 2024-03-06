# db_queries.py

import pandas as pd
import psycopg2

conn = psycopg2.connect(
        dbname="real-estate-db",
        user="user",
        password="passwd",
        host="localhost",
        port="5432"
    )
cursor = conn.cursor()

def count_bairros():
    sql_query = """
        SELECT 
            bairro,
            COUNT(bairro) AS contagem
        FROM 
            propriedades_venda pv
        GROUP BY 
            bairro
        ORDER BY 
            contagem DESC
        LIMIT 15;
    """
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df

def bairros_contagem():
    sql_query = """
    SELECT 
        bairro,
        COUNT(bairro) AS contagem,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY valor) AS median_value,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY area) AS median_area
    FROM 
        propriedades_venda pv
    GROUP BY 
        bairro
    ORDER BY 
        contagem DESC
    """
    df = pd.read_sql_query(sql_query, conn)

    return df

def regions_percentage():
    sql_query = """
    SELECT regiao, 
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM propriedades_venda), 2)::numeric AS percentage
    FROM propriedades_venda pv 
    GROUP BY regiao;
    """
    df = pd.read_sql_query(sql_query, conn)

    return df

def bairros_contagem():
    sql_query = """
    SELECT 
        bairro,
        COUNT(bairro) AS contagem
    FROM 
        propriedades_venda pv
    GROUP BY 
        bairro
    ORDER BY 
        contagem DESC
    LIMIT 15;
    """
    df = pd.read_sql_query(sql_query, conn)

    return df

def avg_price():
    sql_query = """
    SELECT 
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY valor) AS median_value
    FROM 
    propriedades_venda;
    """
    cursor.execute(sql_query)
    rounded_value = cursor.fetchone()[0]  
    cursor.close()
    return rounded_value

def get_median(element):
    sql_query = """
    SELECT 
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {}) AS median_value
    FROM 
    propriedades_venda;
    """.format(element)

    cursor.execute(sql_query)
    rounded_value = cursor.fetchone()[0]  
    cursor.close()
    return rounded_value

def get_count():
    sql_query = """
    SELECT 
    count(valor)
    FROM 
    propriedades_venda;
    """

    cursor.execute(sql_query)
    count = cursor.fetchone()[0]  
    cursor.close()
    return count
