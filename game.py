from odds import *

class game:
	def __init__(self, team_1, team_2, date = None, result = None):
		'''
		Parameters
		team_1: a str of a team in the game
		team_2: a str of the other team in the game (besides team_1)
		date: a datetime object describing the start of the game
		result: a str describing the result of the game 
		'''
		self.team_1 = team_1
		self.team_2 = team_2
		self.when = date
		self.result = result
		self.odds_set = set()
	def __str__(self):
		return '{} vs. {}'.format(self.team_1, self.team_2)
	def update_result(self, result):
		self.result = result
	def add_odds(self, new_odds):
		self.odds_set.add(new_odds)