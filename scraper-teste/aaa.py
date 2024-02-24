import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
INPUT_FILE = "olx_links.csv"
NUM_OF_WORKERS = 30

def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return [row['url'] for row in reader if row['status'] != 'finished']
    
urls = read_csv(INPUT_FILE)
url_chunks = [urls[i::NUM_OF_WORKERS] for i in range(NUM_OF_WORKERS)]

print(url_chunks)