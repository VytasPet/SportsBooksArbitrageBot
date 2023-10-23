
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.support.wait import WebDriverWait
from unidecode import unidecode

CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br"
}

class betasas:
    def __init__(self):
        self.driver = self.run_driver()
        self.matches_array = []


    def run_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument(f"executable_path={CHROME_DRIVER_PATH}")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def kill_driver(self):
        self.driver.quit()

    def display_matches(self, sportas):
        self.add_to_matches_list(sportas)
        listas = self.matches_array
        self.matches_array = []
        return listas


    def html_by_time(self, sportas):
        self.driver.get(f'https://7bet.lt/sports/{sportas}')
        # time.sleep(7)
        try:
            cookie = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
            # cookie = self.driver.find_element(By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
            cookie.click()
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        # cookie = self.driver.find_element(By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
        # cookie.click()
        categories = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[title='Kategorijos']")))
        # categories = self.driver.find_elements(By.CSS_SELECTOR, "[title='Kategorijos']")
        if len(categories) > 1:
            categories = categories[-1]
        else:
            categories = categories[0]
        categories.click()
        # time.sleep(9)
        soup_today = None
        try:
            today_matches = WebDriverWait(self.driver, 16).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title='Šiandienos rungtynės']")))
            # today_matches = self.driver.find_element(By.CSS_SELECTOR, "[title='Šiandienos rungtynės']")
            today_matches.click()
            # time.sleep(7)
            # time_list = self.driver.find_element(By.XPATH, value='//*[@id="altenar"]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div/div[2]')
            time_list_tomorrow = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title='Pagal laiką']")))
            # time_list_tomorrow = self.driver.find_element(By.CSS_SELECTOR, "[title='Pagal laiką']")
            time_list_tomorrow.click()
            # time.sleep(10)
            WebDriverWait(self.driver, 13).until(EC.presence_of_element_located((By.CLASS_NAME, '_asb_events-table-row')))
            soup_today = BeautifulSoup(self.driver.page_source, "html.parser")
        except NoSuchElementException:
            pass
        self.driver.get(f'https://7bet.lt/sports/{sportas}')
        # back_to_tennis = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/div/main/div/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div')
        # back_to_tennis.click()
        # time.sleep(7)
        categories = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[title='Kategorijos']")))
        # categories = self.driver.find_elements(By.CSS_SELECTOR, "[title='Kategorijos']")
        if len(categories) > 1:
            categories = categories[-1]
        else:
            categories = categories[0]
        categories.click()
        # time.sleep(7)
        list_tomorrow = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title='Šiandienos rungtynės']")))

        # list_tomorrow = self.driver.find_element(By.CSS_SELECTOR, "[title='Rytojaus rungtynės']")
        list_tomorrow.click()
        # time.sleep(7)
        # tomorrow_matches = self.driver.find_element(By.XPATH, value='//*[@id="altenar"]/div[2]/div[2]/div[2]/div[5]/div/div/div[2]/div[2]')
        # tomorrow_matches.click()
        # time.sleep(5)
        time_list_tomorrow = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[title='Pagal laiką']")))

        # time_list_tomorrow = self.driver.find_element(By.CSS_SELECTOR, "[title='Pagal laiką']")
        time_list_tomorrow.click()
        WebDriverWait(self.driver, 13).until(EC.presence_of_element_located((By.CLASS_NAME, '_asb_events-table-row')))
        soup_tomorrow = BeautifulSoup(self.driver.page_source, "html.parser")
        soup_today_tomorrow = []
        if soup_today:
            soup_today_tomorrow.append(soup_today)
        soup_today_tomorrow.append(soup_tomorrow)

        return soup_today_tomorrow

    def add_to_matches_list(self, sportas):
        soup_list = self.html_by_time(sportas)
        today = soup_list[0]
        if len(soup_list) > 1:
            tomorrow = soup_list[1]
        dieniniai = today.findAll("div", class_='_asb_events-table-row')
        for vardai in dieniniai:
            v_p = vardai.findAll("div", class_='_asb_events-table-row-competitor-name')
            team_one = v_p[0].find("div", class_='asb-text').getText()
            team_two = v_p[1].find("div", class_='asb-text').getText()
            team_one = ' '.join(reversed(team_one.split(', ')))
            team_two = ' '.join(reversed(team_two.split(', ')))
            odds = vardai.findAll("div", class_='_asb_price-block-content-price')
            team_one_odd = odds[0].find("span")
            team_two_odd = odds[1].find("span")
            if team_two and team_one and team_one_odd and team_two_odd:
                team = {"team_one": unidecode(team_one),
                        "team_two": unidecode(team_two),
                        "team_one_odd": team_one_odd.text,
                        "team_two_odd": team_two_odd.text,
                        "site": "7bet"}
                self.matches_array.append(team)
        if len(soup_list) > 1:
            rytojaus = tomorrow.findAll("div", class_='_asb_events-table-row')
            for vardai in rytojaus:
                v_p = vardai.findAll("div", class_='_asb_events-table-row-competitor-name')
                team_one = v_p[0].find("div", class_='asb-text').getText()
                team_two = v_p[1].find("div", class_='asb-text').getText()
                team_one = ' '.join(reversed(team_one.split(', ')))
                team_two = ' '.join(reversed(team_two.split(', ')))
                odds = vardai.findAll("div", class_='_asb_price-block-content-price')
                team_one_odd = odds[0].find("span")
                team_two_odd = odds[1].find("span")
                if team_two and team_one and team_one_odd and team_two_odd:
                    team = {"team_one": unidecode(team_one),
                            "team_two": unidecode(team_two),
                            "team_one_odd": team_one_odd.text,
                            "team_two_odd": team_two_odd.text,
                            "site": "7bet"}
                    self.matches_array.append(team)

        print(f'bet7 - {sportas} - {len(self.matches_array)}')
        # print(f'bet7 - {self.matches_array}')

betasas().display_matches('tenisas')


