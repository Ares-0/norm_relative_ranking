Normalized Relative Ranking

About
	Have you ever wanted to rate a bunch of things on a scale from 1 to 10 not in isolation but instead comparatively ranked against each other and the more relative ranks you have the better because the error in your subjective ranking will get averaged out? Same.
	
	This program takes a list of any number of items and prompts the user to rank the items against each other. When enough ranks have been gathered, the program will find the error in the rankings and attempt to average it out. Then the scores will be rescaled to match a 1-10 system.
	
	For instance, say a user ranks;
		A 1 rank less than B and 
		B 1 rank less than C and 
		A 3 ranks less than C.
		
	After averaging, 
		A will be about 1.2 ranks less than B, 
		B will be about 1.2 ranks less than C, and 
		A will be about 2.6 ranks less than C. 
	
	The final ranking will be:
		A: 1.0
		B: 5.8
		C: 10


Important Files
	rank.py
	The main file. Run this file to execute the program. A menu in the command line will prompt further progression.

	items.txt
	The default input file for items to be ranked. Other input files can be specified at runtime as well.
	Item files expect to be formatted such that there is exactly one item per line.
	
	final_out.txt
	The default output file for the final rankings. Other output files can be specified at runtime as well. Will be created or overwritten when the time comes. This file will be formatted as a CSV with each line containing exactly one item name and that items final ranking.

		
Libraries Used
	random
	networkx
	itertools
	numpy


Runtime
	When running the program, the user will be prompted with the following menu options. Here is a quick description of what each option does.
  
	1: Import List of Items
	Import list of items to be ranked from a file, either "items.txt" by default, or another user-specified file.
	(REQUIRED)
	
	2: Import Table of Ranks
	Import a csv formatted 2D table of already entered rankings between items, to help load progress from a previous session.
	(Optional)
	
	3: Rank N Pairs
	Rank random pairs of items relatively. N is specified by the user. User will be asked something like "A is __ ranks higher than B: " and will be expected to respond (but not strictly) with a number between -10 and 10 indicating the difference in rank between the two items. Negative values are therefore valid.
	(REQUIRED, unless you want to do all your ranks through option 4)
	
	4: Rank Specific Pair
	User will enter the indices of a particular pair they want to rank, then will be prompted to rank that pair. Helpful for correcting an incorrect entry or making sure a certain pair is ranked without relying on rng.
	(Optional, unless you want to do all your ranks through here)
	
	5: Normalize Data
	6: Print List of Items
	Prints a list of the current items to be ranked.
	(REQUIRED)
	
	7: Print Table of Ranks
	Prints the table of ranks as they currently stand. "7.777" is a hardcoded value indicating null or empty.
	(Optional)
	
	8: Export Table of Ranks
	Export the table of ranks to a user-specified or the default file "ranks_out.txt". Formatted as csv. Useful for saving rankings between sessions.
	(Optional)
	
	9: Quit
	Ends the current session.
	(Optional)
