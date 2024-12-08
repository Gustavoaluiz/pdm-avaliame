from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

# Caminhos para o Chrome e o ChromeDriver
CHROME_PATH = 'D:\\Scrapping\\chrome-win64\\chrome-win64\\chrome.exe'
CHROMEDRIVER_PATH = 'D:\\Scrapping\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'

# URL base com cidade variável
BASE_URL = 'https://www.google.com/maps/search/{cidade}+Restaurantes'

# Função para extrair dados de cada restaurante
def get_restaurant_data(driver):
    print("Coletando dados dos restaurantes...")
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK.THOPZb.CpccDe')  # Localiza os cards de restaurante
    print(f"Total de restaurantes encontrados: {len(elements)}")
    data_list = []

    for i, element in enumerate(elements):
        print(f"Coletando dados do restaurante {i + 1}...")
        try:
            # Link do restaurante
            href = element.find_element(By.CSS_SELECTOR, 'a.hfpxzc').get_attribute('href')
        except NoSuchElementException:
            href = None

        try:
            # Nome do restaurante
            name = element.find_element(By.CSS_SELECTOR, 'div.qBF1Pd.fontHeadlineSmall').text
        except NoSuchElementException:
            name = None

        try:
            # Avaliação geral em estrelas
            stars = element.find_element(By.CSS_SELECTOR, 'span.MW4etd').text  # Captura apenas o número de estrelas
        except NoSuchElementException:
            stars = None

        try:
            # Número de avaliações
            reviews = element.find_element(By.CSS_SELECTOR, 'span.UY7F9').text  # Captura o número de avaliações
            reviews = reviews.replace('.', '').replace(',', '')  # Remove formatações, se necessário
        except NoSuchElementException:
            reviews = None

        try:
            # Média de preços
            price = element.find_element(By.CSS_SELECTOR, 'div.W4Efsd').text
        except NoSuchElementException:
            price = None

        # Adiciona os dados capturados à lista
        data_list.append([href, name, stars, reviews, price])

    return data_list


def scroll_to_load(driver, container_xpath, scroll_times=50, scroll_pause=1):

    print("Iniciando o scroll para carregar mais conteúdo...")
    try:
        container = driver.find_element(By.XPATH, container_xpath)  # Localiza o container pelo XPath
        for i in range(scroll_times):
            driver.execute_script("arguments[0].scrollBy(0, 1000);", container)
            time.sleep(scroll_pause)  # Aguarda para que o conteúdo seja carregado
            print(f"Scroll {i + 1}/{scroll_times} concluído.")
    except Exception as e:
        print(f"Erro ao realizar o scroll: {e}")




# Função para salvar os dados em CSV
def save_to_csv(data, cidade):
    print("Salvando dados no CSV...")
    cols = ["Link", "Nome", "Avaliação (Estrelas)", "Número de Avaliações", "Preço Médio"]
    df = pd.DataFrame(data, columns=cols)
    filename = f'restaurantes_{cidade}.csv'
    df.to_csv(filename, index=False)
    print(f"Dados salvos em {filename}")

if __name__ == "__main__":
    cidade = "Goiania"  # Variável para alterar a cidade
    url = BASE_URL.format(cidade=cidade)

    print("Iniciando...")

    # Configuração do WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = CHROME_PATH
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navega para a URL
    driver.get(url)
    time.sleep(5)  # Aguarda carregamento da página

    # Realiza o scroll para carregar mais conteúdo
    container_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]'
    scroll_to_load(driver, container_xpath, scroll_times=10, scroll_pause=1)

    # Coleta os dados
    restaurant_data = get_restaurant_data(driver)

    # Salva os dados no CSV
    save_to_csv(restaurant_data, cidade)

    # Finaliza o WebDriver
    driver.quit()
    print("Concluído!")
