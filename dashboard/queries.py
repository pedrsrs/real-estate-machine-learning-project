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

def all_data():
    sql_query = """
    SELECT * from propriedades_venda
    """
    df = pd.read_sql_query(sql_query, conn)

    return df

def unique(param):
    sql_query = """
    SELECT distinct {} from propriedades_venda
    """.format(param)
    cursor.execute(sql_query)
    elements = cursor.fetchall()

    elements_list = []
    for element in elements:
        elements_list.append((''.join(element)).title())

    return elements_list

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

def bairro_metro_quadrado():
    sql_query = """
    SELECT 	
		bairro,
		regiao,
		cidade,
        sum(area)/sum(valor)
    from
        propriedades_venda
    group by
        bairro, regiao, cidade
    """
    df = pd.read_sql_query(sql_query, conn)

    return df

def get_median(element):
    sql_query = """
    SELECT 
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {}) AS median_value
    FROM 
    propriedades_venda;
    """.format(element)

    cursor.execute(sql_query)
    rounded_value = cursor.fetchone()[0]  
    return rounded_value

def valor_metro_quadrado():
    sql_query = """
    SELECT 
        cidade,
        regiao,
        bairro,
        ROUND(CAST(sum(valor)/sum(area) AS numeric),2) as valor
    from
        propriedades_venda
    where 
        valor is not null and area is not null
    group by
        cidade, bairro, regiao
    """
    df = pd.read_sql_query(sql_query, conn) 

    return df

def get_count():
    sql_query = """
    SELECT 
    count(valor)
    FROM 
    propriedades_venda;
    """

    cursor.execute(sql_query)
    count = cursor.fetchone()[0]  
    return count
