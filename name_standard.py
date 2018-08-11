from pickle_operations import save_to_pickle

def save_standard(name_filepath, standard_name):
	Standard = {}
	
	name_file = open(name_filepath, 'r')
	lines = name_file.read().split("\n")
	
	for line in lines:
		team_variations = line.split(",")
		#the standard team name will be the first name in the row
		default = team_variations[0]
		for name_variation in team_variations:
			#ignore empty cells in the csv
			if name_variation != "":
				Standard[name_variation] = default
	
	#store result in pickle for master to use the table
	save_to_pickle(Standard, "{}.pickle".format(standard_name))
				
if __name__ == "__main__":
	name_filepath = input("Enter csv filepath containing name variations (w/ .csv) (e.g. mls_name_variations.csv): ")
	standard_name = input("Enter name for pickle (w/o .pickle) (e.g. MLS_Standard): ")
	save_standard(name_filepath, standard_name)