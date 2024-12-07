import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import pyautogui as pa
from selenium.common.exceptions import NoSuchElementException
import os


def get_data(driver):
    print('get data...')
    
    more_elements = driver.find_elements(By.CLASS_NAME, 'w8nwRe')
    for element in more_elements:
        element.click()
    
    elements = driver.find_elements(By.CLASS_NAME, 'jftiEf')
    lst_data = []
    
    for data in elements:
        #name = data.find_element(By.CSS_SELECTOR, '.d4r55').text
        #date = data.find_element(By.CSS_SELECTOR, '.rsqaWe').text
        #text = data.find_element(By.CSS_SELECTOR, '.wiI7pd').text
        #score = data.find_element(By.CSS_SELECTOR, '.kvMYJc').get_attribute("aria-label")
        try:
            name = data.find_element(By.CSS_SELECTOR, '.d4r55').text
        except NoSuchElementException:
            name = None  # Ou algum valor padrão

        try:
            date = data.find_element(By.CSS_SELECTOR, '.rsqaWe').text
        except NoSuchElementException:
            date = None  # Ou algum valor padrão

        try:
            text = data.find_element(By.CSS_SELECTOR, '.MyEned .wiI7pd').text
        except NoSuchElementException:
            text = None  # Ou algum valor padrão

        try:
            score_element = data.find_element(By.CSS_SELECTOR, '.kvMYJc')
            score = score_element.get_attribute("aria-label")
        except NoSuchElementException:
            score = None  # Ou algum valor padrão

        lst_data.append([name, date, text, score])
    return lst_data

def counter(driver):
    result_text = driver.find_element(By.CLASS_NAME, 'jANrlb').find_element(By.CLASS_NAME, 'fontBodySmall').text
    result_number = int(result_text.split(' ')[0].replace(',', ''))
    return int(result_number / 10) + (result_number % 10 > 0) + 3

def scrolling(counter):
    pa.moveTo(769, 614)
    for x in range(counter*2):
       pa.scroll(-1000) 
       time.sleep(0.5)
    return print('scrolling done')

def write_to_xlsx(data):
    print('write to excel...')
    cols = ["Nome", "Data", "Comentário", 'Avaliação']
    df = pd.DataFrame(data, columns=cols)
    df.to_excel('out.xlsx')

if __name__ == "__main__":
    chrome_path = os.getenv('CHROME_PATH')
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH')

    # Incializar driver selenium
    chrome_options = Options()
    chrome_options.binary_location = chrome_path
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()    

    URL = 'https://www.google.com.br/maps/place/Centro+Sul+Portas+e+Janelas/@-16.6491979,-49.3153822,12z/data=!4m12!1m2!2m1!1scentro+sul+portas+e+janelas!3m8!1s0x935eee742cb52c89:0x13e9c27dedb272f9!8m2!3d-16.6595777!4d-49.1765358!9m1!1b1!15sChtjZW50cm8gc3VsIHBvcnRhcyBlIGphbmVsYXOSAQ1kb29yX3N1cHBsaWVy4AEA!16s%2Fg%2F11cmr56f7c?entry=ttu'

    print('starting...')

    driver.get(URL)
    time.sleep(10)

    counter = counter(driver)
    print(counter)
    scrolling(counter)
    data = get_data(driver)
    driver.close()

    write_to_xlsx(data)
    print('Done!')
