#TODO:
#pull results from web
#when a game has a result add it to a finished_games set (for analyzing returns)
#base all game times in UTC
#	they are currently in Eastern time but UTC would make them consistent with
#	the timezone of the timestamp describing when an odds was valid (datetime_valid)

#Author: Xavier Boudreau
import urllib.request
import ast
import datetime
import time
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

def combine_events(old_events, new_events):
	#O(len(new_events)) where len(new_events) is expected to be small (~ <100)
	for event_str in new_events:
		if event_str in old_events:
			#some of the odds may have been updated since we last checked
			#add these new odds to the game
			old_events[event_str].combine_odds(new_events[event_str])
		else:
			#we haven't seen this game before, add it to the events that will occur
			old_events[event_str] = new_events[event_str]
			

def get_from_pickle(filename):
	try:
		with open(filename, 'rb') as pickle_file:
			return pickle.load(pickle_file)
	except FileNotFoundError:
		return None

def save_to_pickle(events, filename):
	with open(filename, 'wb+') as pickle_file:
		pickle.dump(events, pickle_file)
			

def print_results_from_soccerway(url):
	#sample url: "https://us.soccerway.com/national/united-states/mls/2018/regular-season/r45738/"
	
	#results table tag: <table class="matches ">
	#  <tbody>
	#	row tag: <tr ...>
	#		team 1 tag: <td class = "team team-a "> <a title = "TEAM 1 NAME">
	#		score: <td class = "score-time score">
	#		team 2 tag: <td class = "team team-b "> <a title = "TEAM 2 NAME"> 
	unix_now = time.time()
	
	
	page = urllib.request.urlopen(url)
	
	soup = BeautifulSoup(page, 'html.parser')
		
	table_body = soup.find("table", class_ = "matches ").find_next("tbody")
	
	#keep track of when games were played, update when a row has a timestamp in it
	game_date = None
	
	#current_tag = table_body
	
	
	row_tag = table_body.find_next("tr")
	
	#we'll break out the loop when we fail to find more finished matches
	#we can't use the unix timestamp because we don't have a guarantee of when
	#the page is updated
	while row_tag != None:
		unix_timestamp = int(row_tag["data-timestamp"])
		team_a_tag = row_tag.find_next("td", class_ = "team team-a ")
		score_tag = team_a_tag.find_next("td", class_ = "score-time score")
		
		if score_tag == None:
			#we didn't find another completed match so we are done
			break
		team_b_tag = score_tag.find_next("td", class_ = "team team-b ")
		
		team_1 = team_a_tag.find_next("a")["title"]
		score = score_tag.find_next("a").text.strip()
		team_2 = team_b_tag.find_next("a")["title"]
		
		print("{} {} {}\t\t{}".format(team_1, score, team_2, unix_timestamp))
		
		row_tag = team_b_tag.find_next("tr")

def update_results_with_soccerway(url, events):
	#sample url: "https://us.soccerway.com/national/united-states/mls/2018/regular-season/r45738/"
	
	#results table tag: <table class="matches ">
	#  <tbody>
	#	row tag: <tr ...>
	#		team 1 tag: <td class = "team team-a "> <a title = "TEAM 1 NAME">
	#		score: <td class = "score-time score">
	#		team 2 tag: <td class = "team team-b "> <a title = "TEAM 2 NAME"> 
	unix_now = time.time()
	
	page = urllib.request.urlopen(url)
	
	soup = BeautifulSoup(page, 'html.parser')
		
	table_body = soup.find("table", class_ = "matches ").find_next("tbody")
	
	#keep track of when games were played, update when a row has a timestamp in it
	game_date = None
	
	#current_tag = table_body
	
	
	row_tag = table_body.find_next("tr")
	
	#we'll break out the loop when we fail to find more finished matches
	#we can't use the unix timestamp because we don't have a guarantee of when
	#the page is updated
	while row_tag != None:
		unix_timestamp = int(row_tag["data-timestamp"])
		team_a_tag = row_tag.find_next("td", class_ = "team team-a ")
		score_tag = team_a_tag.find_next("td", class_ = "score-time score")
		
		if score_tag == None:
			#we didn't find another completed match so we are done
			break
		team_b_tag = score_tag.find_next("td", class_ = "team team-b ")
		
		team_1 = team_a_tag.find_next("a")["title"]
		score = score_tag.find_next("a").text.strip()
		team_2 = team_b_tag.find_next("a")["title"]
		
		#currently timestamp will not match as game is in EST and this one is in unix
		#I need to convert the unix timestamp to UTC or the EST to UNIX (if aware this is preferrable)
		key_str = team_1 + team_2 + unix_timestamp
		score_str = "{} {} {}".format(team_1, score, team_2)
		table[key_str].result = score_str
		
		row_tag = team_b_tag.find_next("tr")
		
		
	
def finish_games(events, results):
	#update events with results
	#move the events that have results into a new set
	pass

def pull_oddshark(url):
	'''
	gets the betting offers listed at an oddshark webpage
	'''
	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
		'August', 'September', 'October', 'November', 'December']
	#use this for coverting string months into the conventional integer for that month
	#e.g. February = 2
	month_str_to_number = {months[i]: i+1 for i in range(len(months))}
	
	#win: class="op-item op-spread border-bottom op-opening" data-op-moneyline = {}
	#d: class="op-item op-spread op-opening" data-op-info='{"fullgame":"&#43;1"}' data-op-moneyline='{"fullgame":"&#43;190"}'
	#l: class="op-item op-draw op-opening" data-op-info='{"fullgame":""}' data-op-total='{"fullgame":""}' data-op-moneyline='{"fullgame":"&#43;270"}'
	bookie_win_class = 'op-item op-spread border-bottom op-{}'
	bookie_loss_class = 'op-item op-spread op-{}'
	bookie_draw_class = 'op-item op-draw op-{}'
	bookie_names = ['opening', 'bovada.lv', 'mybookie', 'intertops', 'betonline', 
		'caesars', '5dimes', 'westgate', 'topbet', 'sportsbetting', 'gtbets', 'betnow',
		'skybook', 'sportbet', 'station', 'mirage', 'wynn']

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
	#infers order of events from events_on_page
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
	
	return {str(events_on_page[i]):events_on_page[i] for i in range(len(events_on_page))}
	
if __name__ == '__main__':
	events_to_occur_pickle = 'events_to_occur.pickle'
	occured_events_pickle = 'occured_events.pickle'
	#events_to_occur is dictionary containing game objects that don't have a result recorded
	#we want to occasionally pull odds from the internet to check if they have changed
	events_to_occur = get_from_pickle(events_to_occur_pickle)
	
	url = 'https://www.oddsshark.com/soccer/mls/odds'
	new_events = pull_oddshark(url)
		
	#compare newly scraped odds to stored odds, adding them to the dataset if they
	#aren't present
	if events_to_occur != None:
		combine_events(events_to_occur, new_events)
	else:
		events_to_occur = new_events
	save_to_pickle(events_to_occur, events_to_occur_pickle)
	




