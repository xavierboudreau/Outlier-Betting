def add_possible_names(standard, default, name_variations):
	for name_variation in name_variations:
		standard[name_variation] = default


if __name__ == "__main__":
	MLS_Standard = {}
	#TODO: read in name_variations.csv to update possibility of team names
	#store result in pickle for master to utilize
