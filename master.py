#Author: Xavier Boudreau
import urllib.request
import ast
import datetime
from bs4 import BeautifulSoup
from game import *
from odds import *
import pickle

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
def get_int_time(timestr):
	'''
	returns the hour and minute respresented in timestr as integers
	hour is expected as 1-12 and is returned as 0-23
	
	timestr: str in format 'hr:mm<p>' where p is present if in afternoon
	
	e.g. '7:30p' -> hour = 19, minute = 30
	'''
	afternoon = 'p' in timestr
	timestr_fields = timestr.split(':')
	hour = int(timestr_fields[0])
	minute = int(timestr_fields[1][:2])
	if afternoon:
		hour += 12
	elif hour == 12:
		hour = 0
	return hour, minute

def get_from_pickle(filename):
	try:
		with open(filename, 'rb') as pickle_file:
			return pickle.load(pickle_file)
	except FileNotFoundError:
		return None

def save_to_pickle(events, filename):
	with open(filename, 'wb+') as pickle_file:
		pickle.dump(events, pickle_file)
			

def get_results():
	pass

if __name__ == '__main__':
	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
		'August', 'September', 'October', 'November', 'December']
	#use this for coverting string months into the conventional integer for that month
	#e.g. February = 2
	month_str_to_number = {months[i]: i+1 for i in range(len(months))}
	
	events_to_occur_pickle = 'events_to_occur.pickle'
	occured_events_pickle = 'occured_events.pickle'
	
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
	datetime_valid = datetime.datetime.now(datetime.timezone.utc)

	team_tags = soup.find_all("span", class_ = "op-matchup-team-text")
	events_on_page = []
	#find all of the betting events on this page
	for i in range(0,len(team_tags),2):
		#form a date time object that represents the start of this event
		date_tag = team_tags[i].find_previous("div", class_ = "op-separator-bar op-left no-group-name")
		time_tag = date_tag.find_next("div", class_ = "op-matchup-time op-matchup-text")
		
		hour, minute = get_int_time(time_tag.text.strip())
		
		#convert the html string into a dictionary
		date = ast.literal_eval(date_tag["data-op-date"])['full_date']
		day_of_week, month, day_of_month = tuple(date.split())
		month = month_str_to_number[month]
		day_of_month = int(day_of_month)
		year = datetime_valid.year
		if datetime_valid.month > month:
			year += 1
		game_start = datetime.datetime(year, month, day_of_month, hour, minute)
		
		new_game = game(team_tags[i].text.strip(), team_tags[i+1].text.strip(), date = game_start)
		events_on_page.append(new_game)

	#find all the odds offered for all the betting events on this page
	for bookie_name in bookie_names:
		game_odds_tags = soup.find_all("div", class_ = bookie_win_class.format(bookie_name))
		#add each bookie's odds for each game on the page
		for i in range(len(game_odds_tags)):
			game_win_tag = game_odds_tags[i]
			win_odds = moneyline_to_decimal(ast.literal_eval(game_win_tag["data-op-moneyline"])['fullgame'])
			win_result = '{} won'.format(events_on_page[i].team_1)
			events_on_page[i].add_odds(odds(bookie_name, win_result, win_odds, datetime_valid))
			
			
			game_loss_tag = game_win_tag.find_next("div", class_ = bookie_loss_class.format(bookie_name))
			loss_odds = moneyline_to_decimal(ast.literal_eval(game_loss_tag["data-op-moneyline"])['fullgame'])
			loss_result = '{} won'.format(events_on_page[i].team_2)
			events_on_page[i].add_odds(odds(bookie_name, loss_result, loss_odds, datetime_valid))
			
			
			game_draw_tag = game_loss_tag.find_next("div", class_ = bookie_draw_class.format(bookie_name))
			draw_odds = moneyline_to_decimal(ast.literal_eval(game_draw_tag["data-op-moneyline"])['fullgame'])
			draw_result = 'draw'
			events_on_page[i].add_odds(odds(bookie_name, draw_result, draw_odds, datetime_valid))
	
	#TODO: compare newly crawled odds to stored odds, adding them to the dataset if they
	#aren't present
		
	save_to_pickle(events_on_page, events_to_occur_pickle)