import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

# Set up Selenium WebDriver
tennis_url = "https://www.topsport.lt/tenisas"
basketball_url = "https://www.topsport.lt/krepsinis?list_filter%5Bfilter%5D=&list_filter%5B_token%5D=m-GIEoFJuwLXG-XSsashFrIk0TJ6P7cbUYqtUz7fuVA&prelive-sort=date_asc"


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br"
}
response_tennis = requests.get(url=tennis_url, headers=headers)
response_basketball = requests.get(url=basketball_url, headers=headers)

soup_tennis = BeautifulSoup(response_tennis.text, "html.parser")
soup_basket = BeautifulSoup(response_basketball.text, "html.parser")

class Topsport:
    def display_matches(self, sporto_saka):
        if sporto_saka == "krepsinis":
            sportas = basketball_url
        else:
            sportas = f'https://www.topsport.lt/{sporto_saka}'

        sport_response = requests.get(url=sportas, headers=headers)
        sport_soup = BeautifulSoup(sport_response.text, "html.parser")
        sport_info = self.get_sport_info(sport_soup)
        sport_matches_display = self.get_list(sport_info, sporto_saka)
        return sport_matches_display




    def get_sport_info(self, sport):
        all_tablists = sport.find("div", class_="prelive-list")
        all_tablists = all_tablists.findAll("div", {"role": "tablist"})
        # print(all_tablists)
        mamam = []
        for tablist in all_tablists:
            all_matches = tablist.find("div", class_="prelive-list-league-collapse")
            matches_list = [mamam.append(list) for list in all_matches.findAll("div", {"class": "prelive-list-game-item-row"})]
        all_matches = sport.find("div", class_="prelive-list-league-collapse")
        matches_list = [list for list in all_matches.findAll("div", {"class": "prelive-list-game-item-row"})]

        return mamam

    def get_list(self, sport, sporto_saka):
        matches_with_info = []
        for match in sport:
            vardai = match.findAll("div", {"class": "h-select-none"})
            vardai[0] = vardai[0].getText().strip()
            vardai[0] = ' '.join(reversed(vardai[0].split()))
            vardai[1] = vardai[1].getText().strip()
            vardai[1] = ' '.join(reversed(vardai[1].split()))
            if vardai[0][0] == '(':
                # Remove the first 6 characters and update the string
                vardai[0] = vardai[0][6:]
            if vardai[1][0] == '(':
                # Remove the first 6 characters and update the string
                vardai[1] = vardai[1][6:]

            kofai = match.findAll("span", {"class": "prelive-list-league-rate"})
            try:
                team = {"team_one": unidecode(vardai[0]), "team_two": unidecode(vardai[1]), "team_one_odd": kofai[0].getText(), "team_two_odd": kofai[1].getText(), "site": "topsport"}
                if len(team["team_one"]) < 20:
                    matches_with_info.append(team)
            except IndexError:
                pass


        # print(f'topsport - {matches_with_info}')
        print(f'topsport - {sporto_saka} - {len(matches_with_info)}')
        return matches_with_info
