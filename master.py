#TODO:
#Analyze finished games

#Author: Xavier Boudreau
import urllib.request
import ast
import datetime
import pytz
import time
from bs4 import BeautifulSoup
from game import *
from odds import *
from pickle_operations import *

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
			
			
def roundDateTime(dt):
	#rounds a datetime object dt to nearest 10 minutes
	discard = datetime.timedelta(minutes=dt.minute % 10,seconds=dt.second, microseconds=dt.microsecond)
	dt -= discard
	if discard >= datetime.timedelta(minutes=5):
		dt += datetime.timedelta(minutes=10)

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

def update_results_with_soccerway(url, events, events_with_results, naming_standard):
	#sample url: "https://us.soccerway.com/national/united-states/mls/2018/regular-season/r45738/"
	
	#results table tag: <table class="matches ">
	#  <tbody>
	#	row tag: <tr ...>
	#		team 1 tag: <td class = "team team-a "> <a title = "TEAM 1 NAME">
	#		score: <td class = "score-time score">
	#		team 2 tag: <td class = "team team-b "> <a title = "TEAM 2 NAME"> 
	
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
		try:
			unix_timestamp = int(row_tag["data-timestamp"])
			#game_datetime = pytz.utc.localize(datetime.datetime.fromtimestamp(unix_timestamp))
			#for not found games, soccerway has the correct time
			#	Real Salt Lake vs. Chicago Fire was at 22:00 EDT, Oddshark said 4pm
			#	Houston Dynamo vs SKC was at 21:00 EDT, Oddshark said 4pm
			#	Montreal Impact vs. D.C. United was at 19:30, Oddshark said 4pm
			#	Same for 3 other games
			#	It looks like we have a problem with oddsharks times incorrectly becoming 4pm!!!
			game_datetime = datetime.datetime.fromtimestamp(unix_timestamp)
			timezone = time.tzname[time.localtime().tm_isdst]
			NYC = pytz.timezone("America/New_York")
			game_datetime = NYC.localize(game_datetime)
			#Rounded datetimes to nearest 10 minutes, allowing for some error in time reporting
			roundDateTime(game_datetime)
		
			team_a_tag = row_tag.find_next("td", class_ = "team team-a ")
			score_tag = team_a_tag.find_next("td", class_ = "score-time score")
		
			if score_tag == None:
				#we didn't find another completed match so we are done
				break
			team_b_tag = score_tag.find_next("td", class_ = "team team-b ")
		
			try:
				team_1 = naming_standard[team_a_tag.find_next("a")["title"]]
			except KeyError:
				print("{} not found in name standard".format(team_a_tag.find_next("a")["title"]))
			score = score_tag.find_next("a").text.strip()
			try:
				team_2 = naming_standard[team_b_tag.find_next("a")["title"]]
			except KeyError:
				print("{} not found in name standard".format(team_b_tag.find_next("a")["title"]))
			
			print(game_datetime)
			key = game_key(team_1, team_2, game_datetime)
			score_str = "{} {} {}".format(team_1, score, team_2)
			try:
				events[key].result = score_str
				events_with_results[key] = events[key]
				del events[key]
				print("added one result:\n\t{}\n\tResult: {}\tUNIX: {}".format(key, score_str, unix_timestamp))
			except KeyError:
				print("Game not found:\n\t{}\n\tResult: {}\tUNIX: {}".format(key, score_str, unix_timestamp))
		
			row_tag = team_b_tag.find_next("tr")
		except KeyError:
			#print(row_tag)
			row_tag = row_tag.find_next("tr")

def compare_results_to_offered_odds(events):
	#evaluate whether the bets offered for each game are winners or not
	pass

def pull_oddshark(url, naming_standard):
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
		#time_tag = date_tag.find_next("div", class_ = "op-matchup-time op-matchup-text")
		time_tag = team_tags[i].find_previous("div", class_ = "op-matchup-time op-matchup-text")
		
		hour, minute = get_int_time(time_tag.text.strip())
		
		#convert the html string into a dictionary
		date = ast.literal_eval(date_tag["data-op-date"])['full_date']
		day_of_week, month, day_of_month = tuple(date.split())
		month = month_str_to_number[month]
		day_of_month = int(day_of_month)
		year = datetime_valid.year
		if datetime_valid.month > month:
			year += 1
		
		#TODO: adjust the timezone to be dependent on the server's timezone instead
		# of hardcoding New York 
		timezone = time.tzname[time.localtime().tm_isdst]
		NYC = pytz.timezone("America/New_York")
		game_start = datetime.datetime(year, month, day_of_month, hour, minute)
		game_start = NYC.localize(game_start)
		#round game time to nearest 10 minutes, allowing for some error in
		#time reporting
		roundDateTime(game_start)
		
		try:
			team_1 = naming_standard[team_tags[i].text.strip()]
		except KeyError:
			print("{} not found in name standard".format(team_tags[i].text.strip()))
		try:
			team_2 = naming_standard[team_tags[i+1].text.strip()]
		except KeyError:
			print("{} not found in name standard".format(team_tags[i+1].text.strip()))
		
		new_game = game(team_1, team_2, date = game_start)
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
	
	return {(events_on_page[i].get_game_key()):events_on_page[i] for i in range(len(events_on_page))}
	
if __name__ == '__main__':
	events_to_occur_pickle = 'events_to_occur.pickle'
	occured_events_pickle = 'occured_events.pickle'
	MLS_standard_pickle = 'MLS_Standard.pickle'
	oddshark_url = 'https://www.oddsshark.com/soccer/mls/odds'
	soccerway_url = "https://us.soccerway.com/national/united-states/mls/2018/regular-season/r45738/"
	
	#events_to_occur is dictionary containing game objects that don't have a result recorded
	#	we want to occasionally pull odds from the internet to check if they have changed
	events_to_occur = get_from_pickle(events_to_occur_pickle)
	#MLS_Standard is a dictionary to get a standard team name from team name variations
	MLS_Standard = get_from_pickle(MLS_standard_pickle)
	
	new_events = pull_oddshark(oddshark_url, MLS_Standard)
	
	print("ODDS SEEN\n")
	for event in new_events:
		print(new_events[event])
	print("\n")
	
	#compare newly scraped odds to stored odds, adding them to the dataset if they
	#aren't present
	if events_to_occur != None:
		combine_events(events_to_occur, new_events)
	else:
		events_to_occur = new_events
	
	events_with_results = get_from_pickle(occured_events_pickle)
	if events_with_results == None:
		events_with_results = {}
	
	#get the results of games from the internet
	#when a game has a result, add it to events_with results for later
	update_results_with_soccerway(soccerway_url, events_to_occur, events_with_results, MLS_Standard)
	
	print("\nALL EVENTS:\n")
	for event in events_to_occur:
		print(events_to_occur[event])
	for event in events_with_results:
		print(events_with_results[event])
	
	save_to_pickle(events_to_occur, events_to_occur_pickle)
	save_to_pickle(events_with_results, occured_events_pickle)
	
	


