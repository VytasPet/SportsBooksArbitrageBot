import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.support.wait import WebDriverWait
from unidecode import unidecode

CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"

# Set up Selenium WebDriver

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br"
}

class Betsafe:
    def __init__(self):
        self.driver = self.run_driver()


    def display_matches(self, sportas):
        sport_sour = self.go_down(sport_url=f'https://www.betsafe.lt/lt/lazybos/{sportas}')
        sport_matches = self.matches_array(sport_sour, sportas)
        return sport_matches

    def kill_driver(self):
        self.driver.quit()

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


    def go_down(self, sport_url):
        self.driver.get(url=sport_url)
        try:
            cookies_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="gdpr-snackbar-accept"]')))
            cookies_btn.click()
            time.sleep(2)
        except NoSuchElementException:
            pass

        body = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body')))
        # first move to the element
        self.driver.execute_script("return arguments[0].scrollIntoView(true);", body)
        # then scroll by x, y values, in this case 10 pixels up
        self.driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(5)
        modal = self.driver.find_element(By.XPATH, value='//*[@id="main-sportsbook-content"]/div[3]')

        for follower in range(8):
            try:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                time.sleep(5)
            except NoSuchElementException:
                pass



        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        all_leagues = soup.find("section", class_="wpt")
        return all_leagues


    def matches_array(self, sport, sportas):
        matches_with_info = []
        all_matches = []
        tournaments = sport.findAll("div", class_="wpt-tournament__body")
        for match in tournaments:
            matchess = [all_matches.append(match) for match in match.findAll("div", class_="wpt-table__row")]

        for match in all_matches:
            odds = match.findAll("div", class_="wpt-odd")

            if len(odds) >= 2:
                team_one_odd = odds[0].get('data-odd-value')
                team_two_odd = odds[1].get('data-odd-value')
            # print(odds[0].get('data-odd-value'))
            matchess = match.findAll("div", class_="wpt-teams__team")
            if len(matchess) >= 2:
                team = {"team_one": unidecode(matchess[0].find("span").text),
                        "team_two": unidecode(matchess[1].find("span").text),
                        "team_one_odd": team_one_odd,
                        "team_two_odd": team_two_odd,
                        "site": "betsafe"}
                if len(team["team_one"]) < 20:
                    matches_with_info.append(team)
        # print(f'betsafe - {sport} - {matches_with_info}')
        print(f'betsafe - {sportas} - {len(matches_with_info)}')
        return matches_with_info



