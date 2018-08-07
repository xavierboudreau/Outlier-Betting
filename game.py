from odds import *

#A game_key is to act as hash-able type for game (e.g. in a dictionary)
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
			TODO check if UNIX time is aware (comparable to datetime)
		result: a str describing the result of the game 
		'''
		self.team_1 = team_1
		self.team_2 = team_2
		self.when = date
		self.result = result
		self.odds_set = set()
		self.winning_bets = []
		self.losing_bets = []
		
	def __eq__(self, other):
		return self.team_1 == other.team_1 and self.team_2 == other.team_2 and \
			self.when == other.when
			
	def get_game_key(self):
		return game_key(self.team_1, self.team_2, self.when)
		
	def combine_odds(self, other):
		for other_odds in other.odds_set:
			if other_odds not in self.odds_set:
				self.odds_set.add(other_odds)
	def update_winning_bets(self):
		if self.result = None:
			raise TypeError
		while odds_set:
			bet = odds_set.pop()
			if bet.is_winner(result):
				self.winning_bets.append(bet)
			else:
				self.losing_bets.append(bet)
					
	def __str__(self):
		return '{} vs. {} at {}\n\tResult: {}'.format(self.team_1, self.team_2, self.when.strftime("%H:%M on %m-%d-%Y"), self.result)
	
	def update_result(self, result):
		self.result = result
		
	def add_odds(self, new_odds):
		if new_odds.odds_offered != None:
			self.odds_set.add(new_odds)