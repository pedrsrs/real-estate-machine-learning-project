from selenium import webdriver
import time
from selenium.webdriver.common.by import By

def generate_alternate_links(original_links):
    alternate_links = []

    for link in original_links:
        if '/venda/' in link:
            modified_link = link.replace('/venda/', '/aluguel/')
        elif '/aluguel/' in link:
            modified_link = link.replace('/aluguel/', '/venda/')

        alternate_links.append(modified_link)
    
    return alternate_links

def generate_alternate_property(original_links):
    alternate_links = []

    for link in original_links:
        if '/apartamentos/' in link:
            modified_link = link.replace('/apartamentos/', '/casas/')
        elif '/casas/' in link:
            modified_link = link.replace('/casas/', '/apartamentos/')

        alternate_links.append(modified_link)
    
    return alternate_links

driver = webdriver.Chrome()

driver.get('https://www.olx.com.br/imoveis/venda/apartamentos/estado-sp/sao-paulo-e-regiao')

time.sleep(5)
outer_divs = driver.find_elements(By.CSS_SELECTOR, 'div > div.olx-d-flex.olx-fd-column:nth-of-type(1) > div > div > div > div > a.olx-link.olx-link--caption.olx-link--main')
original_links = [outer_div.get_attribute('href') for outer_div in outer_divs]

alternate_links = generate_alternate_links(original_links)
combined_links = original_links + alternate_links

new_alternate_links = generate_alternate_property(combined_links)

new_combined = combined_links + new_alternate_links
for link in new_combined:
    print(link)

time.sleep(20)

driver.quit()


#https://www.olx.com.br/imoveis/venda + apartamento / estado / cidade / zona ? (preço) & rts = 

#?rts=306 - padrao
#?rts=305 - loft
#?rts=303 - duplex ou triplex
#?rts=303 - Kitnet
#?rts=302 - cobertura

#?rts=306 - padrao
#?rts=301 - casa de vila
#?rts=300 - casa de condominio
