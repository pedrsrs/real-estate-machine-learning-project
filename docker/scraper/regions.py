import time
from playwright.sync_api import sync_playwright

OUTPUT_FILENAME = "unfiltered_links.txt"
URL = "https://www.olx.com.br/imoveis/venda/apartamentos/estado-mg/belo-horizonte-e-regiao"

def initialize_driver(browser):
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    page = context.new_page()
    page.goto(URL)
    return page

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

def scrape_regions(page):
    while True:
        original_links = []
        try:
            content = page.query_selector_all('div > div.olx-d-flex.olx-fd-column:nth-of-type(1) > div > div > div > div > a.olx-link.olx-link--caption.olx-link--main')            
            for element in content:
                region_link = element.get_attribute('href')
                original_links.append(region_link)
            
        except Exception as e:
            time.sleep(5) 
            page.reload()
            continue
        break
    return original_links

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = initialize_driver(browser)
        original_links = scrape_regions(page)

        other_payment_methods = generate_other_payment_links(original_links)
        all_payment_types_links  = original_links + other_payment_methods 

        other_property_types = generate_other_property_types(all_payment_types_links)
        all_property_types_links = all_payment_types_links + other_property_types

        links_with_queries = add_query_parameters(all_property_types_links)

        write_to_file(links_with_queries)

        page.close()
        browser.close()

if __name__ == "__main__":
    main()
