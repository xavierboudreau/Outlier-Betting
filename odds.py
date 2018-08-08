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
	def __str__(self):
		return "bookie: {}\t\tresult:{}\t\t odds offered: {}".format(self.bookie, self.result, self.odds_offered)
	def is_winner(self, actual_result):
		#if this bets self.result is consistent with actual_result, return True
		#otherwise return False
		
		#a semantic analysis algorithm would be useful here to generically decide
		#whether a result strings are consistent with each other
		#for now though, I'll just hardcode the comparisons
		
		#parse for team 1 and team 2 with score
		r = actual_result.split("-")
		r[0] = r[0].strip()
		r[1] = r[1].strip()
		name_break_1 = r[0].rfind(" ")
		name_break_2 = r[1].find(" ")
		team_1 = r[0][:name_break_1]
		team_1_score = r[0][name_break_1+1:]
		team_2 = r[1][name_break_2+1:]
		team_2_score = r[1][:name_break_2]
		assert(team_1_score.isdigit() and team_2_score.isdigit())
		
		team_1_score = int(team_1_score)
		team_2_score = int(team_2_score)
		
		#compare scores to get result
		winning_team = None
		if team_1_score > team_2_score:
			winning_team = team_1
		elif team_2_score > team_1_score:
			winning_team = team_2
		
		if winning_team == None:
			return self.result == "draw"
		else:
			#this line is dangerous because "pizza" should be an error rather than
			#a losing bet. Break into two elif and an else case
			return self.result == "{} won".format(winning_team)
			
		
		
if __name__ == '__main__':
	#test
	from datetime import *
	now = datetime.now()
	odds1 = odds('Koceja', 'x won', 1.3, now)
	odds2 = odds('Koceja', 'x won', 1.3000001, now)
	odds3 = odds('Koceja', 'x won', 1.3001001, now)
	s = {odds1, odds2, odds3}
	print(s)