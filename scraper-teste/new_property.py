import time
import pandas as pd
from kafka import KafkaProducer
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from protobuf.unparsed_html_message_pb2 import UnparsedHtmlMessage
from protobuf.scraping_progress_status_pb2 import ScrapingProgressStatus

NUMBER_OF_DRIVERS = 1
INPUT_FILE = 'olx_links.csv'

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
}

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10, 1))

def initialize_driver(start_url=None):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    
    if start_url:
        driver.get(start_url)

    return driver


def get_elements(driver, url):
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 20) 
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div[1]/main/div/div[2]/main/div[4]/div[contains(@class, 'renderIfVisible')]")))
        next_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Próxima página")]')))
        return elements
    except TimeoutException:
        print("Timeout while waiting for elements. Refreshing the page and retrying.")
        driver.refresh()
        time.sleep(1) 
        return get_elements(driver, url)

def send_scraped_data_kafka(url, unparsed_html, driver_index):
    info_message = UnparsedHtmlMessage(
        url=url,
        unparsed_html=unparsed_html
    )
    serialized_info = info_message.SerializeToString()

    kafka_topic = 'unparsed-data'

    try:
        producer.send(kafka_topic, value=serialized_info)
        producer.flush()

        print(f"Message sent to Kafka by driver {driver_index}")

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
def open_new_window(driver, url):
    # Execute JavaScript to open a new window with the provided URL
    driver.execute_script(f"window.open('{url}', '_blank');")
def scrape_data(driver, original_url, driver_index):
    current_url = original_url

    while True:
        time.sleep(3)
        elements = get_elements(driver, current_url)

        for element in elements:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                content_element = element.find_element(By.XPATH, './/section/div[contains(@class, "olx-ad-card__content")]')
                if content_element:
                    unparsed_html = content_element.get_attribute("outerHTML")
                    send_scraped_data_kafka(original_url, unparsed_html, driver_index)

            except Exception as e:
                print(f"Error extracting outerHTML: {e}")
        
        # Click next page and get the new driver instance
        driver = click_next_page(driver)

        if driver is None:
            send_scraping_progress_kafka(original_url, 'finished')
            break  # Exit the loop if there's no next page

def click_next_page(driver):
    try:
        next_button = driver.find_element(By.XPATH, '//span[contains(text(), "Próxima página")]')
        
        if next_button.is_enabled():
            time.sleep(2)
            next_page_url = next_button.find_element(By.XPATH, './/parent::a').get_attribute('href')
            print(next_page_url)
            driver.quit()  # Quit the current driver instance
            return initialize_driver(next_page_url)  # Initialize a new driver instance with the next page URL
        
    except Exception as e:
        print(f"Error clicking the next page button: {e}")

    return None

def run_scraping_process(driver, urls, driver_index):
    for url in urls:
        send_scraping_progress_kafka(url, 'started')
        scrape_data(driver, url, driver_index)
        time.sleep(3)

if __name__ == "__main__":
    df = pd.read_csv(INPUT_FILE)
    urls = df['url'].tolist()

    drivers = [initialize_driver() for _ in range(NUMBER_OF_DRIVERS)]

    urls_per_thread = len(urls) // len(drivers)
    url_chunks = [urls[i:i+urls_per_thread] for i in range(0, len(urls), urls_per_thread)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, (driver, url_chunk) in enumerate(zip(drivers, url_chunks)):
            executor.submit(run_scraping_process, driver, url_chunk, i)

    for driver in drivers:
        driver.quit()
