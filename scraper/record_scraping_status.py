import pandas as pd
from kafka import KafkaConsumer
from protobuf.scraping_progress_status_pb2 import ScrapingProgressStatus

RECORD_FILE = 'olx_links.csv'

def record_status_in_csv(url, status):
    df = pd.read_csv(RECORD_FILE)
    df.loc[df['url'] == url, 'status'] = status
    df.to_csv(RECORD_FILE, index=False)

def main():
    
    consumer = KafkaConsumer('scraping-progress', bootstrap_servers=['localhost:9092'], api_version=(0, 10)) 
    consumer.subscribe(['scraping-progress'])  

    try:
        while True:
            for message in consumer:
                scraper_status_message = ScrapingProgressStatus()
                scraper_status_message.ParseFromString(message.value)

                record_status_in_csv(scraper_status_message.url, scraper_status_message.status)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

if __name__ == "__main__":
    main()
