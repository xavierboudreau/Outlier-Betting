from odds import *

class game:
	def __init__(self, team_1, team_2, result = None):
		self.team_1 = team_1
		self.team_2 = team_2
		self.result = result
		self.odds_set = set()
	def update_result(self, result):
		self.result = result
	def add_odds(self, new_odds):
		self.odds_set.add(new_odds)