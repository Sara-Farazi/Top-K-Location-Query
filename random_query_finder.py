import pdb
import json
import re
import sys
import math

from random import randint
from pymongo import MongoClient
from cell import Point, Coordinates, Cell
from scipy.optimize import minimize_scalar
from geopy.distance import great_circle

file = '../all_terms_exact.txt'
ff = '../data/data2.txt'
randoms = []
whole_terms = []

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



# with open(file) as f:
# 	lines = f.read().splitlines()
# 	while True:
# 		index = randint(0, 1468895)	
# 		l = lines[index]
# 		parts = l.split("\t")
# 		freq = int(parts[2])
# 		if freq > 50:
# 			if index not in randoms:
# 				print(l)
# 			randoms.add(index)
# 			if len(randoms) == 10000:
# 				break



# with open(ff) as f:
# 	lines = f.read().splitlines()
# 	for line in lines:
# 		parts = line.split("\t")
# 		text = parts[0].lower()
# 		terms = text.split(" ")
# 		# pdb.set_trace()

# 		for item in stop:
# 			if item in terms:
# 				terms = list(filter((item).__ne__, terms))

# 		for item in terms:
# 			if item == '':
# 				continue
# 			if len(item) <= 2:
# 				continue
# 			whole_terms.append(item)

# # pdb.set_trace()

# size = 1977983
# while True:
# 	index = randint(0, size)	
# 	item = whole_terms[index]
# 	randoms.append(item)
# 	whole_terms.remove(item)
# 	size = size - 1
# 	if len(randoms) == 1000:
# 		break

# for item in randoms:
# 	print(item)

multi_queries = {}
multi_queries['rare'] = []
multi_queries['medium'] = []
multi_queries['frequent'] = []
multi_queries['tooFrequent'] = []

m_file = '../multis.txt'
with open(m_file) as f:
	for line in f:
		parts = line.split('\t')
		mterm = parts[0]
		freq = int(parts[1])
		if freq >= 100 and freq < 500:
			multi_queries['rare'].append(mterm)
			continue
		if freq >= 500 and freq < 5000:
			multi_queries['medium'].append(mterm)
			continue
		if freq >= 5000 and freq < 20000:
			multi_queries['frequent'].append(mterm)
			continue
		if freq >= 20000 and freq < 100000:
			multi_queries['tooFrequent'].append(mterm)
			continue

# pdb.set_trace()

cnt = 0
while True:
	index = randint(1, 1616)
	# print(index)
	print(multi_queries['tooFrequent'][index])
	cnt += 1
	if cnt == 1000:
		break






