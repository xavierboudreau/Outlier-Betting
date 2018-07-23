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
	def __eq__(self, other):
		return self.team_1 == other.team_1 and self.team_2 == other.team_2 and \
			self.when == other.when
	def __hash__(self):
		return hash(str(self))
	def combine_odds(self, other):
		for other_odds in other.odds_set:
			if other_odds not in self.odds:
				self.odds.add(other_odds)
	def __str__(self):
		return self.team_1 + self.team_2 + str(self.when)
	def pretty_str(self):
		return '{} vs. {}'.format(self.team_1, self.team_2)
	def update_result(self, result):
		self.result = result
	def add_odds(self, new_odds):
		if new_odds.odds_offered != None:
			self.odds_set.add(new_odds)