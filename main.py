from topsport import Topsport
from betsafe import Betsafe
from Bet import betasas
from compare import Compare
from notification import NotificationManager
import time

topas = Topsport()
notification_manager = NotificationManager()
safe = Betsafe()
bet_bet = betasas()

def check_sport_arbitrage(sportas):
    sumatchinta = Compare(safe.display_matches(sportas), topas.display_matches(sportas), bet_bet.display_matches(sportas))
    matchai = sumatchinta.find_matched_matches()
    unique_list = []
    for item in matchai:
        if item not in unique_list:
            unique_list.append(item)

    for matchas in unique_list:

        if len(matchas) > 2:
            odds_team_one = [matcha["team_one_odd"] for matcha in matchas if matcha["team_one_odd"] is not None]
            better_odd_team_one = float(max(odds_team_one) if odds_team_one else None)
            odds_team_two = [matcha["team_two_odd"] for matcha in matchas if matcha["team_two_odd"] is not None]
            better_odd_team_two = float(max(odds_team_two) if odds_team_two else None)
        else:
            better_odd_team_one = float(matchas[0]["team_one_odd"]) if matchas[0]["team_one_odd"] is not None and float(
                matchas[0]["team_one_odd"]) > float(matchas[1]["team_one_odd"]) else float(matchas[1]["team_one_odd"])
            better_odd_team_two = float(matchas[0]["team_two_odd"]) if matchas[0]["team_two_odd"] is not None and float(
                matchas[0]["team_two_odd"]) > float(matchas[1]["team_two_odd"]) else float(matchas[1]["team_two_odd"])


        if 1/better_odd_team_one + 1/better_odd_team_two < 1.01:
            if len(matchas) > 2:
                team_one = matchas[0]
                team_two = matchas[1]
                team_three = matchas[2]
                pirma = team_one if float(team_one['team_one_odd']) == better_odd_team_one else team_two
                pirma = team_two if float(team_two['team_one_odd']) == better_odd_team_one else team_three
                antra = team_one if float(team_one['team_two_odd']) == better_odd_team_two else team_two
                antra = team_two if float(team_two['team_two_odd']) == better_odd_team_two else team_three
            else:
                pirma = matchas[0]
                antra = matchas[1]

            message = f'ARBITRAGE! \n{pirma["team_one"]} ({pirma["site"]}) - {antra["team_two"]} ({antra["site"]})\n' \
                      f' odds {better_odd_team_one} - {better_odd_team_two}'
            print(message)
            notification_manager.send_sms(message)
            time.sleep(4)
            print("Match from Site 1:")
            print(matchas[0])
            print("Match from Site 2:")
            print(matchas[1])
            print("Arbitrage!")
            if len(matchas) > 2:
                print("Match from Site 3:")
                print(matchas[2])
            print(1/better_odd_team_one + 1/better_odd_team_two)
            print(f'Better_one: {better_odd_team_one}\nBetter_two: {better_odd_team_two}')


    print(f'Matches: {len(matchai)}')

check_sport_arbitrage('krepsinis')
check_sport_arbitrage('tenisas')
safe.kill_driver()
bet_bet.kill_driver()
