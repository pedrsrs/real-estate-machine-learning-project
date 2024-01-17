import datetime
import re
from kafka import KafkaConsumer
from protobuf.scraped_data_pb2 import ScrapedDataInfo  
from protobuf.parsed_property_data_pb2 import ParsedPropertyData  

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
        "jan.": "01",
        "fev.": "02",
        "mar.": "03",
        "abr.": "04",
        "mai.": "05",
        "jun.": "06",
        "jul.": "07",
        "ago.": "08",
        "set.": "09",
        "out.": "10",
        "nov.": "11",
        "dez.": "12"
    }

    transformed_date = None

    if "hoje" in date.lower():
        transformed_date = today
    elif "ontem" in date.lower():
        transformed_date = today - datetime.timedelta(days=1)
    elif "anteontem" in date.lower():
        transformed_date = today - datetime.timedelta(days=2)
    else:
        date_str = date.replace("de", "")
        day, month_str = date_str.split()
        month = month_names[month_str]
        year = today.year if (today.month > int(month)) or (today.month == int(month) and today.day > (int(day) + 2)) else today.year - 1
        transformed_date = datetime.date(year, int(month), int(day))

    if transformed_date is not None:
        transformed_date_str = transformed_date.strftime('%d/%m/%Y')
    
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
    cidade = location.split(",")[0]
    bairro = location.split(",")[1]

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

def send_postgres_venda(message):
    quartos = area = vagas_garagem = banheiros = None


def send_postgres_aluguel(message):
    quartos = area = vagas_garagem = banheiros = None


def main():
    conf = {
        'bootstrap.servers': 'localhost:9093', 
        'group.id': 'group1',  
        'auto.offset.reset': 'earliest',  
    }

    consumer = KafkaConsumer('mytopic', bootstrap_servers=['localhost:9093'], api_version=(0, 10))
    consumer.subscribe(['mytopic'])

    try:
        while True:
            for message in consumer:
                scraped_data_info = ScrapedDataInfo()
                scraped_data_info.ParseFromString(message.value)

                titulo = scraped_data_info.title
                tipo = parse_property_type(scraped_data_info.url)
                subtipo = parse_property_subtype(scraped_data_info.url)
                categoria = parse_category(scraped_data_info.url)
                valor = parse_property_price(scraped_data_info.property_price)
                iptu, condominio = parse_other_costs(scraped_data_info.other_costs)
                quartos, area, vagas_garagem, banheiros = parse_information(scraped_data_info.labels)
                cidade, bairro = parse_location(scraped_data_info.location)
                regiao = parse_region(scraped_data_info.url)

                message = ParsedPropertyData(
                    titulo=titulo,
                    tipo=tipo,
                    subtipo=subtipo,
                    valor=valor,
                    iptu=iptu,
                    condominio=condominio,
                    quartos=quartos,
                    area=area,
                    vagas_garagem=vagas_garagem,
                    banheiros=banheiros,
                    cidade=cidade,
                    bairro=bairro,
                    regiao=regiao
                )

                if categoria == "venda":
                    send_postgres_venda(message)
                elif categoria == "aluguel":
                    send_postgres_aluguel(message)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

if __name__ == "__main__":
    main()
