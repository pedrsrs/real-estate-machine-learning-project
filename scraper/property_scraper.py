import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from kafka import KafkaProducer
from protobuf.scraped_data_pb2 import ScrapedDataInfo
import json

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
}

producer = KafkaProducer(bootstrap_servers=['localhost:9093'], api_version=(0, 10, 1))

def initialize_driver():
    return webdriver.Chrome()

def get_elements(driver, url, class_name):
    driver.get(url)

    elements = WebDriverWait(driver, 35).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
    )
    return elements

def extract_information(element):
    title = element.find_element(By.CSS_SELECTOR, "h2").text
    property_price = element.find_element(By.CSS_SELECTOR, "h3.olx-text.olx-text--body-large.olx-text--block.olx-text--semibold.olx-ad-card__price").text
    location = element.find_element(By.CSS_SELECTOR, "div.olx-ad-card__location-date-container > p").text
    data = element.find_element(By.CSS_SELECTOR, "p.olx-ad-card__date--horizontal").text

    # Find other_costs elements, set to an empty list if not found
    other_costs_elements = element.find_elements(By.CSS_SELECTOR, "div.olx-ad-card__priceinfo.olx-ad-card__priceinfo--horizontal > p")
    other_costs_values = [el.text for el in other_costs_elements] if other_costs_elements else []

    # Find spans elements, set to an empty list if not found
    spans = element.find_elements(By.CSS_SELECTOR, 'li.olx-ad-card__labels-item > span')
    labels_values = [span.get_attribute('aria-label') if span.get_attribute('aria-label') else 'No Label' for span in spans]
    return title, property_price, location, data, other_costs_values, labels_values

def send_to_kafka(url, title, property_price, location, data, other_costs_values, labels_values):
    info_message = ScrapedDataInfo(
        url=url,
        title=title,
        property_price=property_price,
        location=location,
        data=data,
        other_costs=other_costs_values,
        labels=labels_values,
    )

    # Serialize the protobuf message to bytes
    serialized_info = info_message.SerializeToString()

    # Replace 'mytopic' with the actual Kafka topic you want to use
    kafka_topic = 'mytopic'

    try:
        # Produce the protobuf message to Kafka topic
        producer.send(kafka_topic, value=serialized_info)

        # Flush messages to ensure they are sent
        producer.flush()

        print(f"Message sent to Kafka: {info_message}")

    except Exception as e:
        print(f"Error sending message to Kafka: {e}")

def click_next_page(driver):
    try:
        next_button = driver.find_element(By.XPATH, '//span[contains(text(), "Próxima página")]')
        if next_button.is_enabled():
            next_button.click()
            return True
    except Exception as e:
        print(f"Error clicking next page button: {e}")
    return False

def main():
    driver = initialize_driver()

    url = 'https://www.olx.com.br/imoveis/venda/estado-sp/sao-paulo-e-regiao/zona-sul?pe=550000&ps=500001'
    class_name = 'renderIfVisible'

    while True:
        elements = get_elements(driver, url, class_name)

        for element in elements:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            info = extract_information(element)
            print(info)
            send_to_kafka(url, *info)

        if not click_next_page(driver):
            break

        next_url = driver.current_url
        if next_url != url:
            url = next_url
        else:
            break

if __name__ == "__main__":
    main()
