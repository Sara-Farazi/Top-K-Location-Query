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
from scipy.optimize import minimize
from geopy.distance import great_circle
from pymongo import MongoClient

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


# RING_SIZE = 200
map_cells = {}
same_distances = {}
file = 'flickr_ring.txt'

client = MongoClient('localhost', 27017)
db = client.BiggerRings6
saved_rings = db.rings

tests = []
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


def is_in_radius(center, location, radius):
	parts1 = center.split('/')
	parts2 = location.split('/')
	x1 = float(parts1[0]) + 0.5
	x2 = float(parts2[0]) + 0.5
	y1 = float(parts1[1]) + 0.5
	y2 = float(parts2[1]) + 0.5
	p_c = (x1, y1)
	p = (x2, y2)
	dist = great_circle(p_c, p).kilometers
	if dist >= radius and dist < radius + 200:
		return True
	else:
		return False


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
	d1 = math.pow((x1 - x2),2)
	d2 = math.pow((y1 - y2),2)
	d = math.sqrt(d1 + d2)
	# res = great_circle(p1, p2).kilometers
	return d


def find_events():	
	# with open('data/alpha-test.txt') as ff:
	# 	for line in ff:
	# 		l = line.replace('\n', '')
	# 		tests.append(l)

	with open(file) as f:
		tot_time = 0
		lines = f.read().splitlines()
		for line in lines:
			start_time = time.time()
			parts = line.split('\t\t')
			term = parts[0]
			total = 0
			# print(term)

			# print(parts)
			# if term in tests:

			for p in parts[1:len(parts)-1]:
				# print(total)
				pParts = p.split('\t')
				# print(pParts)
				# print(int(pParts[1]))
				total += int(pParts[1])			

			
			if term == '':
				continue
			# if term == 'indianapolis':
			# 	continue
			# answers = {}
			for p in parts[1: 2]:
				pParts = p.split('\t')
				# print (pParts)
				center = pParts[0]
				freq = int(pParts[1])
				error = int(pParts[2])
				rings = {}
				# ind = int(len(pParts)/3)
				for i in range(3,13):
					pp = pParts[i].split(" ")
					rings[float(pp[0])] = float(pp[1])
					# total += float(pp[1])
					# rings[int(pParts[3 * i])] = int(pParts[3*i + 1])
				curs = saved_rings.find({"cell": center})
				if curs.count() == 1:
					saved = curs[0]
				elif curs.count() > 1:
					saved = curs[curs.count()-1]
				else:
					# print(term)
					print('Not Found')
					continue	
				if saved.get('list') == None:
					continue
				else:
					saved = saved["list"]
					# xsum = saved['100/77695999999999'] + saved['167/96159999999998'] + saved['279/936'] + saved['466/56'] + saved['777/6']
					# saved['1296/0'] += xsum
		
				# print(freq)
				# pdb.set_trace()
				focus = freq/total
		
				if focus == 1:
					# print('here')
					continue

				cnt = 0
				for item in rings:
					cnt += rings[item]
				
				# print('total:{}\tfound:{}'.format(total,cnt))


				def f(params):
					c, x = params
					result = 0	
					# pdb.set_trace()	
					# + 100!
					for ring, f in rings.items():
						r = ring.__str__()
						# if r == '5000.0':
						# 	# r = r.replace('.', '/')
						# 	r = '5000'
						# else:
						# 	r = r.replace('.', '/')
						r = r.replace('.', '/')
						if r == '100/0':
							r = '100'
						# print(term)
						saved[r] = saved[r] - f
						# 100, 102.4, 256.0, 640.0, 1600.0, 4000.0, 10000.0
						# pdb.set_trace()
						# di = 0
						# if ring == 10000.0:
						# 	di = 7000
						# if ring == 4000.0:
						# 	di = 2800
						# if ring == 1600:
						# 	di = 1120
						# if ring == 640.0:
						# 	di = 498
						# if ring == 256.0:
						# 	di = 179
						# if ring == 102.4:
						# 	di = 101
						# if ring == 100.0:
						# 	di = 50
						# pdb.set_trace()
						# di = ring
						di = ring/100
						result = result + (f * math.log(c * ( (di) **(-x))))
					result += (freq * math.log(c * ( (1) **(-x))))
						# print(result)
				
					for k, val in saved.items():
						
						if k == '_id' or k == 'cell':
							continue
						if val <= 0:
							continue
						kr = k.replace('/', '.')
						d = 0
						dd = float(kr)
						# pdb.set_trace()
						# if dd == 10000.0:
						# 	d = 7000
						# if dd == 4000.0:
						# 	d = 2800
						# if dd == 1600:
						# 	d = 1120
						# if dd == 640.0:
						# 	d = 498
						# if dd == 256.0:
						# 	d = 179
						# if dd == 102.4:
						# 	d = 101
						# if dd == 100:
						# 	d = 50
						# print(d)
						# if float(kr) > 1000:
						# print('{}\t{}'.format(k, val))
						d = dd/100
						if val > 0:
							result = result + (val * (math.log(1 - (c * ((d **(-x)))))))
						
					# print(result)

					

					return (-1) * result


				# print("--- %s seconds ---" % (time.time() - start_time))
				initial = [0.001, 0.01]
				res = minimize(f, initial, bounds = [(0.001, 0.999), (0.01,5)])
				# print("Done optimization")
				
				alpha = res.x[1]
				C = res.x[0]
				# answers[center] = (C, alpha)
				# value.update({'alpha': alpha})
				# print("{} --- {}".format(term, freq))

				print('{}\t{}\t{}\t{}\t{}\t{}'. format(term, center, C, alpha, total, error))
				tot_time += (time.time() - start_time)
	print(tot_time/len(lines))
		# print(answers)
		# for k, v in answers.items():
		# 	max_val = 0
		# 	center = 0
		# 	result = 0
		# 	p = [v[0], v[1]]
		# 	val = f(p)
		# 	if val > max_val:
		# 		max_val = val
		# 		center = k
		# 		result = answers[k]

		# print('{}\t{}\t{}\t{}'.format(term,center, result[0], result[1]))


if __name__ == "__main__":
	build_map()
	find_events()