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

file = 'rare_res.txt'
terms = {}

with open('../real_multis.txt') as f:
	for line in f:
		parts = line.split('\t')
		term = parts[0]
		t = ((len(parts)-2)/3)
		locations = [parts[3*k + 1] for k in range(0, int(t))]
		freqs = [parts[3*k + 2] for k in range(0, int(t))]
		if len(locations) > 10:
			terms[term]= locations[0:10]
		else:
			terms[term] = locations




res = {}

with open(file) as f:
	lines = f.read().splitlines()
	for line in lines:
		parts = line.split('\t\t')
		term = parts[0]
		centers = []
		for p in parts[1:len(parts)-1]:
			pParts = p.split('\t')
			center = pParts[0]
			freq = pParts[1]
			centers.append(center)
			# print('{}\t{}\t{}'.format(term, center, freq))
		if len(centers) > 10:
			res[term]= centers[0:10]
		else:
			res[term] = centers
		# t = ((len(parts)-2)/3)
		# locations = [parts[3*k + 1] for k in range(0, int(t))]
		# freqs = [parts[3*k + 2] for k in range(0, int(t))]
		# if len(locations) > 10:
		# 	res[term]= locations[0:10]
		# else:
		# 	res[term] = locations


accu0 = 0
accu1 = 0
accu2 = 0
accu3 = 0
accu4 = 0
accu5 = 0
accu6 = 0
accu7 = 0
accu8 = 0
accu9 = 0

for item in terms:
	if res.get(item, None):
		if terms[item][0] == res[item][0]:
			accu0 += 1
		if len(terms[item]) > 1 and terms[item][1] == res[item][1]:
			accu1 += 1
		if len(terms[item]) > 2 and terms[item][2] == res[item][2]:
			accu2 += 1
		if len(terms[item]) > 3 and terms[item][3] == res[item][3]:
			accu3 += 1
		if len(terms[item]) > 4 and terms[item][4] == res[item][4]:
			accu4 += 1
		if len(terms[item]) > 5 and terms[item][5] == res[item][5]:
			accu5 += 1
		if len(terms[item]) > 6 and terms[item][6] == res[item][6]:
			accu6 += 1
		if len(terms[item]) > 7 and terms[item][7] == res[item][7]:
			accu7 += 1
		if len(terms[item]) > 8 and terms[item][8] == res[item][8]:
			accu8 += 1
		if len(terms[item]) > 9 and terms[item][9] == res[item][9]:
			accu9 += 1


print(accu0/len(res))
print(accu1/len(res))
print(accu2/len(res))
print(accu3/len(res))
print(accu4/len(res))
print(accu5/len(res))
print(accu6/len(res))
print(accu7/len(res))
print(accu8/len(res))
print(accu9/len(res))