link = "http://www.exteriores.gob.es/Consulados/SAOPAULO/es/ServiciosConsulares/Paginas/Pasaporte-SP.aspx"

import os, time, random, string, requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

while True:
    try: 
        print("Executando")
        chrome_options = webdriver.ChromeOptions()
        service_args = []
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome("./chromedriver", options=chrome_options, service_args=service_args)

        wait = WebDriverWait(driver, 10)

        driver.implicitly_wait(120)
        
        original_window = driver.current_window_handle

        driver.get(link)
        
        driver.find_element_by_xpath("//a[contains(text(),'aquí')]").click()

        wait.until(EC.number_of_windows_to_be(2))

        for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break

        wait.until(EC.title_is("Consulado General de España en São Paulo"))

        driver.implicitly_wait(120)

        driver.find_element_by_xpath("//a[contains(text(),'Cita aquí >>>> Pasaportes')]").click()

        time.sleep(30)
        
        data = driver.find_element_by_id("idDivBktDatetimeSelectedDate").text

        print(data)

        requests.get("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage?chat_id=" + TELEGRAM_CHAT_ID + "&text=" + data)        

        time.sleep(600)
        driver.quit()
        del driver
        del chrome_options
    except Exception as e:
        print(
            str(time.localtime().tm_hour)
            + ":"
            + str(time.localtime().tm_min)
            + ":"
            + str(time.localtime().tm_sec)
        )
        print(e)
        driver.quit()
        del driver
        del chrome_options
