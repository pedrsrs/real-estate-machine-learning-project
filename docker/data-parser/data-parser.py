import datetime
import re
from kafka import KafkaConsumer
from protobuf.unparsed_html_message_pb2 import UnparsedHtmlMessage  
import psycopg2
from bs4 import BeautifulSoup

POSTGRES_HOST = 'postgres'
POSTGRES_DATABASE = 'real-estate-db'
POSTGRES_USER = 'user'
POSTGRES_PASSWORD = 'passwd'
POSTGRES_VENDA_TABLE = 'propriedades_venda'
POSTGRES_ALUGUEL_TABLE = 'propriedades_aluguel'

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

    return 'padrão'

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
    if "?" in url:
        pattern = re.compile(r'/([^?/]+)\?')
        match = pattern.search(url)
    else:
        pattern = re.compile(r'/([^/]+)$')
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

def send_postgres(data, table):
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DATABASE,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )

        cursor = conn.cursor()

        query = """
            INSERT INTO {} (titulo, tipo, subtipo, valor, iptu, condominio, quartos, area, vagas_garagem, banheiros, cidade, bairro, regiao, data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """.format(table)

        cursor.execute(query, data)
        conn.commit()
        print("Data sent to " + table + " table successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn is not None:
            conn.close()

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    title_element = soup.select_one('h2')
    property_price_element = soup.select_one('h3.olx-text.olx-text--body-large.olx-text--block.olx-text--semibold.olx-ad-card__price')

    title = title_element.text.strip() if title_element else None
    property_price = property_price_element.text.strip() if property_price_element else None

    location = soup.select_one('div.olx-ad-card__location-date-container > p').text.strip()
    data = soup.select_one('p.olx-ad-card__date--horizontal').text.strip()

    other_costs_elements = soup.select('div.olx-ad-card__priceinfo.olx-ad-card__priceinfo--horizontal > p')
    other_costs_values = [el.text.strip() for el in other_costs_elements] if other_costs_elements else []

    spans = soup.select('li.olx-ad-card__labels-item > span')
    labels_values = [span.get('aria-label', 'No Label').strip() for span in spans]

    return {
        'title': title,
        'property_price': property_price,
        'location': location,
        'data': data,
        'other_costs_values': other_costs_values,
        'labels_values': labels_values
    }

def main():

    consumer = KafkaConsumer('unparsed-data', bootstrap_servers=['kafka:29092'], api_version=(0, 10)) 
    consumer.subscribe(['unparsed-data'])  

    try:
        while True:
            for message in consumer:
                scraped_data_info = UnparsedHtmlMessage()
                scraped_data_info.ParseFromString(message.value)

                print("-"*10)
                print(scraped_data_info)
                print("-"*10)

                parsed_info = parse_html(scraped_data_info.unparsed_html)
                
                if parsed_info['title'] is not None:
                    titulo = parsed_info['title']
                tipo = parse_property_type(scraped_data_info.url)
                subtipo = [parse_property_subtype(scraped_data_info.url)]
                categoria = parse_category(scraped_data_info.url)
                if parsed_info['property_price'] is not None:
                    valor = parse_property_price(parsed_info['property_price'])
                iptu, condominio = parse_other_costs(parsed_info['other_costs_values'])
                quartos, area, vagas_garagem, banheiros = parse_information(parsed_info['labels_values'])
                cidade, bairro = parse_location(parsed_info['location'])
                regiao = parse_region(scraped_data_info.url)
                data = parse_date(parsed_info['data'])

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

                print(data)
                if titulo is not None and valor is not None:
                    if categoria == "venda":
                        table = POSTGRES_VENDA_TABLE
                        send_postgres(data, table)
                    elif categoria == "aluguel":
                        table = POSTGRES_ALUGUEL_TABLE
                        send_postgres(data, table)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

if __name__ == "__main__":
    main()
