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

multis = {}
all_terms = []
multi_qr = []
multi_qm = []
multi_qf = []
multi_qt = []

reals = {}

map_cells = {}
all_products ={}


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

def find_prob(cell, t):
	d = get_dist(cell, t[0])
	if d == 0:
		return t[1]
	return t[1] * math.pow(d, -1 * t[2])


def get_product_prob(center1, center2, c1, c2, a1, a2):
	# print('{}...{}...{}...{}...{}...{}'.format(center1, center2, c1, c2, a1, a2))
	for key, value in map_cells.items():
		if key == center1 and key == center2:
			joint_p = c1 * c2
			all_products[key] = joint_p
			continue
		if key == center1:
			p1 = c1
			p2 = c2 * (math.pow(get_dist(center2, key), (-1 * a2)))
			joint_p = p1 * p2
			all_products[key] = joint_p
			continue
		if key == center2:
			p2 = c2
			p1 = c1 * (math.pow(get_dist(center1, key), (-1 * a1)))
			joint_p = p1 * p2
			all_products[key] = joint_p
			continue

		d1 = get_dist(center1, key)
		d2 = get_dist(center2, key)
		p1 = c1 * (math.pow(d1, (-1 * a1)))
		p2 = c2 * (math.pow(d2, (-1 * a2)))
	
		# pdb.set_trace()
		joint_p = p1 * p2
		all_products[key] = joint_p

	# max_p = 0
	# res = ''
	# for key, value in all_products.items():
	# 	if value > max_p:
	# 		max_p = value
	# 		res = key
	temp = sorted(all_products.items(), key=lambda x: x[1], reverse = True)
	# pdb.set_trace()
	return temp[:5]

with open('../New/rare_multi.txt') as f:
	for line in f:
		l = line.replace('\n', '')
		multi_qr.append(l)
		parts = l.split(' ')
		all_terms.append(parts[0])
		all_terms.append(parts[1])
with open('../New/med_multi.txt') as f:
	for line in f:
		l = line.replace('\n', '')
		multi_qm.append(l)
		parts = l.split(' ')
		all_terms.append(parts[0])
		all_terms.append(parts[1])
with open('../New/frequent_multi.txt') as f:
	for line in f:
		l = line.replace('\n', '')
		multi_qf.append(l)
		parts = l.split(' ')
		all_terms.append(parts[0])
		all_terms.append(parts[1])
with open('../New/tooFreq_multi.txt') as f:
	for line in f:
		l = line.replace('\n', '')
		multi_qt.append(l)
		parts = l.split(' ')
		all_terms.append(parts[0])
		all_terms.append(parts[1])


with open('../10multi.txt') as f:
	for line in f:
		parts = line.split("\t")
		term = parts[0]
		multis[term] = []
		for i in range(0, int(len(parts)/3)):
			multis[term].append((parts[i*3 + 1]))

with open('../New/real_multis.txt') as f:
	for line in f:
		parts = line.split("\t")
		term = parts[0]
		reals[term] = (parts[1], parts[2])
		

cnt = 0
allc = 0
for item in multi_qr:
	parts = item.split(" ")
	if len(parts[0]) == 1 or len(parts[1]) == 1:
		continue

	a = multis[parts[0]]
	b = multis[parts[1]]
	# a = sorted(a, key=lambda x: x[1])
	# b = sorted(b, key=lambda x: x[1])
	intersect = [x for x in a if x in b]
	# print(intersect)
	if reals.get(item, None):
		allc += 1
		# ins = [x[0] for x in intersect]
		if len(intersect) != 0:
			if reals[item][0] == intersect[0]:
				# print(reals[item][0]) 
				# print(intersect)
				cnt += 1
				# pdb.set_trace()

print(cnt)
print(allc)
print(cnt/allc)


cnt = 0
allc = 0
for item in multi_qm:
	parts = item.split(" ")
	if len(parts[0]) == 1 or len(parts[1]) == 1:
		continue

	a = multis[parts[0]]
	b = multis[parts[1]]
	# a = sorted(a, key=lambda x: x[1])
	# b = sorted(b, key=lambda x: x[1])
	intersect = [x for x in a if x in b]
	# print(intersect)
	if reals.get(item, None):
		allc += 1
		# ins = [x[0] for x in intersect]
		if len(intersect) != 0:
			if reals[item][0] == intersect[0]:
				# print(reals[item][0]) 
				# print(intersect)
				cnt += 1
				# pdb.set_trace()

print(cnt)
print(allc)
print(cnt/allc)

cnt = 0
allc = 0
for item in multi_qt:
	parts = item.split(" ")
	if len(parts[0]) == 1 or len(parts[1]) == 1:
		continue

	a = multis[parts[0]]
	b = multis[parts[1]]
	# a = sorted(a, key=lambda x: x[1])
	# b = sorted(b, key=lambda x: x[1])
	intersect = [x for x in a if x in b]
	# print(intersect)
	if reals.get(item, None):
		allc += 1
		# ins = [x[0] for x in intersect]
		if len(intersect) != 0:
			if reals[item][0] == intersect[0]:
				# print(reals[item][0]) 
				# print(intersect)
				cnt += 1
				# pdb.set_trace()

print(cnt)
print(allc)
print(cnt/allc)

cnt = 0
allc = 0
for item in multi_qt:
	parts = item.split(" ")
	if len(parts[0]) == 1 or len(parts[1]) == 1:
		continue

	a = multis[parts[0]]
	b = multis[parts[1]]
	# a = sorted(a, key=lambda x: x[1])
	# b = sorted(b, key=lambda x: x[1])
	intersect = [x for x in a if x in b]
	# print(intersect)
	if reals.get(item, None):
		allc += 1
		# ins = [x[0] for x in intersect]
		if len(intersect) != 0:
			if reals[item][0] == intersect[0]:
				# print(reals[item][0]) 
				# print(intersect)
				cnt += 1
				# pdb.set_trace()

print(cnt)
print(allc)
print(cnt/allc)


fcs = {}

# with open('../all_multis_fc.txt') as f:
# 	for line in f:
# 		l = line.split('\t')
# 		if len(l) < 4:
# 			continue
# 		term = l[0]
# 		fcs[term] = (l[1], float(l[2]), float(l[3]), int(l[4]))


# for item in multi_qt:
# 	p = item.split(" ")
# 	p1 = p[0]
# 	p2 = p[1]
# 	if fcs.get(p1, None) and fcs.get(p2, None):
# 		results = get_product_prob(fcs[p1][0], fcs[p2][0], fcs[p1][1], fcs[p2][1], fcs[p1][2], fcs[p2][2])
# 		print('{}\t{}\t{}\t{}'.format(item, results[0][0], results[0][1], results[0][1] * min(fcs[p1][3], fcs[p2][3])))


# p_joint = 0
# joint_cell = 0
# tot = 0

# for item in multi_qf:
# 	p = item.split(" ")
# 	pp1 = p[0]
# 	pp2 = p[1]
# 	if fcs.get(pp1, None) and fcs.get(pp2, None):
# 		for cell in map_cells:
# 			t1 = fcs[pp1]
# 			t2 = fcs[pp2]
# 			p1 = find_prob(cell, t1)
# 			p2 = find_prob(cell, t2)
# 			pj = min(p1, p2)
# 			if pj > p_joint:
# 				p_joint = pj
# 				if pj == p1:
# 					joint_cell = t1[0]
# 					tot = t1[3]
# 				if pj == p2:
# 					joint_cell = t2[0]
# 					tot = t2[3]

# 		print('{}\t{}\t{}\t{}'.format(item, joint_cell, p_joint, tot))

# for item in multi_qt:
# 	for cell in map_cells:
# 		p1 = find_prob(cell, fcs[p1])
# 		p2 = find_prob(cell, fcs[p2])
# 		pj = min(p1, p2)
# 		if pj > p_joint:
# 			p_joint = pj
# 			if pj == p1:
# 				joint_cell = t1[0]
# 				tot = t1[3]
# 			if pj == p2:
# 				joint_cell = t2[0]
# 				tot = t2[3]

# 	print('{}\t{}\t{}\t{}'.format(item, joint_cell, p_joint, tot))