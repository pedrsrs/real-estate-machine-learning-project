import re
import datetime
import psycopg2
from kafka import KafkaConsumer
from selectolax.parser import HTMLParser
from protobufs.unparsed_html_message_pb2 import UnparsedHtmlMessage  

POSTGRES_HOST = 'postgres'
POSTGRES_DATABASE = 'real-estate-db'
POSTGRES_USER = 'user'
POSTGRES_PASSWORD = 'passwd'
POSTGRES_VENDA_TABLE = 'propriedades_venda'
POSTGRES_ALUGUEL_TABLE = 'propriedades_aluguel'
SCRAPING_DATE_RECORD = 'data/scraping_start_date.txt'

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
            INSERT INTO {} (titulo, tipo, subtipo, valor, iptu, condominio, quartos, area, vagas_garagem, banheiros, cidade, bairro, regiao, anuncio_data, link, anuncio_id, coleta_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
    parser = HTMLParser(html)

    try:

        title = parser.css_first('h2').text(strip=True) if parser.css_first('h2') else None
        property_price = parser.css_first('h3.olx-ad-card__price').text(strip=True) if parser.css_first('h3.olx-ad-card__price') else None

        location = parser.css_first('div.olx-ad-card__location-date-container > p').text(strip=True) if parser.css_first('div.olx-ad-card__location-date-container > p') else None
        data = parser.css_first('p.olx-ad-card__date--horizontal').text(strip=True) if parser.css_first('p.olx-ad-card__date--horizontal') else None

        other_costs_elements = parser.css('div.olx-ad-card__priceinfo.olx-ad-card__priceinfo--horizontal > p') if parser.css('div.olx-ad-card__priceinfo.olx-ad-card__priceinfo--horizontal > p') else None
        other_costs_values = [el.text(strip=True) for el in other_costs_elements] if other_costs_elements else []

        spans = parser.css('li.olx-ad-card__labels-item > span') if parser.css('li.olx-ad-card__labels-item > span') else None
        labels_values = [span.attrs.get('aria-label', 'No Label').strip() for span in spans] if spans else []

        link = parser.css_first('a.olx-ad-card__title-link').attrs.get('href') if parser.css_first('a.olx-ad-card__title-link') else None
        
        anuncio_id = (re.search(r'-(\d+)$', link)).group(1) if link else None

    except Exception as e:
        pass

    return {
        'title': title,
        'property_price': property_price,
        'location': location,
        'data': data,
        'other_costs_values': other_costs_values,
        'labels_values': labels_values,
        'link': link,
        'anuncio_id': anuncio_id
    }

def build_data(parsed_info, scraped_data_info):
    titulo = parsed_info['title']
    tipo = parse_property_type(scraped_data_info.url)
    subtipo = [parse_property_subtype(scraped_data_info.url)]
    valor = parse_property_price(parsed_info['property_price'])
    iptu, condominio = parse_other_costs(parsed_info['other_costs_values'])
    quartos, area, vagas_garagem, banheiros = parse_information(parsed_info['labels_values'])
    cidade, bairro = parse_location(parsed_info['location'])
    regiao = parse_region(scraped_data_info.url)
    anuncio_data = parse_date(parsed_info['data'])
    link = parsed_info['link']
    anuncio_id = parsed_info['anuncio_id'] 

    with open(SCRAPING_DATE_RECORD, 'r') as file:
        coleta_data = file.readline().strip()

    categoria = parse_category(scraped_data_info.url)

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
        anuncio_data,
        link, 
        anuncio_id,
        coleta_data
    )
    return data, categoria

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
                
                data, categoria = build_data(parsed_info, scraped_data_info)

                print(data)
                if data[0] is not None and data[3] is not None:
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