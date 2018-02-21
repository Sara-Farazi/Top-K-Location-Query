import pdb
import json
import re
import sys
import math
from cell import Point, Coordinates, Cell
# from summary import Summary, Counter
from nltk.corpus import stopwords
from scipy.optimize import minimize_scalar
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
file = '../all-multis-ring-q.txt'

client = MongoClient('localhost', 27017)
db = client.BiggerRings03
saved_rings = db.rings

qterms = []
all_products = {}

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


def find_qterms():
	with open('tooFreq_multi.txt') as f:
		for line in f:
			l = line.replace('\n', '')
			qterms.append(l)



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
	# print(loc1)
	# print(loc2)
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

all_terms = {}

	
def terms_find():
	with open(file) as f:
		lines = f.read().splitlines()
		for line in lines:
			parts = line.split('\t')
			term = parts[0]
			all_terms[term] = parts

def find_events(m):
	if all_terms.get(m, None):
		parts = all_terms[m]		
		center = parts[1]
		focus = float(parts[2])
		alpha = float(parts[3])
		# total = float(parts[4])
		# print('{}\t{}\t{}\t{}'.format(center, focus, alpha, total))
		return (center, focus, alpha)
	else:
		return 0

def find_prob(cell, t):
	d = get_dist(cell, t[0])
	if d == 0:
		return t[1]
	return t[1] * math.pow(d, -1 * t[2])


if __name__ == "__main__":
	build_map()
	find_qterms()
	terms_find()
	for item in qterms:
		terms = item.split(" ")
		if len(terms[0]) == 1 or len(terms[1]) == 1:
			continue
		t1 = find_events(terms[0])
		t2 = find_events(terms[1])
		
		if t1 == 0 or t2 == 0:
			print("not available")
			continue

		p_joint = 0
		joint_cell = 0
		tot = 0
		for cell in map_cells:
			p1 = find_prob(cell, t1)
			p2 = find_prob(cell, t2)
			pj = min(p1, p2)
			if pj > p_joint:
				p_joint = pj
				if pj == p1:
					joint_cell = t1[0]
					# tot = t1[3]
				if pj == p2:
					joint_cell = t2[0]
					# tot = t2[3]

		print('{}\t{}\t{}'.format(item, joint_cell, p_joint))

		# results = get_product_prob(t1[0], t2[0], t1[1], t2[1], t1[2], t2[2])
		# print('{}\t{}\t{}'.format(item, results[0][0], results[0][1]))

		# print('{}\t{}\t{}\t{}'.format(item, results[0][0], results[0][1], results[0][1] * min(t1[3], t2[3])))
		

