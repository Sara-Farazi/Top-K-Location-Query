__author__="Sara Farazi"

# Kleinberg's method for finding the probabilistic model of a term geographical distribution.

import re
import sys
import pdb
import math
import json
import time
import math
import time
from cell import Point, Coordinates, Cell
from summary import Summary, Counter
from nltk.corpus import stopwords
from scipy.optimize import minimize
from geopy.distance import great_circle


# Change this file path for a new dataset:
file = 'base-134.txt'
all_terms = {}
map_cells = {}
test_terms = []


# tests = ['newtown', 'paris', 'fighter', 'march', 'equipment', 'arrows', 'wasser', 'call', 'courant', 'meadow', 'balade', 'kirke', 'showcase', 'piemonte', 'detail', 'cup']

def build_map():
	for i in range(-90, 91):
		for j in range(-180, 181):
			id = i.__str__() + "/" + j.__str__()
			upper_left = Point(i, j)
			upper_right = Point(i + 1, j)
			lower_left = Point(i, j + 1)
			lower_right = Point(i + 1, j + 1) 
			coordinates = Coordinates(upper_right, upper_left, lower_right, lower_left)
			new_cell = Cell(id, coordinates)
			map_cells.update({id : new_cell})



# get distance between 2 points on the map (eucledian and great circle)
def get_dist(loc1, loc2):
	parts1 = loc1.split('/')
	parts2 = loc2.split('/')
	x1 = float(parts1[0]) + 0.5
	x2 = float(parts2[0]) + 0.5
	y1 = float(parts1[1]) + 0.5
	y2 = float(parts2[1]) + 0.5
	p1 = (x1, y1)
	p2 = (x2, y2)
	# res = great_circle(p1, p2).kilometers
	d1 = math.pow((x1 - x2),2)
	d2 = math.pow((y1 - y2),2)
	d = math.sqrt(d1 + d2)
	return d


# Calculates C and alpha for terms (events)
def find_events():

	# with open('random_set_events_2.txt') as file1:
	# 	lines = file1.read().splitlines()
	# 	for line in lines:
	# 		parts = line.split('\t')
	# 		term = parts[0]
	# 		test_terms.append(term)

	with open(file) as f:
		centers = {}
		tot_time = 0
		lines = f.read().splitlines()
		for line in lines:
			parts = line.split('\t')
			term = parts[0]
			# if term in test_terms:
			t = ((len(parts)-2)/3)
			locations = [parts[3*k + 1] for k in range(0, int(t))]
			freqs = [parts[3*k + 2] for k in range(0, int(t))]			

			for loc, freq in zip(locations, freqs):

				if term == '':
					continue
				if all_terms.get(term, None):
					if all_terms[term].get(loc, None):
						all_terms[term][loc] += int(freq)
					else:
						all_terms[term].update({loc: int(freq)})
				else:
					all_terms.update({term: {loc: int(freq)}})

		for key, value in all_terms.items():
			centers[key] = []
			max_count = 0
			loc = ""
			count_sum = 0
			for k, val in value.items():
				# print(val)
				centers[key].append(k)
				count_sum += val
				if val > max_count:
					max_count = val
					loc = k
			value.update({'center': (loc, max_count/count_sum)})
			value.update({'sum': count_sum})


		for key, value in all_terms.items():


			def f(params):
				c,x = params
				# distances1 = {}
				# distances2 = {}
				result = 0		
				for k, val in value.items():
					if k == 'center' or k == 'sum':
						continue
					dist = get_dist(value['center'][0], k)
					if dist == 0:
						dist = 1

					result = result + (val * math.log(c * ( dist **(-x))) )
				
				used_locations = [k for k, val in value.items()]

				for k in map_cells:
					if k not in used_locations:
						dist = get_dist(value['center'][0], k)
						if dist == 0:
							continue
						
						result = result + math.log(1 - (c * (dist**(-x))))
				
				# print(result)
				return (-1) * result
			start_time = time.time()
			initial = [0.001, 0.01]
			res = minimize(f, initial, bounds = [(0.001, 0.999), (0.01,5)])
			# print("Done optimization")
			
			alpha = res.x[1]
			C = res.x[0]
			# value.update({'alpha': alpha})
			# answers[item] = (C, alpha)
			print('{}\t{}\t{}\t{}'. format(key, value['center'][0], C, alpha))

		
			tot_time += (time.time() - start_time)
			print((time.time() - start_time))
		print(tot_time/len(all_terms))



if __name__ == "__main__":
	build_map()
	find_events()







