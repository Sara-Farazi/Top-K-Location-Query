__author__="Sara Farazi"
import pdb
import time
import math
import random
from cell import Point, Coordinates, Cell
from newSummary import Summary, Counter
from nltk.corpus import stopwords
from geopy.distance import great_circle


file = "data/1mtweets.txt"
map_cells = {}
map_terms = {}
seen_cells = {}
all_terms = []
rand_test_terms = []

EARTH_CIRCUMFERENCE = 6378137

rand_test_terms = ['ford', 'visiting', 'words', 'child', 'harbor', 'autobahn', 'su', 'janeiro', 'miami', 'iphone', 'lots', 'tennessee', 'mode', 'theme', 'maui', 'agouti', 'alta', 'arbre', 'point', 'galaxy', 'svizzera', 'perhaps', 'skyscrapers', 'photographs.', 'exhibits', 'wyoming', 'tube', 'linz', 'vt', 'lebanon', 'mays', 'shots', 'things', 'crane', 'shelter', 'brunette', 'new', 'concierto', 'nassau', 'ended', 'beale', 'magical', 'session', 'kanagawa', 'festa', 'abu', 'dag', 'bien', 'aperture', 'mayo', 'hackney', 'minute', 'volkswagen', 'shared', 'ex', 'animalia', 'hip', 'sao', 'tedx', 'nc', 'adoption', 'insect', 'mur', 'walls', 'felipe', 'azul', 'goodwood', 'crosswalk', 'arizona', 'sitting', 'surfing', 'viene', 'helping', 'f.', 'soul', 'taiwan', 'ipad', 'could', 'der', 'electric', 'dark', 'underwater', 'australia', 'ne', 'also', 'sent', 'krzesinski', 'fuente', 'meets', 'shower', 'million', 'racing', 'collage', 'diving', 'bolivia', 'jesse', 'providing', 'auditorium', 'kelvin', 'montagna']

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
	with open('data/alpha-test.txt') as f:
		for line in f:
			l = line.replace('\n', '')
			all_terms.append(l)
	# with open('Multi-Term/rare_multi.txt') as f:
	# 	for line in f:
	# 		l = line.replace('\n', '')
	# 		parts = l.split(' ')
	# 		all_terms.append(parts[0])
	# 		all_terms.append(parts[1])
	# with open('Multi-Term/med_multi.txt') as f:
	# 	for line in f:
	# 		l = line.replace('\n', '')
	# 		parts = l.split(' ')
	# 		all_terms.append(parts[0])
	# 		all_terms.append(parts[1])
	# with open('Multi-Term/frequent_multi.txt') as f:
	# 	for line in f:
	# 		l = line.replace('\n', '')
	# 		parts = l.split(' ')
	# 		all_terms.append(parts[0])
	# 		all_terms.append(parts[1])
	# with open('Multi-Term/tooFreq_multi.txt') as f:
	# 	for line in f:
	# 		l = line.replace('\n', '')
	# 		parts = l.split(' ')
	# 		all_terms.append(parts[0])
	# 		all_terms.append(parts[1])


def get_random_test_terms(num):
	count = num
	lines = set([])
	while len(lines) < num:
		lines.add(random.randrange(1, 1641))
	cnt = 0
	with open('Results/random_query_1000_true_events.txt') as f:
		for line in f:
			cnt += 1
			if cnt in lines:
				parts = line.split("\t")
				term = parts[0]
				rand_test_terms.append(term)



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
	# p1 = (x1, y1)
	# p2 = (x2, y2)
	# res = great_circle(p1, p2).kilometers
	lat1 = x1 
	lon1 = y1
	lat2 = x2
	lon2 = y2
	dLat = math.radians(lat2 - lat1)
	dLon = math.radians(lon2 - lon1)
	a = (math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2))
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	d = EARTH_CIRCUMFERENCE * c
	return d
	# return res



def stream_terms(k):
	tot_time = 0
	with open(file) as f:
		lines = f.read().splitlines()
		for line in lines:
			# start_time = time.time()
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
					# print(item)
					if item in map_terms.keys():
						map_terms[item].update_summary(cell_id)
						# map_terms[item].seen_cells.add(cell_id)
					else:
						temp_summary = Summary(k)
						temp_summary.update_summary(cell_id)
						
						map_terms.update({item : temp_summary})
					# map_terms[item].seen_cells.add(cell_id)
					# if item == 'paris':
					# 	map_terms[item].update_replacements()
				# print(item)
		# 	print(time.time() - start_time) 
		# 	tot_time += (time.time() - start_time)
		# print(tot_time/len(lines))



	for key, value in map_terms.items():
		value.counters = sorted(value.counters, key=lambda x: x.count, reverse=True)
		print("{}\t\t{}".format(key, value))


if __name__ == "__main__":
	build_map()
	find_terms()
	# get_random_test_terms(100)
	# pdb.set_trace()
	stream_terms(50)