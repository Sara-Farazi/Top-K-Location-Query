__author__="Sara Farazi"

# Answer and evaluate TFS test queries

import re
import sys
import pdb
import math
import json
import math
from cell import Point, Coordinates, Cell
from summary import Summary, Counter
from geopy.distance import great_circle
from pymongo import MongoClient
from scipy.integrate import quad


test_terms = []
reals = {}
map_cells = {}
client = MongoClient('localhost', 27017)
db = client.BiggerRings04
saved_rings = db.rings

def get_dist(x,y):
	p1 = (x, y)
	p2 = (29, -96)
	d1 = math.pow((42 - x),2)
	d2 = math.pow((-72 - y),2)
	d = math.sqrt(d1 + d2)
	return great_circle(p1, p2).kilometers

def get_dist_euclid(x,y):
	p1 = (x, y)
	p2 = (29, -96)
	d1 = math.pow((42 - x),2)
	d2 = math.pow((-72 - y),2)
	d = math.sqrt(d1 + d2)
	return d

def get_dist2(x1,y1, x2, y2):
	p1 = (x1, y1)
	p2 = (x2, y2)
	d1 = math.pow((x1 - x2),2)
	d2 = math.pow((y1 - y2),2)
	d = math.sqrt(d1 + d2)
	return d
	# return great_circle(p1, p2).kilometers

def get_radius(dist):
	sizes = [100, 102.4, 256.0, 640.0, 1600.0, 4000.0, 10000.0]
	if dist < sizes[0]:
		return sizes[0]
	if dist >= sizes[len(sizes)-1]:
		return sizes[len(sizes)-1]

	for i in range(0, len(sizes) - 1):
		if dist >= sizes[i] and dist < sizes[i+1]:
			return sizes[i]

def integrand(x, c, a):
     return c*x**(-a) 



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


# with open('Results/random_query_1000_true_events.txt') as f:
# 	for line in f:
# 		parts = line.split('\t')
# 		test_terms.append(parts[0])


#42/-74
with open('exact_test.txt') as f1:
	for line in f1:
		parts = line.split('\t')
		term = parts[0]
		tt = parts[len(parts)-1]
		ttt = tt.split(' ')
		total= int(ttt[1])
		# print(len(parts))
		t = int((len(parts) - 2)/3)
		for i in range(1,t):
			loc = parts[i*3 + 1]
			if loc == '42/-72':
				if int(parts[i*3 + 2]) > 5:
					reals[term] = (int(parts[i * 3 + 2]), total)
					break
		# reals[term] = (0, total)



with open('a-6.txt') as f2:
	diff = 0
	diff1 = 0
	diff2 = 0
	diff3 = 0
	diff4 = 0
	al = 0
	all_reals = 0
	cnt = 0
	ave = 0
	difflog = 0

	for line in f2:
		parts = line.split('\t')
		term = parts[0]
		if term in reals:
			center = parts[1]
			pp = center.split('/')
			x = int(pp[0])
			y = int(pp[1])
			c = float(parts[2])
			a = float(parts[3])
			# total = int(parts[4])
			# print('total: {}'.format(total))
			sum_all = 0
			# for item in map_cells:
			# 	pp = item.split('/')
			# 	x1 = int(pp[0])
			# 	y1 = int(pp[1])
			# 	if x1 == x and y1 == y:
			# 		ihcontinue
			# 	p = c * math.pow(get_dist2(x, y, x1, y1), (-1*a))
			# 	# print(p)
			# 	sum_all += p
			# print('******************************')
			# print(sum_all)
			cnt += 1
			d = get_dist(x,y)
			de = get_dist_euclid(x,y)
			if de == 0 or d == 0:
				continue
			#expected = ((c * math.pow(d,(2-a)))/(2-a))
			integral = quad(integrand, 1, 400, args=(c,a))[0]
			# print(integral)
			expected = (c * de**(-a))/abs(integral)
			curs = saved_rings.find({"cell": center})
			if curs.count() == 1:
				saved = curs[0]
			elif curs.count() > 1:
				saved = curs[curs.count()-1]
			ring = get_radius(d)
			# pdb.set_trace()
			r = ring.__str__()
			r = r.replace('.', '/')
			if r == '100/0':
				r = '100'
			tot = float(saved['list'][r])
			
			expected_freq = 0
			
			expected_freq = (expected * reals[term][1]) 
			if expected_freq < 1:
				expected_freq = 1
			else:
				expected_freq = int(expected_freq + 1) 
			# print('term: {}\t real:{}\texpected:{}\ttotal:{}\tring:{}'.format(term, reals[term][0], expected_freq, tot, ring))
			# print("{}\t{}\t{}".format(a, expected_freq, reals[term][0]))
			err = abs(expected_freq - reals[term][0])/(reals[term][0])
			loger = 0
			if expected_freq == 0:
				loger = 0
			else:
				loger = abs(math.log(expected_freq,10)-math.log(reals[term][0],10))
			difflog += loger
			# print('{}\t{}\t{}\t{}'.format( a, ring, reals[term][0], expected_freq))
			err2 = abs(expected_freq - reals[term][0])
			err1 = 0
			if err2 == 0 or reals[term][0] == 1:
				err1 = 0
			else:
				# print(diff2)
				# print(reals[term][0])
				err1 = math.log(err2/(reals[term][0]))
			diff += math.pow(abs(expected_freq - reals[term][0]),2)
			diff1 += err
			diff2 += abs(expected_freq - reals[term][0])
			all_reals += reals[term][0]
			diff3 += err1
			if err > 1:
				diff4 += math.log(err,10)
			else:
				diff += 0
			ave += expected_freq
			print("{}\t{}".format(a, loger))


	print('*****************************')
	print(diff/cnt)
	print("RMSE:{}".format(math.sqrt(diff/cnt)/ave))
	print("AVe Rel: {}".format(diff1/cnt))
	print("Log Err: {}".format(difflog/cnt))
	print(difflog)
	print("******************************")
	print(diff2)
	av = all_reals/cnt
	print(diff2/(cnt*av))
	print(cnt)
	print(all_reals/cnt)

	

	# print(diff2/all_reals)



			

