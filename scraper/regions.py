import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OUTPUT_FILENAME = "unfiltered_links.txt"
URL = "https://www.olx.com.br/imoveis/venda/apartamentos/estado-mg/belo-horizonte-e-regiao"

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
    
def generate_other_payment_links(original_links):
    alternate_links = []

    for link in original_links:
        if '/venda/' in link:
            modified_link = link.replace('/venda/', '/aluguel/')
        elif '/aluguel/' in link:
            modified_link = link.replace('/aluguel/', '/venda/')

        alternate_links.append(modified_link)
    
    return alternate_links

def generate_other_property_types(original_links):
    alternate_links = []

    for link in original_links:
        if '/apartamentos/' in link:
            modified_link = link.replace('/apartamentos/', '/casas/')
        elif '/casas/' in link:
            modified_link = link.replace('/casas/', '/apartamentos/')

        alternate_links.append(modified_link)
    
    return alternate_links

def add_query_parameters(links):
    updated_links = []
    
    for link in links:
        if '/apartamentos/' in link:
            for variant in ['?rts=305', '?rts=304', '?rts=303', '?rts=302', ""]:
                updated_links.append(link + variant)
        elif '/casas/' in link:
            for variant in ['?rts=301', '?rts=300', ""]:
                updated_links.append(link + variant)
        else:
            updated_links.append(link)

    return updated_links

def write_to_file(links, filename=OUTPUT_FILENAME):
    with open(filename, 'w') as file:
        for link in links:
            file.write(link + '\n')

def scrape_regions(driver):

    try:
        elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div > div.olx-d-flex.olx-fd-column:nth-of-type(1) > div > div > div > div > a.olx-link.olx-link--caption.olx-link--main'))
        )
        original_links = [outer_div.get_attribute('href') for outer_div in elements]
        return original_links
    except TimeoutException:
        print("Timeout while waiting for elements. Refreshing the page and retrying.")
        driver.refresh()
        time.sleep(5) 
        return scrape_regions(driver)

def main():
    driver = initialize_driver()
    driver.get(URL)
    original_links = scrape_regions(driver)

    other_payment_methods = generate_other_payment_links(original_links)
    all_payment_types_links  = original_links + other_payment_methods 

    other_property_types = generate_other_property_types(all_payment_types_links)
    all_property_types_links = all_payment_types_links + other_property_types

    links_with_queries = add_query_parameters(all_property_types_links)

    write_to_file(links_with_queries)

    driver.quit()

if __name__ == "__main__":
    main()
