def percent_difference(value_1, value_2):
	return (100*abs(value_1-value_2))/(0.5*(value_1+value_2))


#eventually I'll want to move on beyond win draw loss and have generic betting events with
#a description of the offer (e.g. what is necessary to win, odds offered, time)
#these could be associated together with regards to one event 
#(e.g. odds of different scorelines for the same game)
class betting_event:
	def __init__(self, team1, team2, event_date = None):
		self.team_1 = team1
		self.team_2 = team2
		#dict of form {'bookie_1 name': odds, 'bookie_2 name': odds}
		self.team_1_win_odds = {}
		self.team_1_lose_odds = {}
		self.draw_odds = {}
		self.event_date = event_date
		self.odds_representation = None
	def add_bookie(self, bookie_name, team_1_win, team_1_loss, draw):
		if team_1_win != None:
			self.team_1_win_odds[bookie_name] = team_1_win
		if team_1_loss != None:
			self.team_1_lose_odds[bookie_name] = team_1_loss
		if draw != None:
			self.draw_odds[bookie_name] = draw
	def get_average_odds(self, key):
		'''
		key should be one of 'team_1_win', 'team_1_loss', or 'draw'
		'''
		try:
			if key == 'team_1_win':
				return sum(self.team_1_win_odds.values())/len(self.team_1_win_odds.values())
			elif key == 'team_1_loss':
				return sum(self.team_1_lose_odds.values())/len(self.team_1_lose_odds.values())
			elif key == 'draw':
				return sum(self.draw_odds.values())/len(self.draw_odds.values())
		except ZeroDivisionError:
			#if there are no odds available then the average DNE
			return None
	def find_outliers(self):
		#just return win odds for now
		max_win_odds = max(self.team_1_win_odds.values())
		max_loss_odds = max(self.team_1_lose_odds.values())
		max_draw_odds = max(self.draw_odds.values())
		return percent_difference(max_win_odds, self.get_average_odds('team_1_win'))
	def __str__(self):
		return '{} vs. {}. Kickoff: {}'.format(self.team_1, self.team_2, self.event_date)
	def __repr__(self):
		return str(self)