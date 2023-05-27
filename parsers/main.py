import re
import selenium
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

class BG:
    def __init__(self):
        CHROME_BIN_LOCATION = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
        CHROME_DRIVER_LOCATION = r'D:\IT progs\bonus_track\chromedriver.exe'
        USER_DATA_DIR = r'C:\environments\selenium'
        options = selenium.webdriver.chrome.options.Options()
        service = selenium.webdriver.chrome.service.Service(CHROME_DRIVER_LOCATION)
        options.add_argument(f'user-data-dir={USER_DATA_DIR}')
        options.add_argument('--disable-popup-blocking')
        options.binary_location = CHROME_BIN_LOCATION
        self.driver = selenium.webdriver.Chrome(options=options, service=service)
        self.driver.maximize_window()

    def close(self):
        self.driver.close()

    def get_page(self, inn):
        baseurl = fr'https://bus.gov.ru/public/register/search.html?pageSize=30&agency={inn}&city=&tofkName=&tofkCode=&authority=&level=&agencyTypesDropDownValue=b_c_a_types&status=&annulment=false'
        self.driver.get(baseurl)
        self.driver.execute_script('window.scroll(0,document.body.scrollHeight)')

    def get_region_name(self, region_test_check):
        comma_counter = 0
        probel_counter = 0
        region = ''
        for i in region_test_check:
            if i == ',':
                comma_counter += 1
                probel_counter = 1
                if comma_counter == 2:
                    break
            if comma_counter == 1:
                if probel_counter == 1:
                    probel_counter += 1
                    continue
                region += i
        return region[1:]

    def get_info(self, inn):
        try:
            self.get_page(inn)

            check = BeautifulSoup(self.driver.find_element(By.XPATH,
                                                           "/html/body/div[3]/div/div[2]/table/tbody/tr/td[2]/div/table/tbody/tr/td[2]/form/div[3]/span").get_attribute(
                'outerHTML'), "html.parser")

            tot = check.find("span").text
            total_found = int(tot.replace('Найдено: ', '').strip())
            if total_found == 0:
                return 0

            region_check = BeautifulSoup(self.driver.find_element(By.XPATH,
                                                                  '/html/body/div[3]/div/div[2]/table/tbody/tr/td[2]/div/table/tbody/tr/td[2]/form/div[4]/table/tbody/tr/td[2]/div[1]/div/span').get_attribute(
                'outerHTML'), "html.parser").find('span').text

            region = self.get_region_name(region_check)  # Значение region куда-то записать

            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                '/html/body/div[3]/div/div[2]/table/tbody/tr/td[2]/div/table/tbody/tr/td[2]/form/div[4]/table/tbody/tr/td[2]/div[1]/a')))
            
            soup = str(BeautifulSoup(self.driver.find_element(By.CSS_SELECTOR,
                                                              "#agency > tbody > tr > td:nth-child(2) > "
                                                              "div.result-element > a").get_attribute(
                'outerHTML'), "html.parser"))
            
            soup_ = BeautifulSoup(self.driver.find_element(By.CSS_SELECTOR,
                                                           "#agency > tbody > tr > td:nth-child(2) > "
                                                           "div.result-element > a").get_attribute(
                'outerHTML'), "html.parser")

            agency_name = soup_.find('a',
                                     {'class': 'result-title'}).text.strip()  # Значение agency_name записать куда-то

            match = re.search(r'agency=(\d+)', soup)

            if match:
                number = match.group(1)
                with open('agency_after_inn.txt',
                          'a', encoding='utf-8') as file:  # создается файл с agency, c которым работает код в agency_api
                    file.write(number + '\n')
                with open('agency_and_inn.txt',
                          'a',
                          encoding='utf-8') as file:  # создается файл для проверки, в котором пишется inn и его agency
                    file.write('agency:' + number + ' inn:' + inn + '\n')
                with open('full_info.txt',
                          'a', encoding='utf-8') as file:  # создается файл для проверки, в котором пишется вся информация
                    file.write(f"{number};{inn[:-1]};{region};{agency_name}" + '\n')

        except:
            with open('agency_and_inn.txt',
                      'a') as file:  # создается файл для проверки, в котором пишется inn и его agency
                file.write('agency:' + 'Ошибка' + ' inn:' + inn + '\n')


with open('full_info.txt', 'a', encoding='utf-8') as file:
    file.write('agency;inn;region;agency_name' + '\n')
with open('inn.txt', 'r', encoding='utf-8') as f: # c этого файла достаем все inn, при помощи них будем искать всю информацию, которую запишем в full_info
    inns = f.readlines()
inns = [x.replace('\n', ' ') for x in inns]

tmp = BG()
for i in tqdm(inns):
    tmp.get_info(i)
