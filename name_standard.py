from pickle_operations import save_to_pickle

def add_possible_names(standard, default, name_variations):
	for name_variation in name_variations:
		standard[name_variation] = default


if __name__ == "__main__":
	MLS_Standard = {}
	#TODO: read in name_variations.csv to update possibility of team names
	
	mls_name_filepath = "name_variations.csv"
	mls_name_file = open(mls_name_filepath, 'r')
	lines = mls_name_file.read().split("\n")
	
	for line in lines:
		team_variations = line.split(",")
		#the standard team name will be the first name in the row
		default = team_variations[0]
		for name_variation in team_variations:
			#ignore empty cells in the csv
			if name_variation != "":
				MLS_Standard[name_variation] = default
				
	#store result in pickle for master to use the table
	save_to_pickle(MLS_Standard, "MLS_Standard.pickle")