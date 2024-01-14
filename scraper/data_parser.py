import re
from kafka import KafkaConsumer
from protobuf.scraped_data_pb2 import ScrapedDataInfo  
from protobuf.parsed_data_pb2 import ParsedPropertyData  

def parse_property_type(url):
    tipo = None
    if '/apartamentos/' in url:
        tipo = "apartamento"
    elif '/casas/' in url:
        tipo = "casa"
    return tipo

def parse_property_subtype(url):
    subtipo = None
    if 'rts=300' in url:
        subtipo = "apartamento"
    elif 'rts=301' in url:
        subtipo = "casa"
    elif 'rts=302' in url:
        subtipo = "casa"
    elif 'rts=303' in url:
        subtipo = "casa"
    elif 'rts=304' in url:
        subtipo = "casa"
    elif 'rts=305' in url:
        subtipo = "casa"
    elif 'rts=306' in url:
        subtipo = "casa"
    return subtipo

def parse_category(url):
    categoria = None

    if '/venda/' in url:
        categoria = "venda"
    elif '/aluguel/' in url:
        categoria = "aluguel"
    
    return categoria

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

def send_db(labels):
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

                message = ParsedPropertyData(
                    titulo=titulo,
                    tipo=tipo,
                    subtipo=subtipo,
                    categoria=categoria,
                    valor=valor,
                    iptu=iptu,
                    condominio=condominio,
                    quartos=quartos,
                    area=area,
                    vagas_garagem=vagas_garagem,
                    banheiros=banheiros,
                    cidade=cidade,
                    bairro=bairro
                )

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

if __name__ == "__main__":
    main()

    