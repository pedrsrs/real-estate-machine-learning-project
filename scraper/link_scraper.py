import re
import csv
import scrapy
from scrapy.crawler import CrawlerProcess
from queue import Queue

INPUT_FILE_NAME = 'unfiltered_links.txt'
OUTPUT_FILE_NAME = 'olx_links.csv'

MIN_PRICE = 0
MAX_PRICE = 100000000
MAX_RESULTS_PER_SEARCH = 5000

class OlxSpider(scrapy.Spider):
    name = 'olx'
    custom_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    def __init__(self):
        self.link_queue = Queue()
        self.read_links_from_file()  

    def read_links_from_file(self):
        with open(INPUT_FILE_NAME, 'r') as f:
            for link in f:
                link = link.strip()  
                self.link_queue.put(link)

    def start_requests(self):
        if not self.link_queue.empty():
            yield scrapy.Request(self.link_queue.get(), headers=self.custom_headers, callback=self.parse_page)

    def parse_page(self, response):
        olx_result_number = re.search(
            r'de\s(.*?)\sresultados',
            response.css('.olx-text.olx-text--body-small.olx-text--block.olx-text--regular.olx-color-neutral-110::text').get().strip()
        )   
        if olx_result_number:
            unparsed_number_of_results = olx_result_number.group(1)
            number_of_results = unparsed_number_of_results.replace('.', '')

            if self.verify_result_size(int(number_of_results)):
                if int(number_of_results) > 0:
                    data = {
                        "url": response.url,
                        "qtd": number_of_results
                    }
                    self.write_to_csv(data)

            else:
                self.divide_links(response.url)

        if not self.link_queue.empty():
            next_link = self.link_queue.get()
            yield scrapy.Request(next_link, headers=self.custom_headers, callback=self.parse_page)

    def verify_result_size(self, number_of_results):
        return number_of_results <= MAX_RESULTS_PER_SEARCH
        
    def divide_links(self, url):
        if "pe=" in url:
            min_price = int(re.search(r'pe=(\d+)', url).group(1))
            max_price = int(re.search(r'ps=(\d+)', url).group(1))
        else: 
            min_price = MIN_PRICE
            max_price = MAX_PRICE

        half_point = (min_price + max_price) // 2 

        if "rts=" in url:
            query_character = "&"
        else:
            query_character = "?"

        new_links = [
            f'{url.split(query_character)[0]}{query_character}pe={half_point + 1}&ps={max_price}',
            f'{url.split(query_character)[0]}{query_character}pe={min_price}&ps={half_point}'
        ]
        self.link_queue.queue.extendleft(new_links)
    
    def write_to_csv(self, data):
        with open(OUTPUT_FILE_NAME, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["url", "qtd"])

            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(data)

process = CrawlerProcess()
process.crawl(OlxSpider)
process.start()