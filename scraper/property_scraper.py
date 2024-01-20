import time
import pandas as pd
from kafka import KafkaProducer
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  
from selenium.webdriver.chrome.options import Options
from protobuf.scraped_data_pb2 import ScrapedDataInfo

NUMBER_OF_DRIVERS = 3

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
}

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10, 1))

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    return webdriver.Chrome(options=chrome_options)

def get_elements(driver, url, class_name):
    driver.get(url)

    try:
        elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )
        return elements
    except TimeoutException:
        print("Timeout while waiting for elements. Refreshing the page and retrying.")
        driver.refresh()
        time.sleep(5) 
        return get_elements(driver, url, class_name)

def extract_information(element):
    title = element.find_element(By.CSS_SELECTOR, "h2").text
    property_price = element.find_element(By.CSS_SELECTOR, "h3.olx-text.olx-text--body-large.olx-text--block.olx-text--semibold.olx-ad-card__price").text
    location = element.find_element(By.CSS_SELECTOR, "div.olx-ad-card__location-date-container > p").text
    data = element.find_element(By.CSS_SELECTOR, "p.olx-ad-card__date--horizontal").text

    other_costs_elements = element.find_elements(By.CSS_SELECTOR, "div.olx-ad-card__priceinfo.olx-ad-card__priceinfo--horizontal > p")
    other_costs_values = [el.text for el in other_costs_elements] if other_costs_elements else []

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
    serialized_info = info_message.SerializeToString()

    kafka_topic = 'unparsed-data'

    try:
        producer.send(kafka_topic, value=serialized_info)
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
        print(f"Error clicking the next page button: {e}")
    return False

def scrape_data(driver, url, class_name):
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

def run_scraping_process(driver, urls, class_name):
    for url in urls:
        scrape_data(driver, url, class_name)

if __name__ == "__main__":

    df = pd.read_csv('olx_links.csv')
    urls = df['url'].tolist()

    drivers = [initialize_driver() for _ in range(NUMBER_OF_DRIVERS)]

    urls_per_thread = len(urls) // len(drivers)
    url_chunks = [urls[i:i+urls_per_thread] for i in range(0, len(urls), urls_per_thread)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_scraping_process, drivers, url_chunks, ['renderIfVisible']*len(url_chunks))

    for driver in drivers:
        driver.quit()
