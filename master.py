#Author: Xavier Boudreau
import urllib.request
import ast
from bs4 import BeautifulSoup
from betting_event import *

def moneyline_to_decimal(moneyline_odds):
	try:
		moneyline_odds = int(moneyline_odds)
	except ValueError:
		#if moneyline_odds is an empty string there are no odds to convert
		return None
	decimal_odds = moneyline_odds/100
	if moneyline_odds < 0:
		return -1/decimal_odds
	else:
		return decimal_odds

if __name__ == '__main__':	
	#win: class="op-item op-spread border-bottom op-opening" data-op-moneyline = {}
	#d: class="op-item op-spread op-opening" data-op-info='{"fullgame":"&#43;1"}' data-op-moneyline='{"fullgame":"&#43;190"}'
	#l: class="op-item op-draw op-opening" data-op-info='{"fullgame":""}' data-op-total='{"fullgame":""}' data-op-moneyline='{"fullgame":"&#43;270"}'
	bookie_win_class = 'op-item op-spread border-bottom op-{}'
	bookie_loss_class = 'op-item op-spread op-{}'
	bookie_draw_class = 'op-item op-draw op-{}'
	bookie_names = ['opening', 'bovada.lv', 'mybookie', 'intertops', 'betonline', 
		'caesars', '5dimes', 'westgate', 'topbet', 'sportsbetting', 'gtbets', 'betnow',
		'skybook', 'sportbet', 'station', 'mirage', 'wynn']

	url = 'https://www.oddsshark.com/soccer/mls/odds'
	page = urllib.request.urlopen(url)

	soup = BeautifulSoup(page, 'html.parser')

	#to get dates: find all class="op-separator-bar op-left no-group-name"

	teams = soup.find_all("span", class_ = "op-matchup-team-text")
	events_on_page = []
	for i in range(0,len(teams),2):
		date_tag = teams[i].find_previous("div", class_ = "op-separator-bar op-left no-group-name")
		#convert the html string into a dictionary
		date = ast.literal_eval(date_tag["data-op-date"])['full_date']
		events_on_page.append(betting_event(teams[i].text.strip(), teams[i+1].text.strip(), date))

	for bookie_name in bookie_names:
		game_odds_tags = soup.find_all("div", class_ = bookie_win_class.format(bookie_name))
		#add each bookie's odds for each game on the page
		for i in range(len(game_odds_tags)):
			game_win_tag = game_odds_tags[i]
			win_odds = moneyline_to_decimal(ast.literal_eval(game_win_tag["data-op-moneyline"])['fullgame'])
			game_loss_tag = game_win_tag.find_next("div", class_ = bookie_loss_class.format(bookie_name))
			loss_odds = moneyline_to_decimal(ast.literal_eval(game_loss_tag["data-op-moneyline"])['fullgame'])
			game_draw_tag = game_loss_tag.find_next("div", class_ = bookie_draw_class.format(bookie_name))
			draw_odds = moneyline_to_decimal(ast.literal_eval(game_draw_tag["data-op-moneyline"])['fullgame'])
			events_on_page[i].add_bookie(bookie_name, win_odds, loss_odds, draw_odds)
		
	high_differences = []
	for event in events_on_page:
		print(event)
		#print(event.team_1_win_odds)
		#print(event.team_1_lose_odds)
		try:
			high_differences.append(event.find_outliers())
		except ValueError:
			pass
		print(event.get_average_odds('team_1_win'))
	
	print(high_differences)
