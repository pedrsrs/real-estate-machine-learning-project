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

def unique(param, regiao):
    if regiao is None:
        sql_query = """
        SELECT distinct {} from propriedades_venda 
        """.format(param)
    else:
        sql_query = """
        SELECT distinct {} from propriedades_venda where regiao ilike '{}'
        """.format(param, regiao)
    cursor.execute(sql_query)
    elements = cursor.fetchall()

    return elements

def bairros_contagem(regiao):
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

def regions_percentage(regiao):
    sql_query = """
    SELECT regiao, 
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM propriedades_venda), 2)::numeric AS percentage
    FROM propriedades_venda pv 
    GROUP BY regiao;
    """
    df = pd.read_sql_query(sql_query, conn)

    return df

def bairro_metro_quadrado(regiao):
    sql_query = """
    SELECT 
        sum(area)/sum(valor)
    from
        propriedades_valor
    group by
        bairro
    """
    df = pd.read_sql_query(sql_query, conn)

    return df

def get_median(element, regiao):
    sql_query = """
    SELECT 
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {}) AS median_value
    FROM 
    propriedades_venda;
    """.format(element)

    cursor.execute(sql_query)
    rounded_value = cursor.fetchone()[0]  
    return rounded_value

def valor_metro_quadrado(regiao):
    sql_query = """
    SELECT 
        ROUND(CAST(sum(valor)/sum(area) AS numeric),2)  as result
    from
        propriedades_venda
    """
    cursor.execute(sql_query)
    count = cursor.fetchone()[0]  
    return count

def get_count(regiao):
    sql_query = """
    SELECT 
    count(valor)
    FROM 
    propriedades_venda;
    """

    cursor.execute(sql_query)
    count = cursor.fetchone()[0]  
    return count
