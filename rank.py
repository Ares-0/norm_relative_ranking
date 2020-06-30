# Libraries
import random
import networkx as nx
import itertools
import numpy as np

# TO DO
# 
# More error checking (file io, helper functions)
# General legibility of code
# Streamline some of the graph stuff
#


# globals
EMPTY = 7.777
num_items = 0
items = [] 	# list of name of items to be ranked
ranks = [[]] #2d list of relative ranks	
able = []	# table helping indicate if graph is connected
errors = [[]]	# table of errors for each edge
G = nx.Graph()


# Functions

# Import list from user-specified or default file
def get_list():
	item_list = []
	filename = input("Press 'Enter' for default file.\nOr enter filename of items file: ")
	
	if(len(filename) > 1):
		try:
			print("Importing items from " + filename + ":")
			f = open(filename, "r")
		except FileNotFoundError:
			print("ERROR: File does not exist")
			return []
	else:
		print("Importing items from items.txt:")
		f = open("items.txt", "r")
	
	line = f.readline()
	
	while(len(line) > 0):
		if(line[-1] == '\n'):
			line = line[:-1]
		item_list.append(line)	# append line		
		line = f.readline()		# get next line
		
	f.close()
	print("Done")
	return item_list

# Given two items, ask user for ranking and return result
def rank_pair(items, x, y):
	if x == y:
		return 0
	ix = str(items[x])
	iy = str(items[y])
	print("\nRank " + iy + " compared to " + ix)
	r = EMPTY
	valid = False
	while(not valid):
		try:
			valid = True
			r=float(input(iy + " is ___ ranks higher than " + ix + ": "))
		except ValueError:
			print("Not a number, skipping vote")
			valid = True
	return r

# Check the ranking graph to see if a path exists between all elements
def enough_votes(ranks):
	#able = [False] * num_items	# an array indicating that element n is accessible from the 0th element
	checked = [False] * num_items		# an array indicating if an element was checked or not
	able[0] = True	# element 0 is accessible from itself

	#print("a: " + str(able))
	#print("c: " + str(checked))
	
	# for element in list that (a) is accessible and (b) has not been checked
	# get list of accessible elements
	# add them to able table
	# go back and check list again
	done = False
	while (not done):
		to_check = check_next(able, checked)
		#print("to check: " + str(to_check))
		if(len(to_check) == 0):
			done = True
		else:
			for x in to_check:
				con = get_connections(ranks, x)
				for y in con:
					able[y] = True
				checked[x] = True
				#print("connections to " + str(x) + ": " + str(con))
			#print("a: " + str(able))
			#print("c: " + str(checked))	
	result = True
	for x in able:
		result = result & x
	return result

# Enough Votes helper
# looks for elements that are reachable and haven't been checked for connections
def check_next(able, checked):
	to_check = []
	for i in range(0, num_items):
		if(able[i] == True and checked[i] == False):
			to_check.append(i)
	return to_check

# Enough Votes helper
# takes an element and returns a list of elements it has been ranked against
def get_connections(ranks, element):
	connections = []
	for x in range(0, num_items):
		if not ranks[x][element] == EMPTY:
			connections.append(x)
	return connections

# Prints a 2d array legibly
def print_2d(array):
	print("")
	for x in array:
		for y in x:
			if(y >= 0):
				print(' ', end="")
			print("{:1.3f}".format(y), end = " ")
			#print(y, end=' ')
		print("")
	print("")

# display the error table, first with all raw data, then averaged (very tall)
def print_error_table():
	global errors
	# this first part gets messy quick
	print("\nError table: ", end=' ')
	for x in errors:
		print()
		for y in x:
			print(y)
		print('.')
	print("\nError Averaged:")
	for x in errors:
		for y in x:
			avg = 0
			s = sum(y)
			if(len(y) <= 1):
				avg = s
			else:
				avg = s / len(y)
			print("{:1.3f}".format(avg), end = " ")
		print()
	
# collect votes until enough are present (old)
def collect_votes():
	done = False
	while(not done):
		rank_x = random.randint(0,num_items-1)
		rank_y = random.randint(0,num_items-1)
		
		#print("To test: x: " + str(rank_x+1) + "\ty: " + str(rank_y+1))
		
		# lets save some time
		if(rank_x == rank_y):					# no need to compare to self
			continue
		
		if(rank_x > rank_y):					# no need to rerank things part 2
			rank_x, rank_y = rank_y, rank_x
		
		if(ranks[rank_x][rank_y] != EMPTY):		# no need to rerank things part 1
			continue
		
		#print("Adjusts: x: " + str(rank_x+1) + "\ty: " + str(rank_y+1))
		
		new_rank = rank_pair(items, rank_x, rank_y)
		ranks[rank_x][rank_y] = new_rank
		ranks[rank_y][rank_x] = -1*new_rank
		
		#print_2d(ranks)
		
		done = enough_votes(ranks)
		if done:
			print("ranks completed")
		else:
			print("ranks incomplete")

# collect exactly N votes
def collect_n_votes():
	valid = False
	n = 0
	while(not valid):
		try:
			valid = True
			n=float(input("Rank how many pairs? "))
		except ValueError:
			print("Not a number")
			valid = False
			continue
			
		# this upper bound ACKSHUALLY should be the number of unranked pairs
		unranked = 0
		for x in range(0, num_items):
			for y in range(0, num_items):
				if(ranks[x][y] == EMPTY):
					unranked += 1
		if(unranked == 0):
			print("ranking filled")
			return
		if(n < 0 or n > unranked/2):
			print("Out of bounds")
			valid = False
			continue
	if(n==0):
		return
	count = n
	#for i in range(0,int(n)):
	while(n > 0):
		rank_x = random.randint(0,num_items-1)
		rank_y = random.randint(0,num_items-1)
		
		#print("To test: x: " + str(rank_x+1) + "\ty: " + str(rank_y+1))
		
		# lets save some time
		if(rank_x == rank_y):					# no need to compare to self
			continue
		
		if(rank_x > rank_y):					# no need to rerank things part 2
			rank_x, rank_y = rank_y, rank_x
		
		if(ranks[rank_x][rank_y] != EMPTY):		# no need to rerank things part 1
			continue
		
		#print("Adjusts: x: " + str(rank_x+1) + "\ty: " + str(rank_y+1))
		
		new_rank = rank_pair(items, rank_x, rank_y)
		ranks[rank_x][rank_y] = new_rank
		ranks[rank_y][rank_x] = -1*new_rank
		n -= 1

# Move given array into a graph structure
def array_to_graph(ranks):
	g = nx.Graph()
	g.add_nodes_from(items)
	for x in range(0, num_items):
		for y in range(0, num_items):
			if(x > y):
				continue
			c = ranks[x][y]
			if(not c == EMPTY):
				g.add_edge(x, y, cost = c)
				#print("x: " + str(x) + "    y: " + str(y) + "   c: " + str(c))
	return g

# print all paths and path costs
def print_path_costs():
	for x in range(0, num_items):
		for y in range(0, num_items):
			# dont double up on stuff
			if(x > y):
				continue
			# get all simple paths between x and y
			a = nx.all_simple_paths(G, x, y)
			
			# for every path
			for path in a:
				print(path, end=' ')
				pairs = [path[i: i + 2] for i in range(len(path)-1)]
				c = 0
				# for every pair, get the cost and add to total
				for p in pairs:
					if(p == None):
						continue
					a = G.get_edge_data(p[0], p[1])
					c0 = a.get("cost")
					if (p[0] < p[1]):
						c += c0
					else:
						c -= c0
				print(c)
			print()

# export table of ranks to csv file
def export_rank_table():
	filename = input("Press 'Enter' for default file.\nOr enter filename of ranks file: ")
	if(len(filename) < 1):
		filename = "rank_out.txt"
	print("Writing to " + filename + ":")
	fout = open(filename, "w")
	for x in ranks:
		line_out = ""
		for y in x:
			if(y >= 0):
				line_out += " "
			line_out += "{:1.3f}".format(y)
			line_out += ","
		line_out += "\n"
		fout.write(line_out)
	fout.close()
	
# import table of ranks from csv file
def import_rank_table():
	if(len(items) <= 1):
		print("Error, item list not initialized")
		return
	
	filename = input("Press 'Enter' for default file.\nOr enter filename of ranks file: ")
	if(len(filename) > 1):
		try:
			print("Importing items from " + filename + ":")
			fin = open(filename, "r")
		except FileNotFoundError:
			print("ERROR: File does not exist")
			return
	else:
		print("Importing items from rank_out.txt:")
		fin = open("rank_out.txt", "r")
	
	
	#fin = open("rank_out.txt", "r")
	for x in range(0, num_items):
		# clear current
		for y in range(0, num_items):
			ranks[x][y] = EMPTY
		line = fin.readline()
		rank_list = line.split(',')
		rank_list = rank_list[:-1] # lose \n
		y=0
		for i in rank_list:
			ranks[x][y] = float(i)
			y += 1
	fin.close()

# Find the error of all the paths and fill the error table with them
def fill_error_table():
	# first put stuff into a graph structure because it can do neat and cool things
	global G
	G = array_to_graph(ranks)
	global errors
	errors	= [[[] for x in range(num_items)] for y in range(num_items)]
	for x in range(0, num_items):
		for y in range(0, num_items):
			# for every pair of nodes, find paths between
			
			# dont double up on stuff
			if(x >= y):
				continue
			
			# get all simple paths between x and y
			#a = nx.all_simple_paths(G, x, y)
			a = nx.edge_disjoint_paths(G, x, y)		# edge disjoint paths do not share any edges
			a2 = []
			
			#print("Paths: ")
			# for every path, find the cost to traverse
			cost_array = []
			for path in a:
				a2.append(path)
				#print(path, end=' ')
				# extract pairs from path
				pairs = [path[i: i + 2] for i in range(len(path)-1)]
				
				# for every pair, get the cost and add to total
				c = 0
				for p in pairs:
					if(p == None):
						continue
					data = G.get_edge_data(p[0], p[1])
					c0 = data.get("cost")
					#c += c0
					if (p[0] < p[1]):
						c += c0
					else:
						c -= c0
				#print(c)
				cost_array.append(c)
				
			# now I have an array of costs for the paths
			if(len(cost_array) < 2):	# paths of 1 we don't care about
				continue
			#print("Cost array: " + str(cost_array))
			
			avg = sum(cost_array) / len(cost_array) # average cost of all paths
			#print("Avg: " + str(avg))
			#print()
			
			# for each path, find the error from average and distribute among edges
			i = 0
			for path in a2:
				#print("Path: ", end=' ')
				#print(path, end=' ')
				
				# find error of cost from average
				# still have cost_array btw
				err = cost_array[i] - avg
				#print("err: " + str(err))
				
				# apply error to each edge of path
				pairs = [path[i: i + 2] for i in range(len(path)-1)]
				weights = [0]*len(pairs)
				j = 0
				# for every pair, get and save the cost
				for p in pairs:
					if(p == None):
						weights[j] = 0
					c0 = (G.get_edge_data(p[0], p[1])).get("cost")
					weights[j] = abs(c0)	# absolute value of cost is ok # later note: ENCOURAGED even
					j += 1
				#print("Cost array: ", end=' ')
				#print(weights)
				j = 0
				for p in pairs:
					ex, ey = p[0], p[1]
					if(ex > ey):
						ex, ey = ey, ex
					if(weights[j] == 0):
						continue
					# adding error to increase length
					# add to positive
					# subtract from negative
					dE = -1*err*(weights[j] / sum(weights))
					errors[ex][ey].append(dE)
					#print("weighted correction: ", end=' ')
					#print(dE+0)
					j+= 1
				i += 1

# Add the error to the costs and scale the weights to align with 1-10 rating scale
def normalize():
	print("\nnormalization in progress")
	global ranks
	global errors
	
	corrected_ranks = [[0 for x in range(num_items)] for y in range(num_items)]
	for x in range(0, num_items):
		for y in range(0, num_items):
			corrected_ranks[x][y] = ranks[x][y]
	
	# make new array of corrected ranks, or error corrected old ranks 
	for x in range(0, num_items):
		for y in range(0, num_items):
			if(x >= y):
				continue
			if(not corrected_ranks[x][y] == EMPTY):
				avg = sum(errors[x][y])
				num = len(errors[x][y])
				#print("x: " + str(x) + " y: " + str(y) + " avg: " + str(avg) + " num: " + str(num))
				if(num > 1):
					avg = avg / num
				corrected_ranks[x][y] = ranks[x][y] + avg
				corrected_ranks[y][x] = -1*corrected_ranks[x][y]

	F = nx.Graph()
	F = array_to_graph(corrected_ranks)
	
	# make a table of distances between everything
	distances = [[0.0 for x in range(num_items)] for y in range(num_items)]
	for x in range(0, num_items):
		for y in range(0, num_items):
			# for every pair
			if(x >= y):
				continue
			
			#print("(x, y) = " + str(x) + " " + str(y))
			# find the most costly path
			weights = []
			j = 0
			for path in nx.all_simple_paths(F, x, y):
				weights.append(0)
				pairs = [path[i: i + 2] for i in range(len(path)-1)]
				for p in pairs: 
					c0 = (F.get_edge_data(p[0], p[1])).get("cost")
					if (p[0] < p[1]):
						weights[j] += c0
					else:
						weights[j] -= c0
				j += 1
			#print(weights)		# am I sure all these signs check out?
			# I want the value of the weight with the largest magnitude max() doesn't do that
			xs = np.array(weights)
			xs_abs = np.abs(xs)
			max_index = np.argmax(xs_abs)
			distances[x][y] = weights[max_index]
			
			#distances[x][y] = max(weights)

	# ok so I have a table of distances between stuff
	#for x in distances:
	#	print(x)
	
	# lets find max and min
	max_x = 0
	max_y = 0
	for x in range(0, num_items):
		for y in range(0, num_items):
			if(x >= y):
				continue
			if(abs(distances[x][y]) >= abs(distances[max_x][max_y])):
				max_x, max_y = x, y
	#print(max_x)
	#print(max_y)
	# by nature of the search, x shooooould be the min and y shoooould be the max
	
	# the cost between them is the normalization target
	height = distances[max_x][max_y]
	scale = 9 / abs(height)	# 9 being the hardcoded range of scores, 10 - 1
	intercept = 9 - height
	#print(scale)
	
	# conveniently, the distances from the largest node have already been calculated
	unsorted = distances[max_x] 
	names = []
	for x in items:
		names.append(x)
	# scale all weights appropriately
	for i in range(0, num_items):
		unsorted[i] = (unsorted[i] * scale)
		
	#print(unsorted)
	#print(names)
	#print()
	
	z = zip(names, unsorted)
	a = unsorted
	a = sorted(z, key = lambda x:x[1])
	
	#print(a)
	
	final_names = names
	final_scores = unsorted
	for i in range(0, num_items):
		final_names[i] = a[i][0]
		final_scores[i] = a[i][1]
		
	# final shift of values to align with 1 - 10
	intercept = 10 - final_scores[num_items-1]
	for i in range(0, num_items):
		final_scores[i] = final_scores[i] + intercept
	
	#print()
	#print(final_names)
	#print(final_scores)
	# boom that is the linearly normalized scores
	
	print("done")
	#fout = open("final_out.txt", "w")
	
	
	fout = input("Press 'Enter' for default file.\nOr enter filename of output file: ")
	if(len(fout) < 1):
		fout = "final_out.txt"
	print("Writing to " + fout + ":")
	fout = open(fout, "w")
	
	for i in range(0, num_items):
		line_out = ""
		line_out += str(final_names[i])
		line_out += ","
		line_out += str(final_scores[i])	
		line_out += ",\n"
		fout.write(line_out)
	fout.close()
	print()

# Rank (or rerank) a specified pair of items
def single_rank():
	x_in = 0
	y_in = 0
	
	i = 0
	for x in items:
		print(str(i) + ": " + x)
		i += 1
	
	valid = False
	while(not valid):
		try:
			valid = True
			x_in=int(input("X index: "))
		except ValueError:
			print("Not a number")
			valid = False
			continue
		if(r < 0 or r > num_items - 1):
			print("Out of bounds")
			valid = False
			continue
	valid = False
	while(not valid):
		try:
			valid = True
			y_in=int(input("Y index: "))
		except ValueError:
			print("Not a number")
			valid = False
			continue
		if(r < 0 or r > num_items - 1):
			print("Out of bounds")
			valid = False
			continue
	new_rank = rank_pair(items, x_in, y_in)
	ranks[x_in][y_in] = new_rank
	ranks[y_in][x_in] = -1*new_rank
	
# print main menu options and query a selection from user
def print_main_menu():
	menu_items = []
	menu_items.append("Import List of Items")
	menu_items.append("Import Table of Ranks")
	menu_items.append("Rank N Pairs")
	menu_items.append("Rank Specific Pair")
	menu_items.append("Normalize Data")
	menu_items.append("Print List of Items")
	menu_items.append("Print Table of Ranks")
	menu_items.append("Export Table of Ranks")
	menu_items.append("Quit")
	#menu_items.append("")
	
	print()
	i = 0
	for x in menu_items:
		i += 1
		print("  " + str(i) + ": " + x)
	print()
	valid = False
	while(not valid):
		try:
			valid = True
			r=float(input("Selection: "))
		except ValueError:
			print("Not a number")
			valid = False
			continue
		if(r < 0 or r > len(menu_items)):
			print("Out of bounds")
			valid = False
			continue
	print()
	return r
	

#
# MAIN
#

quit = False
while(not quit):
	r = print_main_menu()
	
	# IMPORT LIST OF ITEMS TO RANK
	if(r == 1):
		items = get_list()
		num_items = len(items)
		ranks = [[EMPTY for x in range(num_items)] for y in range(num_items)]
		able = [False] * num_items
		continue
	
	# IMPORT TABLE OF RANKS
	if(r == 2):
		import_rank_table()
		continue
	
	# RANK N PAIRS
	if(r == 3):
		collect_n_votes()
		continue
	
	# RANK 1 PAIR
	if(r == 4):
		single_rank()
		continue
	
	# FIND ERRORS AND NORMALIZE DATA
	if(r == 5):
		done = enough_votes(ranks)
		if(not done):
			print("Error: not enough rank data")
			continue
		fill_error_table()
		normalize()
		
	# PRINT LIST OF ITEMS
	if(r == 6):
		if(len(items) <= 1):
			print("Error, items not initialized")
		else:
			for x in items:
				print(x)
		
	# PRINT TABLE OF RANKS
	if(r == 7):
		if(len(ranks) <= 1):
			print("Error, ranks not initialized")
		else:
			print("Ranks: ")
			print_2d(ranks)
			print()
		
	# EXPORT TABLE OF RANKS
	if(r == 8):
		export_rank_table()
	
	# QUIT
	if(r == 9):
		quit = True



