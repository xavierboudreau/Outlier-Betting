def str_odds(odds):
	'''
	Takes a decimal odds value and converts to rounded str for comparison purposes
	'''
	#round the odds to four decimal places
	return '{0:.4f}'.format(odds)

class odds:
	def __init__(self, bookie, result, odds_offered, time_offered):
		self.bookie = bookie
		self.result = result
		self.odds_offered = odds_offered
		self.time_offered = time_offered
	def __eq__(self, other):
		return self.bookie == other.bookie and \
			self.result == other.result and \
			str_odds(self.odds_offered) == str_odds(other.odds_offered)
	def __hash__(self):
		return hash((self.bookie, self.result, str_odds(self.odds_offered)))
	def is_winner(self, actual_result):
		#if this bets self.result is consistent with actual_result, return True
		#otherwise return False
		pass
		
if __name__ == '__main__':
	#test
	from datetime import *
	now = datetime.now()
	odds1 = odds('Koceja', 'x won', 1.3, now)
	odds2 = odds('Koceja', 'x won', 1.3000001, now)
	odds3 = odds('Koceja', 'x won', 1.3001001, now)
	s = {odds1, odds2, odds3}
	print(s)