__author__="Sara Farazi"
import re
import sys
import pdb
import math
import json
import math
from cell import Point, Coordinates, Cell
from summary import Summary, Counter

test_terms = {}
# file1 = 'test.txt'

all_terms = ['louvre', 'nosotros', 'florence', 'scots', 'bilbao', 'brussels', 'leipzig', 'trondheim', 'oisterwijk', 'marseille', 
'shanghai', 'longwood', 'naperville', 'bali', 'chiang', 'stockholm', 'boulder', 'garda', 'noordwijkerhout', 'ann', 'elvert', 
'hyde', 'access-public', 'elijah', 'wildsingapore', 'interactive', 'giants', 'heithabyr', 'documentalista.', 'cronista', 'pecados', 
'indianapolis', 'valladolid', 'jersey', 'ascca', 'fototeca', 'd.c.', 'belgica', 'arbor.', 'auckland', 'geneva', 'kyoto', 'albuquerque', 
'linz', 'virtual', 'bristol', 'historia', 'sacramento', 'monterey', 'dresden', 'austin', 'brugge', 'reykjavik', 'brooklyn', 'nashville', 
'vienna', 'praha', 'arkansas', 'kanagawa', 'bmx', 'df', 'ottawa', 'sarthe', 'rotterdam', 'canberra', 'protocol', 'length', 'volviera', 
'viene', 'moscow', 'bronx', 'dublin', 'halifax', 'madridejos.fotos.es', 'queens', 'raftwet', 'focal', 'esperanzas', 'mays', 'rva', 
'osa', 'review', 'jewell', 'copenhagen', 'jakintza', 'crenshaw', 'sao', 'salzburg', 'agouti', 'madridejos', 'monica', 'waikiki', 
'beijing', 'moore', 'whitewater', 'dasyprocta', 'borough', 'dallas', 'oaxaca', 'budapest']

with open('Results/random_query_1000_true_events.txt') as file:
	all_cnt = 0
	for line in file:
		parts = line.split('\t')
		if len(parts) == 1:
			continue
		term = parts[0]
		test_terms[term] = (parts[2], parts[3], parts[1])

terms = {}
with open('c-3-60q.txt') as f:
		 			
	sum_diff_c = 0
	sum_diff_a = 0
	cnt = 0
	wrongs = 0
	for line in f:
		parts = line.split('\t')
	
		term = parts[0]
		if term in test_terms:
			
			if len(parts) == 1 and test_terms[term][0] == 1:
				cnt += 1
			if len(parts) == 1:
				continue


			c = float(parts[2])
			alpha = float(parts[3])
			# if term not in test_terms:
			# 	print(term)
			# 	continue
			ct = float(test_terms[term][0])
			at = float(test_terms[term][1])
			cent = test_terms[term][2]
			cen = parts[1]
			# cenp = cen.split('/')
			# cen = cenp[1] + '/' + cenp[0]
			if cent != cen:
				print('{}\t{}\t{}'.format(term, cent, cen))
				wrongs += 1
				continue

			cnt += 1
			# pdb.set_trace()
			# print('{}\t{}'.format(term, at))
			sum_diff_c += (math.fabs(ct - c)/ct) 
			sum_diff_a += (math.fabs(at - alpha)/at) 
			# print('{}\t{}'.format(ct, (math.fabs(ct - c)/ct) * 100 ))
			terms[term] = [((math.fabs(ct - c)/ct) * 100) ]
		
	# print(cnt)
	# cnt = cnt - wrongs
	# print('average percentage error of c: {}'.format((sum_diff_c/cnt) * 100 ))
	# print('average percentage error of alpha: {}'.format((sum_diff_a/cnt) * 100))
	# print('wrongs: {}'.format(wrongs))

with open('c-4-49q.txt') as f:
	sum_diff_c = 0
	sum_diff_a = 0
	cnt = 0
	wrongs = 0
	for line in f:
		parts = line.split('\t')
		if len(parts) == 1:
			continue
		cnt += 1
		term = parts[0]
		c = float(parts[2])
		alpha = float(parts[3])
		# if term not in test_terms:
		# 	print(term)
		# 	continue
		ct = float(test_terms[term][0])
		at = float(test_terms[term][1])
		cent = test_terms[term][2]
		cen = parts[1]
		if cent != cen:
			# print(term)
			wrongs += 1
			continue
			
		# pdb.set_trace()
		# print('{}\t{}\t{}\t{}'.format(term, at, (math.fabs(ct - c)/ct) * 100, (math.fabs(at - alpha)/at) * 100))
		sum_diff_c += (math.fabs(ct - c)/ct) * 100
		sum_diff_a += (math.fabs(at - alpha)/at) * 100 
		# print('{}\t{}'.format(term, (math.fabs(ct - c)) ))
		if terms.get(term, None):
			terms[term].append((math.fabs(ct - c)/ct) * 100 )



with open('c-5-44q.txt') as f:
	sum_diff_c = 0
	sum_diff_a = 0
	cnt = 0
	wrongs = 0
	for line in f:
		parts = line.split('\t')
		if len(parts) == 1:
			continue
		cnt += 1
		term = parts[0]
		c = float(parts[2])
		alpha = float(parts[3])
		# if term not in test_terms:
		# 	print(term)
		# 	continue
		ct = float(test_terms[term][0])
		at = float(test_terms[term][1])
		cent = test_terms[term][2]
		cen = parts[1]
		if cent != cen:
			# print(term)
			wrongs += 1
			continue
			
		# pdb.set_trace()
		# print('{}\t{}\t{}\t{}'.format(term, at, (math.fabs(ct - c)/ct) * 100, (math.fabs(at - alpha)/at) * 100))
		sum_diff_c += (math.fabs(ct - c)/ct) * 100
		sum_diff_a += (math.fabs(at - alpha)/at) * 100 
		# print('{}\t{}'.format(term, (math.fabs(ct - c)) ))
		if terms.get(term, None):
			terms[term].append((math.fabs(ct - c)/ct) * 100 )
		# terms[term].append(at)


with open('c-6-37q.txt') as f:
	sum_diff_c = 0
	sum_diff_a = 0
	cnt = 0
	wrongs = 0
	for line in f:
		parts = line.split('\t')
		if len(parts) == 1:
			continue
		cnt += 1
		term = parts[0]
		c = float(parts[2])
		alpha = float(parts[3])
		# if term not in test_terms:
		# 	print(term)
		# 	continue
		ct = float(test_terms[term][0])
		at = float(test_terms[term][1])
		cent = test_terms[term][2]
		cen = parts[1]
		if cent != cen:
			# print(term)
			wrongs += 1
			continue
			
		# pdb.set_trace()
		# print('{}\t{}\t{}\t{}'.format(term, at, (math.fabs(ct - c)/ct) * 100, (math.fabs(at - alpha)/at) * 100))
		sum_diff_c += (math.fabs(ct - c)/ct) * 100
		sum_diff_a += (math.fabs(at - alpha)/at) * 100 
		# print('{}\t{}'.format(term, (math.fabs(ct - c)) ))
		if terms.get(term, None):
			terms[term].append((math.fabs(ct - c)/ct) * 100 )
			terms[term].append(at)



tests = []
for item in terms:
	if len(terms[item]) < 5:
		continue
	tests.append((terms[item][0], terms[item][1], terms[item][2], terms[item][3], terms[item][4]))
# print(tests)
tests = sorted(tests, key=lambda x: x[4])
for item in tests:
	print('{}\t{}\t{}\t{}\t{}'.format(item[0], item[1], item[2], item[3], item[4]))
