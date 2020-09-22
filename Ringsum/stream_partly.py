__author__="Sara Farazi"

import re
import sys
import pdb
import math
import json
import time
import math
from collections import defaultdict
from cell import Point, Coordinates, Cell
from summary import Summary, Counter
from nltk.corpus import stopwords
from scipy.optimize import minimize_scalar
from geopy.distance import great_circle
from pymongo import MongoClient


part = [0.01 ,0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 1]
# part = [0.01, 0.1, 0.3, 0.5, 0.7]
partss = part[::-1]
# partss = [0.2]

# size = 1544472
# size = 458#154518

all_terms = []
map_cells = {}
map_terms = {}
counts = {}
tr = {}

stop = ['d', 'wouldn', 'to', 'those', 'while', 'whom', 'only', 'few', 'after', 'off', 'such', 'an', 'he', 'her', 'be', 'll', 
	'hers', 'than', 'does', 'through', 'their', 'was', 'on', 'some', 'couldn', 'above', 'yours', 'but', 'ma', 'yourselves', 
	'as', 'very', 'haven', 'because', 'just', 'should', 'too', 'myself', 'before', 'shouldn', 'during', 'own', 'from', 'up', 
	'into', 'them', 'same', 'can', 'where', 'at', 'with', 'had', 'they', 'ours', 'down', 'how', 'we', 'further', 'any', 'there', 
	'needn', 'aren', 'this', 'each', 'will', 't', 'didn', 'themselves', 'been', 'are', 'having', 'its', 'once', 'if', 'or', 
	'against', 'who', 'have', 'when', 'isn', 'what', 'hadn', 'under', 'here', 'it', 'i', 'won', 'then', 'his', 'himself', 'a', 
	'about', 'me', 'below', 'wasn', 're', 'am', 'him', 'the', 'no', 'and', 'y', 'mustn', 'o', 'why', 'between', 'not', 'now', 
	'were', 'for', 'm', 'in', 'out', 'these', 'is', 'my', 'shan', 'more', 'has', 'again', 'doesn', 'mightn', 'theirs', 'did', 
	'don', 'over', 'she', 'you', 'so', 'our', 'yourself', 've', 'weren', 'which', 'do', 'that', 'most', 'ourselves', 'until', 
	'your', 'herself', 'doing', 'all', 'of', 'nor', 'by', 'ain', 'being', 'hasn', 'other', 'itself', 's', 'both']


def find_terms():
	with open('Results/random_query_1000_true_events.txt') as f:
		for line in f:
			l = line.split('\t')
			if l[0] == 'sully':
				all_terms.append(l[0])
				tr[l[0]] = (l[2], l[3])
			# if len(all_terms) == 1:
			# 	break


def count_qterms():
	for i in all_terms:
		counts[i] = 0
	with open('data/1mtweets.txt') as f:
		for line in f:
			parts = line.split('\t')
			text = parts[0].lower()
			terms = text.split(" ")
			# pdb.set_trace()

			for item in stop:
				if item in terms:
					terms = list(filter((item).__ne__, terms))

			for item in terms:
				if item == '':
					continue
				if len(item) == 1:
					continue
				for i in all_terms:
					if i == item:
						counts[i] += 1


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


def get_dist(loc1, loc2):
	parts1 = loc1.split('/')
	parts2 = loc2.split('/')
	x1 = float(parts1[0]) + 0.5
	x2 = float(parts2[0]) + 0.5
	y1 = float(parts1[1]) + 0.5
	y2 = float(parts2[1]) + 0.5
	# res = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2 ))
	p1 = (x1, y1)
	p2 = (x2, y2)
	res = great_circle(p1, p2).kilometers
	return res



def stream(k):
	with open('data/1mtweets.txt') as f:
		counter = 0
		for line in f:
			parts = line.split("\t")
			text = parts[0].lower()
			lat = parts[2]
			lon = parts[1] 
			cell_id = math.floor(float(lat)).__str__() + "/" + math.floor(float(lon)).__str__()
			# cell = map_cells[cell_id]
			terms = text.split(" ")
			# pdb.set_trace()

			for item in stop:
				if item in terms:
					terms = list(filter((item).__ne__, terms))

			for item in terms:
				if item == '':
					continue
				if len(item) == 1:
					continue
				if item in all_terms:
					if item in map_terms.keys():
						map_terms[item].update_summary(cell_id)
						# map_terms[item].seen_cells.add(cell_id)
					else:
						temp_summary = Summary(k)
						temp_summary.update_summary(cell_id)
						
						map_terms.update({item : temp_summary})

					all_movements = 0
					all_dist = 0
					cnt1 = 0
					cnt2 = 0
					cnt3 = 0
					rct = 0
					for p in partss:
						if counter >= counts[item] * p:
							print('more than {}'.format(p))
							# for item in map_terms:
							rct = map_terms[item].find_remained_cells()
							# map_terms[item].temp_sum = map_terms[item].counters
							# cnt1 += map_terms[item].cnt
							# all_dist += map_terms[item].find_remained_cells()

							print(rct)
							print(len(map_terms[item].counters))
							# print(item)
							# print(tr[item])
							
							partss.remove(p)
							if len(partss) == 0:
								print(rct/len(map_terms))
								print(item)

							break


						# parts = line.split("\t")
						# text = parts[0].lower()
						# lat = parts[1]
						# lon = parts[2] 
						
						# cell_id = math.floor(float(lat)).__str__() + "/" + math.floor(float(lon)).__str__()
						# # cell = map_cells[cell_id]
						# terms = text.split(" ")
						# # pdb.set_trace()

						# for item in stop:
						# 	if item in terms:
						# 		terms = list(filter((item).__ne__, terms))
						# for item in terms:
						# 	if item == '':
						# 		continue
						# 	if len(item) == 1:
						# 		continue
						# 	if item in all_terms:
						# 		if item in map_terms.keys():
						# 			for c in map_terms[item].counters:
						# 				c.rings.add_to_rings(cell_id)
						# 		else:
						# 			temp_summary = Summary(k)
						# 			temp_summary.update_summary(cell_id)
								
						# 			map_terms.update({item : temp_summary})


						# counter += 1
						# continue
					

					
					
					
							# print(item)
							

					counter += 1


	# for key, value in map_terms.items():
	# 	value.counters = sorted(value.counters, key=lambda x: x.count, reverse=True)
	# 	print("{}\t\t{}".format(key, value))
	print(counter)



if __name__ == "__main__":
	build_map()
	find_terms()
	count_qterms()
	# pdb.set_trace()
	stream(60)