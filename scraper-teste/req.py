import requests
from selectolax.parser import HTMLParser

def scrape_olx_data():
    # Make the cURL request
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.olx.com.br/imoveis/venda/apartamentos/estado-mg/belo-horizonte-e-regiao/barreiro?rts=302',
    }
    url = 'https://www.olx.com.br/imoveis/venda/apartamentos/cobertura/estado-mg/belo-horizonte-e-regiao/barreiro?o=2'
    response = requests.get(url, headers=headers)
    html_content = response.text

    # Parse the HTML content using Selectolax
    doc = HTMLParser(html_content)

    # Extract information from the parsed HTML
    # For example, to extract titles of all listings:
    listings = doc.css('.olx-ad-card__title')
    for listing in listings:
        title = listing.text(strip=True)
        print(title)

    # Add more extraction logic for other information you want to scrape

if __name__ == "__main__":
    scrape_olx_data()