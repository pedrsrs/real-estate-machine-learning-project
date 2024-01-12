import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_driver():
    return webdriver.Chrome()

def get_elements(driver, url, class_name):
    driver.get(url)

    elements = WebDriverWait(driver, 35).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
    )
    return elements

def extract_information(element):
    title = element.find_element(By.CSS_SELECTOR, "h2").text
    property_price = element.find_element(By.CSS_SELECTOR, "h3.olx-text.olx-text--body-large.olx-text--block.olx-text--semibold.olx-ad-card__price").text
    location = element.find_element(By.CSS_SELECTOR, "div.olx-ad-card__location-date-container > p").text
    data = element.find_element(By.CSS_SELECTOR, "p.olx-ad-card__date--horizontal").text

    other_costs_elements = element.find_elements(By.CSS_SELECTOR, "div.olx-ad-card__priceinfo.olx-ad-card__priceinfo--horizontal > p")
    other_costs = [el.text for el in other_costs_elements]

    spans = element.find_elements(By.CSS_SELECTOR, 'li.olx-ad-card__labels-item > span')
    labels = [span.get_attribute('aria-label') for span in spans]

    return title, property_price, location, data, other_costs, labels

def print_information(url, title, property_price, location, data, other_costs, labels):
    print(url)
    print(title)
    print(property_price)
    print(location)
    print(data)
    print(other_costs)
    print(labels)
    print("-" * 10)
    #time.sleep(0.3)

def click_next_page(driver):
    try:
        next_button = driver.find_element(By.XPATH, '//span[contains(text(), "Próxima página")]')
        if next_button.is_enabled():
            next_button.click()
            return True
    except Exception as e:
        print(f"Error clicking next page button: {e}")
    return False

def main():
    driver = initialize_driver()

    url = 'https://www.olx.com.br/imoveis/venda/estado-sp/sao-paulo-e-regiao/zona-sul?pe=550000&ps=500001'
    class_name = 'renderIfVisible'

    while True:
        elements = get_elements(driver, url, class_name)

        for element in elements:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            info = extract_information(element)
            print_information(url, *info)

        if not click_next_page(driver):
            break

        next_url = driver.current_url
        if next_url != url:
            url = next_url
        else:
            break

if __name__ == "__main__":
    main()
