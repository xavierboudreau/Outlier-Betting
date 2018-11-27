from pickle_operations import *
import numpy as np

#TODO
#implement cynical strategy that prefers odds 

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

def find_distance_arrays(event_data):
	'''
	parameters:
	event_data: dictionary of games
	
	returns
	winning_odds: a list of odds objects that were successful
	losing_odds: a list of odds objects that were not successful
	'''
	
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

def calculate_profit_bins(winning_odds, losing_odds, bins):
	'''
	Returns: a list profits such that profits[k] represents the profit or loss incurred
	if all bets with percent change bins[k] or higher were taken
	
	winning_odds: a list of odds objects that were successful
	losing_odds: a list of odds objects that were not successful
	bins: a list of minimum cutoffs for percent change in odd objects
	'''
	#I could increase the speed by reusing previous entries in profits table
	#but I don't have that much data at the moment so its not a concern
	
	if len(winning_odds)==0 or len(losing_odds)==0:
		return None
	
	profits = [None for i in range(len(bins))]
	
	for cutoff_index in range(len(bins)):
		profit = 0
		cutoff = bins[cutoff_index]
		i = 0
		while i < len(winning_odds) and winning_odds[i].percent_from_avg >= cutoff:
			#we gain the offered odds for every correct bet
			profit += winning_odds[i].odds_offered
			i += 1
		i = 0
		while i < len(losing_odds) and losing_odds[i].percent_from_avg >= cutoff:
			#we lose a dollar for every incorrect
			profit -= 1
			i += 1
		
		profits[cutoff_index] = profit
	
	return profits
	
def find_min_max_odds_variation(winning_odds, losing_odds):
	min = float('inf');
	max = -float('inf');
	
	for winner in winning_odds:
		if winner.percent_from_avg < min:
			min = winner.percent_from_avg
		if winner.percent_from_avg > max:
			max = winner.percent_from_avg
	
	for loser in losing_odds:
		if loser.percent_from_avg < min:
			min = loser.percent_from_avg
		if loser.percent_from_avg > max:
			max = loser.percent_from_avg
	
	return min, max

def save_bins_to_csv(csv_path, bins, profits):
	if len(bins) != len(profits):
		print("NUMBER OF BINS & PROFITS ARE UNEQUAL")
		return None
	
	csv = open(csv_path, 'w+')
	csv.write("PERCENT CHANGE,PROFITS\n")
	
	for i in range(len(bins)):
		csv.write("{},{}\n".format(bins[i], profits[i]))
	
	csv.close()

if __name__ == '__main__':
	event_data_pickle = 'MLS/evaluated_events.pickle'
	bins_profits_csv = "MLS_graphs/11_27/11_27.csv"
	#event_data_pickle = 'EPL/evaluated_events.pickle'
	event_data = get_from_pickle(event_data_pickle)
	
	
	winning_odds, losing_odds = find_distance_arrays(event_data)
	print('Number of losing bets: {}'.format(len(losing_odds)))
	print('Number of winning bets: {}'.format(len(winning_odds)))
	net_income = 0
	for bet in winning_odds:
		net_income += bet.odds_offered
	print('Total value of winning bets: {}'.format(net_income))
	
	
	min_diff, max_diff = find_min_max_odds_variation(winning_odds, losing_odds)
	print("Max percent difference in bet set: {}".format(max_diff))
	print("Min percent difference in bet set: {}".format(min_diff))

	#The bins space depends on the high and low percent_from_average in the odds lists
	buckets = 100
	bins = np.linspace(max_diff + 0.01, min_diff - 0.01, buckets)
	
	profits = calculate_profit_bins(winning_odds, losing_odds, bins)
	
	print("Total possible bets: {}".format(len(winning_odds)+len(losing_odds)))
	print("Total games: {}".format(len(event_data)))
	
	save_bins_to_csv(bins_profits_csv, bins, profits)
	
	
	
	