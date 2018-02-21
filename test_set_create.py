import pdb
import json
import re
import sys
import math
import random

all_terms = []

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


with open('data/1mtweets.txt') as f:
	for line in f:
		parts = line.split("\t")
		text = parts[0].lower()

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
			all_terms.append(item)




test_terms = set()

while len(test_terms) < 1000:
	t = random.randint(10, len(all_terms))
	test_terms.add(all_terms[t])
	all_terms.remove(all_terms[t])




file = open('Results/random_test_1000.txt', 'w')

for i in test_terms:
	file.write(i + '\n')