from pickle_operations import *

#TODO
#compute average bet value and percent differences (not percent error) for one event bet result
#plot a distribution of percent differences for many bets
#make variable epsilon strategy simulation

class result:
	def __init__(self, result_string, odds_list, avg_odds):
		self.key = result_string
		
		self.odds_list = odds_list
		self.avg_odds = avg_odds

def percent_change(initial, final):
	deviation = final-initial
	return deviation/initial
	
def find_avg_odds(odds_list):
	sum = 0
	for odds in odds_list:
		sum += odds.odds_offered
	return sum/len(odds_list)

def update_percent_from_average(odds_list, avg_odds):
	for odds in odds_list:
		odds.percent_from_avg = percent_change(avg_odds, odds.odds_offered)

def update_percents_list(odds_w_percents, odds_wo_percents):
	avg_odds = find_avg_odds(odds_wo_percents)
			
	update_percent_from_average(odds_wo_percents, avg_odds)
			
	for odds in odds_wo_percents:
		odds_w_percents.append(odds)

def find_distance_arrays(event_data_pickle):
	'''
	find
	winners{game: {result: [avg_odds, odds_list]}}
	'''
	event_data = get_from_pickle(event_data_pickle)
	if event_data == None:
		return None
		
	winning_odds = []
	losing_odds = []
	
	
	for event in event_data:
		for result_string in event_data[event].winning_bets:
			odds_list = list(event_data[event].winning_bets[result_string])
			
			update_percents_list(winning_odds, odds_list)
			
		for result_string in event_data[event].losing_bets:
			odds_list = list(event_data[event].losing_bets[result_string])
			
			update_percents_list(losing_odds, odds_list)
						
	#sort winning and losing odds by percent difference from average
	winning_odds.sort(key = lambda x: x.percent_from_avg, reverse = True)
	losing_odds.sort(key = lambda x: x.percent_from_avg, reverse = True)
	
	return winning_odds, losing_odds

def calculate_profit(winning_odds, losing_odds):
	#returns array of (percent change from average,profit)
	#sorted from high to low by percent change. 
	#For some % change x in the array,
	#its associated profit y will be the profit or loss incurred if we placed bets
	#on all odds with percent change x or greater
	
	#profit = { q if winner, -1 if loser}, where q is the offered odds of the bet
	
	
	if len(winning_odds) < 2 or len(losing_odds) < 2:
		return None
	
	profits = [None for i in range(len(winning_odds))]
	
	#we are calculating the profit up to these indicies - 1
	winner_split = 1
	loser_split = 1
	
	#these indicies are what we will iterate through the odds lists to capture the profit/loss
	curr_winner = 0
	curr_loser = 0
	
	#store the profit to avoid uneccessary re-computing
	profit = 0
	while winner_split <= len(winning_odds):
		#cutoff is the minimum percent change we will allow this round
		cutoff = winning_odds[winner_split-1].percent_from_avg
		
		while loser_split <= len(losing_odds) and losing_odds[loser_split-1].percent_from_avg >= cutoff:
			loser_split += 1
		#the last unit added to loser_split is a mistake
		if loser_split > 0:
			loser_split -= 1
		
		while curr_winner < winner_split:
			profit += winning_odds[curr_winner].odds_offered
			curr_winner += 1
		
		while curr_loser < loser_split:
			#our profit function dictates that a lost bet yields a loss of 1
			profit -= 1
			curr_loser += 1
		
		profits[winner_split-1] = (cutoff, profit)
		
		curr_winner = winner_split
		curr_loser = loser_split
		winner_split += 1
		
		#reset loser_split so we can test the 0 index again next loop
		if loser_split < 1:
			loser_split = 1

	return profits

if __name__ == '__main__':
	event_data_pickle = 'MLS/evaluated_events.pickle'
	winning_odds, losing_odds = find_distance_arrays(event_data_pickle)
	profits = calculate_profit(winning_odds, losing_odds)
	print(profits)
	
	
	
	
	
	
	
	
	
	
	
	
