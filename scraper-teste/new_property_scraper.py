import csv
import time
from multiprocessing import Process
from kafka import KafkaProducer
from playwright.sync_api import sync_playwright
from protobuf.unparsed_html_message_pb2 import UnparsedHtmlMessage
from protobuf.scraping_progress_status_pb2 import ScrapingProgressStatus

NUM_OF_WORKERS = 4
INPUT_FILE = 'olx_links.csv'

def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return [row['url'] for row in reader if row['status'] != 'finished']
        
def send_scraped_data_kafka(url, unparsed_html):
    producer = KafkaProducer(bootstrap_servers="localhost:9092")
    info_message = UnparsedHtmlMessage(
        url=url,
        unparsed_html=unparsed_html
    )
    serialized_info = info_message.SerializeToString()

    kafka_topic = 'unparsed-data'

    try:
        producer.send(kafka_topic, value=serialized_info)
        producer.flush()

    except Exception as e:
        print(f"Error sending message to Kafka: {e}")
    
def send_scraping_progress_kafka(url, status):
    producer = KafkaProducer(bootstrap_servers="localhost:9092")
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

def get_elements(page, url, browser):
    scrape(page, url)
    goto_next_page(page, url, browser)

def goto_next_page(page, url, browser):
    next_page_button = page.query_selector("text=Próxima página")

    next_page_url = page.evaluate("(element) => element.closest('a').href", next_page_button)
    print(next_page_url)
    if next_page_url:
        page.close()
        time.sleep(2)
        page = new_page(next_page_url, browser)
        get_elements(page, url, browser)
    else:
        page.close()

def scrape(page, url):
    while True:
        try:
            main_content = page.query_selector('main#main-content > div:nth-child(4)')
            render_if_visible_elements = main_content.query_selector_all('.renderIfVisible')

            for elements in render_if_visible_elements:
                page.evaluate("element => element.scrollIntoView(true);", elements)
                content = elements.query_selector('section > div.olx-ad-card__content')
                html = content.evaluate("el => el.outerHTML")
                send_scraped_data_kafka(url, html) 
                print("data sent")
               
        except Exception as e:
            time.sleep(1)
            page.reload()
            time.sleep(3)
            continue
        break

def new_page(url, browser):
    while True:
        try:
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
            page = context.new_page()
            page.goto(url)
            time.sleep(3)
        except Exception as e:
            page.close()
            time.sleep(1)
            continue
        break

    return page

def scrape_elements(urls):
    scraped_data = {}

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for url in urls:
            page = new_page(url, browser)
            send_scraping_progress_kafka(url, "started")
            print("starting link:", url)
            get_elements(page, url, browser)
            page.close()
            send_scraping_progress_kafka(url, "finished")
        browser.close()

    return scraped_data

if __name__ == "__main__":
    urls = read_csv(INPUT_FILE)
    url_chunks = [urls[i::NUM_OF_WORKERS] for i in range(NUM_OF_WORKERS)]

    processes = []
    for chunk in url_chunks:
        process = Process(target=scrape_elements, args=(chunk,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()  
