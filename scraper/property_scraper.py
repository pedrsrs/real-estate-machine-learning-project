import time
import pandas as pd
from kafka import KafkaProducer
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from protobuf.unparsed_html_message_pb2 import UnparsedHtmlMessage
from protobuf.scraping_progress_status_pb2 import ScrapingProgressStatus

NUMBER_OF_DRIVERS = 1
INPUT_FILE = 'olx_links.csv'

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
}

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10, 1))

def initialize_driver():
    firefox_options = Options()
    firefox_options.add_argument("--window-size=1920,1080")
    firefox_options.add_argument("--disable-extensions")
    firefox_options.add_argument("--proxy-server='direct://'")
    firefox_options.add_argument("--proxy-bypass-list=*")
    firefox_options.add_argument("--start-maximized")
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--disable-dev-shm-usage')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument('--ignore-certificate-errors')
    firefox_options.add_argument("--enable-javascript")
    firefox_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/97.0 Safari/537.3")

    return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)

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

def send_scraped_data_kafka(url, unparsed_html):
    info_message = UnparsedHtmlMessage(
        url=url,
        unparsed_html=unparsed_html
    )
    serialized_info = info_message.SerializeToString()

    kafka_topic = 'unparsed-data'

    try:
        producer.send(kafka_topic, value=serialized_info)
        producer.flush()

        print(f"Message sent to Kafka: {info_message}")

    except Exception as e:
        print(f"Error sending message to Kafka: {e}")

def send_scraping_progress_kafka(url, status):
    progress_message = ScrapingProgressStatus(
        url=url,
        status=status
    )
    serialized_progress = progress_message.SerializeToString()

    kafka_topic = 'scraping-progress'

    try:
        producer.send(kafka_topic, value=serialized_progress)
        producer.flush()

        print(f"Progress message sent to Kafka: {progress_message}")

    except Exception as e:
        print(f"Error sending progress message to Kafka: {e}")

def click_next_page(driver):
    try:
        next_button = driver.find_element(By.XPATH, '//span[contains(text(), "Próxima página")]')
        
        if next_button.is_enabled():
            next_button.click()

            return True
        
    except Exception as e:
        print(f"Error clicking the next page button: {e}")

    return False

def scrape_data(driver, original_url, class_name):
    current_url = original_url

    while True:
        elements = get_elements(driver, current_url, class_name)

        for element in elements:
            try:
                content_element = element.find_element(By.XPATH, './/div[contains(@class, "olx-ad-card")]')
                driver.execute_script("arguments[0].scrollIntoView(true);", content_element)
                unparsed_html = content_element.get_attribute("outerHTML")
                send_scraped_data_kafka(original_url, unparsed_html)

            except Exception as e:
                print(f"Error extracting outerHTML: {e}")

        if not click_next_page(driver):
            send_scraping_progress_kafka(original_url, 'finished')
            break

        next_url = driver.current_url
        if next_url != current_url:
            current_url = next_url
        else:
            send_scraping_progress_kafka(original_url, 'finished')
            break

def run_scraping_process(driver, urls, class_name):
    for url in urls:
        send_scraping_progress_kafka(url, 'started')
        scrape_data(driver, url, class_name)

if __name__ == "__main__":
    df = pd.read_csv(INPUT_FILE)
    urls = df.loc[df['status'] != 'finished', 'url'].tolist()

    drivers = [initialize_driver() for _ in range(NUMBER_OF_DRIVERS)]

    urls_per_thread = len(urls) // len(drivers)
    url_chunks = [urls[i:i+urls_per_thread] for i in range(0, len(urls), urls_per_thread)]

    class_names = ['renderIfVisible']*len(url_chunks)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_scraping_process, drivers, url_chunks, class_names)

    for driver in drivers:
        driver.quit()