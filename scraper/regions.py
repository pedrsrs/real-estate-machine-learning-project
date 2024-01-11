from selenium import webdriver
import time
from selenium.webdriver.common.by import By

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

def write_to_file(links, filename="unfiltered_links.txt"):
    with open(filename, 'w') as file:
        for link in links:
            file.write(link + '\n')

def main():
    driver = webdriver.Chrome()
    driver.get('https://www.olx.com.br/imoveis/venda/apartamentos/estado-mg/belo-horizonte-e-regiao')
    time.sleep(5)

    outer_divs = driver.find_elements(By.CSS_SELECTOR, 'div > div.olx-d-flex.olx-fd-column:nth-of-type(1) > div > div > div > div > a.olx-link.olx-link--caption.olx-link--main')
    original_links = [outer_div.get_attribute('href') for outer_div in outer_divs]

    other_payment_methods = generate_other_payment_links(original_links)
    all_payment_types_links  = original_links + other_payment_methods 

    other_property_types = generate_other_property_types(all_payment_types_links)

    all_property_types_links = all_payment_types_links + other_property_types

    links_with_queries = add_query_parameters(all_property_types_links)

    write_to_file(links_with_queries)

    time.sleep(20)

    driver.quit()

if __name__ == "__main__":
    main()
