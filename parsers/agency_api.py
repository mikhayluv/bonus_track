import json
import pandas as pd
import selenium
import sqlalchemy as sa
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm


class AG:
    def __init__(self):
        CHROME_BIN_LOCATION = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
        CHROME_DRIVER_LOCATION = r'D:\Питон\chromedriver.exe'
        USER_DATA_DIR = r'C:\environments\selenium'
        options = selenium.webdriver.chrome.options.Options()
        service = selenium.webdriver.chrome.service.Service(CHROME_DRIVER_LOCATION)
        options.add_argument(f'user-data-dir={USER_DATA_DIR}')
        options.add_argument('--disable-popup-blocking')
        options.binary_location = CHROME_BIN_LOCATION
        self.driver = selenium.webdriver.Chrome(options=options, service=service)
        self.driver.maximize_window()

    def get_page(self, agency):
        baseurl = fr'https://bus.gov.ru/public/agency/receipts-and-units.json?agency={agency}'
        self.driver.get(baseurl)
        self.driver.execute_script('window.scroll(0,document.body.scrollHeight)')

    def get_info(self, agency):
        self.get_page(agency)
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/pre')))
        soup = (BeautifulSoup(self.driver.find_element(By.XPATH, "/html/body/pre").get_attribute('outerHTML'),
                              "html.parser")).text
        data = json.loads(soup)
        df_tmp = pd.DataFrame(data)
        df_tmp.insert(loc=0, column='agency', value=agency)
        df_tmp.to_csv('agency_api.csv', sep=';', mode='a', index=False, header=False)


if __name__ == '__main__':
    with open('agency_after_inn.txt', 'r', encoding='utf-8') as f:  # файл создается из кода main_bus_gov_public
        agencies = f.readlines()
        print(f'agencies: {agencies}')
    agi = [x.replace('\n', '') for x in agencies]
    
    tmp = AG()
    for i in tqdm(agi):
        tmp.get_info(i)
