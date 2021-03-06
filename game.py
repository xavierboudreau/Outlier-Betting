from odds import *

#A game_key is to act as hashable type for game
#note that hash(date1) == hash(date1.toZone('UTC'))
#this will allow the games to go in a dictionary

class game_key:
	def __init__(self, team1, team2, date):
		self.team_1 = team1
		self.team_2 = team2
		self.when = date
		
	def __eq__(self, other):
		return self.team_1 == other.team_1 and self.team_2 == other.team_2 and \
			self.when == other.when
			
	def __hash__(self):
		return hash((self.team_1, self.team_2, self.when))
		
	def __str__(self):
		return '{} vs. {} at {}'.format(self.team_1, self.team_2, self.when.strftime("%H:%M on %m-%d-%Y"))
	
	def try_hash(self):
		return hash((self.team_1, self.team_2, self.when))


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
		self.bets = {}
		self.winning_bets = {}
		self.losing_bets = {}
		
	def __eq__(self, other):
		return self.team_1 == other.team_1 and self.team_2 == other.team_2 and \
			self.when == other.when
			
	def get_game_key(self):
		return game_key(self.team_1, self.team_2, self.when)
		
	def combine_odds(self, other):
		for other_result in other.bets:
			if other_result in self.bets:
				self.bets[other_result].update(other.bets[other_result])
			else:
				self.bets[other_result] = other.bets[other_result]
				
	def update_winning_bets(self):
		if self.result == None:
			#this function cannot be called on games without results
			raise TypeError
		
		for bet_result in self.bets:
			if is_winner(bet_result, self.result):
				self.winning_bets[bet_result] = self.bets[bet_result]
			else:
				self.losing_bets[bet_result] = self.bets[bet_result]
					
	def __str__(self):
		return '{} vs. {} at {}\n\tResult: {}'.format(self.team_1, self.team_2, self.when.strftime("%H:%M on %m-%d-%Y"), self.result)
	
	def update_result(self, result):
		self.result = result
		
	def add_odds(self, new_odds):
		if new_odds.odds_offered != None:
			if new_odds.result in self.bets:
				self.bets[new_odds.result].add(new_odds)
			else:
				self.bets[new_odds.result] = {new_odds}
			
		