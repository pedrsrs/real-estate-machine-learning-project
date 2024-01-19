import datetime
import re
from kafka import KafkaConsumer
from protobuf.scraped_data_pb2 import ScrapedDataInfo  
import psycopg2

def parse_property_type(url):
    tipo = None
    if '/apartamentos/' in url:
        tipo = "apartamento"
    elif '/casas/' in url:
        tipo = "casa"
    return tipo

def parse_property_subtype(url):
    subtype_mapping = {
        'rts=300': 'casa de condomínio',
        'rts=301': 'casa de vila',
        'rts=302': 'cobertura',
        'rts=303': 'duplex ou triplex',
        'rts=304': 'kitnet',
        'rts=305': 'loft'
    }

    for filter, subtype in subtype_mapping.items():
        if filter in url:
            return subtype

    return None

def parse_category(url):
    categoria = None

    if '/venda/' in url:
        categoria = "venda"
    elif '/aluguel/' in url:
        categoria = "aluguel"
    
    return categoria

def parse_date(date):
    today = datetime.date.today() 
    month_names = {
        "jan": "01",
        "fev": "02",
        "mar": "03",
        "abr": "04",
        "mai": "05",
        "jun": "06",
        "jul": "07",
        "ago": "08",
        "set": "09",
        "out": "10",
        "nov": "11",
        "dez": "12"
    }

    transformed_date = None

    if "hoje" in date.lower():
        transformed_date = today
    elif "ontem" in date.lower():
        transformed_date = today - datetime.timedelta(days=1)
    elif "anteontem" in date.lower():
        transformed_date = today - datetime.timedelta(days=2)
    else:
        date_str = date.split(",")[0]
        date_str = date_str.replace(" de ", " ")
        day, month_str = date_str.split()
        month = month_names[month_str]
        year = today.year if (today.month > int(month)) or (today.month == int(month) and today.day >= (int(day) + 2)) else today.year - 1
        transformed_date = datetime.date(year, int(month), int(day))

    if transformed_date is not None:
        transformed_date_str = transformed_date.strftime('%Y-%m-%d')
    
    return transformed_date_str


def parse_other_costs(other_costs):
    iptu = condominio = None

    for item in other_costs:
        if 'IPTU' in item:
            iptu = int(item.split()[-1].replace(".", ""))
        elif 'Condomínio' in item:
            condominio = int(item.split()[-1].replace(".", ""))

    return iptu, condominio

def parse_property_price(unparsed_property_price):
    property_price_digits = re.findall(r'\d+', unparsed_property_price)
    concatenated_price = ''.join(property_price_digits)
    return int(concatenated_price)

def parse_location(location):
    if "," in location:
        cidade, bairro = location.split(",", 1)  
    else:
        cidade, bairro = None, location

    return cidade, bairro

def parse_region(url):
    pattern = re.compile(r'/([^?/]+)\?')
    match = pattern.search(url)

    if match:
        result = match.group(1).replace('-', ' ')
        return result
    else:
        return None

def parse_information(labels):
    quartos = area = vagas_garagem = banheiros = None

    for item in labels:
        if 'quarto' in item:
            quartos = int(item.split()[0])
        elif 'metro' in item:
            area = int(item.split()[0])
        elif 'garagem' in item:
            vagas_garagem = int(item.split()[0])
        elif 'banheiro' in item:
            banheiros = int(item.split()[0])

    return quartos, area, vagas_garagem, banheiros

def send_postgres_venda(data):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="real-estate-db",
            user="user",
            password="passwd"
        )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO propriedades_venda (titulo, tipo, subtipo, valor, iptu, condominio, quartos, area, vagas_garagem, banheiros, cidade, bairro, regiao, data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data)

        conn.commit()
        print("Data sent to propriedades_venda table successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn is not None:
            conn.close()

def send_postgres_aluguel(data):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="real-estate-db",
            user="user",
            password="passwd"
        )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO propriedades_aluguel (titulo, tipo, subtipo, valor, iptu, condominio, quartos, area, vagas_garagem, banheiros, cidade, bairro, regiao, data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data)

        conn.commit()
        print("Data sent to propriedades_aluguel table successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn is not None:
            conn.close()

def main():
    conf = {
        'bootstrap.servers': 'localhost:9092',  
        'group.id': 'group1',
        'auto.offset.reset': 'earliest',
    }

    consumer = KafkaConsumer('unparsed-data', bootstrap_servers=['localhost:9092'], api_version=(0, 10)) 
    consumer.subscribe(['unparsed-data'])  

    try:
        while True:
            for message in consumer:
                scraped_data_info = ScrapedDataInfo()
                scraped_data_info.ParseFromString(message.value)

                titulo = scraped_data_info.title
                tipo = parse_property_type(scraped_data_info.url)
                subtipo = [parse_property_subtype(scraped_data_info.url)]
                categoria = parse_category(scraped_data_info.url)
                valor = parse_property_price(scraped_data_info.property_price)
                iptu, condominio = parse_other_costs(scraped_data_info.other_costs)
                quartos, area, vagas_garagem, banheiros = parse_information(scraped_data_info.labels)
                cidade, bairro = parse_location(scraped_data_info.location)
                regiao = parse_region(scraped_data_info.url)
                data = parse_date(scraped_data_info.data)

                data = (
                    titulo,
                    tipo,
                    subtipo,
                    valor,
                    iptu,
                    condominio,
                    quartos,
                    area,
                    vagas_garagem,
                    banheiros,
                    cidade,
                    bairro,
                    regiao,
                    data
                )

                if categoria == "venda":
                    send_postgres_venda(data)
                elif categoria == "aluguel":
                    send_postgres_aluguel(data)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

if __name__ == "__main__":
    main()
