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

# 		parts = line.split('\t\t')
# 		term = parts[0]
# 		test_terms[term] = []
# 		# print(parts)
# 		if len(parts) > 7:
# 			for i in range(1,len(parts)-1):
# 				pParts = parts[i].split('\t')
# 				# print(p)
# 				# print(pParts)
# 				# print(int(pParts[1]))
# 				loc = pParts[0]
# 				f = pParts[1]
# 				er = pParts[2]
# 				test_terms[term].append((loc, f))
				
# 			all_cnt += 1
# 		# print(test_terms[term])

terms = {}
with open('ring50q.txt') as f:
# 	acc = 0
# 	cnt = 0
# 	for line in f:
# 		parts = line.split('\t\t')
# 		term = parts[0]
# 		if len(parts) > 7:
# 			pParts = parts[5].split('\t')
# 			# print(pParts)
# 			# print(int(pParts[1]))
# 			loc = pParts[0]
# 			f = pParts[1]
# 			er = pParts[2]
			
# 			if loc == test_terms[term][0][0] or loc == test_terms[term][1][0] or loc == test_terms[term][2][0] or loc == test_terms[term][3][0] or loc == test_terms[term][4][0]:
# 				cnt += 1
# 			elif (test_terms[term][5][1] == test_terms[term][5][1] and loc == test_terms[term][5][0]) or (test_terms[term][5][1] == test_terms[term][6][1] and loc == test_terms[term][6][0])\
# 				or (test_terms[term][5][1] == test_terms[term][7][1] and loc == test_terms[term][7][0]) or \
# 					(test_terms[term][5][1] == test_terms[term][8][1] and loc == test_terms[term][8][0]) :
# 					cnt += 1
# 			else:
# 				print('{}\t{}\t{}'.format(term, loc, test_terms[term][1]))
# 	print(cnt)
# 	print(all_cnt)
# 	acc = cnt/all_cnt
# 	print(acc)
		 			
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
			# if ct < 0.4:
			# 	continue
			# cenp = cen.split('/')
			# cen = cenp[1] + '/' + cenp[0]
			if cent != cen:
				print(term)
				# print('{}\t{}\t{}'.format(term, cent, cen))
				wrongs += 1
				continue

			cnt += 1
			# pdb.set_trace()
			# print('{}\t{}'.format(term, at))
			sum_diff_c += (math.fabs(ct - c)/ct) 
			sum_diff_a += (math.fabs(at - alpha)/at) 
			# print('{}\t{}'.format(ct, (math.fabs(ct - c)/ct) * 100 ))
			terms[term] = [((math.fabs(at - alpha)/at) * 100) ]
		
	print(cnt)
	# cnt = cnt - wrongs
	print('average percentage error of c: {}'.format((sum_diff_c/cnt) * 100 ))
	print('average percentage error of alpha: {}'.format((sum_diff_a/cnt) * 100))
	print('wrongs: {}'.format(wrongs))




# with open('uni_03.txt') as f:
# 	sum_diff_c = 0
# 	sum_diff_a = 0
# 	cnt = 0
# 	wrongs = 0
# 	for line in f:
# 		parts = line.split('\t')
# 		if len(parts) == 1:
# 			continue
# 		cnt += 1
# 		term = parts[0]
# 		c = float(parts[2])
# 		alpha = float(parts[3])
# 		# if term not in test_terms:
# 		# 	print(term)
# 		# 	continue
# 		ct = float(test_terms[term][0])
# 		at = float(test_terms[term][1])
# 		cent = test_terms[term][2]
# 		cen = parts[1]
# 		if cent != cen:
# 			# print(term)
# 			wrongs += 1
# 			continue
			
# 		# pdb.set_trace()
# 		# print('{}\t{}\t{}\t{}'.format(term, at, (math.fabs(ct - c)/ct) * 100, (math.fabs(at - alpha)/at) * 100))
# 		sum_diff_c += (math.fabs(ct - c)/ct) * 100
# 		sum_diff_a += (math.fabs(at - alpha)/at) * 100 
# 		# print('{}\t{}'.format(term, (math.fabs(ct - c)) ))
# 		terms[term].append((math.fabs(at - alpha)/at) * 100 )
# 		# terms[term].append(at)


# with open('uni_01.txt') as f:
# 	sum_diff_c = 0
# 	sum_diff_a = 0
# 	cnt = 0
# 	wrongs = 0
# 	for line in f:
# 		parts = line.split('\t')
# 		if len(parts) == 1:
# 			continue
# 		cnt += 1
# 		term = parts[0]
# 		c = float(parts[2])
# 		alpha = float(parts[3])
# 		# if term not in test_terms:
# 		# 	print(term)
# 		# 	continue
# 		ct = float(test_terms[term][0])
# 		at = float(test_terms[term][1])
# 		cent = test_terms[term][2]
# 		cen = parts[1]
# 		if cent != cen:
# 			# print(term)
# 			wrongs += 1
# 			continue
			
# 		# pdb.set_trace()
# 		# print('{}\t{}\t{}\t{}'.format(term, at, (math.fabs(ct - c)/ct) * 100, (math.fabs(at - alpha)/at) * 100))
# 		sum_diff_c += (math.fabs(ct - c)/ct) * 100
# 		sum_diff_a += (math.fabs(at - alpha)/at) * 100 
# 		# print('{}\t{}'.format(term, (math.fabs(ct - c)) ))
# 		terms[term].append((math.fabs(at - alpha)/at) * 100 )
# 		terms[term].append(at)

# for item in terms:
# 	print('{}\t{}\t{}\t{}\t{}'.format(item, terms[item][0], terms[item][1], terms[item][2], terms[item][3]))
