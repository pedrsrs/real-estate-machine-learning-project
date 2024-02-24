from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_driver():
    driver = webdriver.Chrome()  # Change this to your preferred webdriver
    return driver

def navigate_to_page(driver, url):
    driver.get(url)

def collect_information(driver):
    # Example of collecting information, modify as needed
    next_button = driver.find_element(By.XPATH, '//span[contains(text(), "Próxima página")]')    
    parent_span = next_button.find_element(By.XPATH, './/parent::a').get_attribute('href')

    print(parent_span)


def close_driver(driver):
    driver.quit()
#/html/body/div[1]/div[1]/main/div/div[2]/main/div[4]/div[contains(@class, 'renderIfVisible')]
if __name__ == "__main__":
    url = "https://www.olx.com.br/imoveis/venda/apartamentos/cobertura/estado-mg/belo-horizonte-e-regiao/barreiro?o=2"
    driver = start_driver()
    try:
        navigate_to_page(driver, url)
        information = collect_information(driver)
    finally:
        close_driver(driver)
