__author__="Sara Farazi"
import re
import sys
import pdb
import math
import json
import math
from cell import Point, Coordinates, Cell
# from summary import Summary, Counter

test_terms = {}



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


with open('all_multis.txt') as f:
	for line in f:
		l = line.split('\t')
		term = l[0]
		center = l[1]
		freq = float(l[2])
		test_terms[term] = (center, freq)

cnt = 0
wrongs = 0
with open('baseline-joint-too.txt') as f:
	for line in f:
		l = line.split('\t')
		if len(l) < 2:
			continue
		term = l[0]
		center = l[1]
		# freq = float(l[3])
		if term in test_terms:
			if center == test_terms[term][0]:
				cnt += 1
				# print((math.fabs(test_terms[term][1] - freq)))
				# print('{}\t{}'.format(freq, test_terms[term][1]))
			else:
				wrongs += 1

print(cnt)
print(wrongs)
print(cnt/(cnt+wrongs))


