# Find the ground truth values of C and alpha for events (terms)

import pdb
import json
import re
import sys
import math

from pymongo import MongoClient
from cell import Point, Coordinates, Cell
from scipy.optimize import minimize_scalar
from geopy.distance import great_circle

file = "data/data2.txt"

# tests = ['louvre', 'nosotros', 'florence', 'scots', 'bilbao', 'brussels', 'leipzig', 'trondheim', 'oisterwijk', 'marseille', 
# 'shanghai', 'longwood', 'naperville', 'bali', 'chiang', 'stockholm', 'boulder', 'garda', 'noordwijkerhout', 'ann', 'elvert', 
# 'hyde', 'access-public', 'elijah', 'wildsingapore', 'interactive', 'giants', 'heithabyr', 'documentalista.', 'cronista', 'pecados', 
# 'indianapolis', 'valladolid', 'jersey', 'ascca', 'fototeca', 'd.c.', 'belgica', 'arbor.', 'auckland', 'geneva', 'kyoto', 'albuquerque', 
# 'linz', 'virtual', 'bristol', 'historia', 'sacramento', 'monterey', 'dresden', 'austin', 'brugge', 'reykjavik', 'brooklyn', 'nashville', 
# 'vienna', 'praha', 'arkansas', 'kanagawa', 'bmx', 'df', 'ottawa', 'sarthe', 'rotterdam', 'canberra', 'protocol', 'length', 'volviera', 
# 'viene', 'moscow', 'bronx', 'dublin', 'halifax', 'madridejos.fotos.es', 'queens', 'raftwet', 'focal', 'esperanzas', 'mays', 'rva', 
# 'osa', 'review', 'jewell', 'copenhagen', 'jakintza', 'crenshaw', 'sao', 'salzburg', 'agouti', 'madridejos', 'monica', 'waikiki', 
# 'beijing', 'moore', 'whitewater', 'dasyprocta', 'borough', 'dallas', 'oaxaca', 'budapest']
# 'newtown', 'paris', 'fighter', 'march', 'equipment', 'arrows', 'wasser', 'call', 'courant', 'meadow', 'balade', 'kirke', 'showcase', 
# 'piemonte', 'detail', 'cup']


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

all_terms = {}
map_cells = {}
# tests = ['thanksgiving', 'blackfriday', 'christmas', 'metoo', 'korea', 'trump', 'kevin', 'spacy', 'bitcoin', 'tax']
tests = []


def find_terms():
    # with open('New/rare_multi.txt') as f:
    #     for line in f:
    #         l = line.replace('\n', '')
    #         # tests.append(l)
    #         parts = l.split(' ')
    #         tests.append(parts[0])
    #         tests.append(parts[1])
    # with open('New/med_multi.txt') as f:
    #     for line in f:
    #         l = line.replace('\n', '')
    #         # tests.append(l)
    #         parts = l.split(' ')
    #         tests.append(parts[0])
    #         tests.append(parts[1])
    # with open('New/frequent_multi.txt') as f:
    #     for line in f:
    #         l = line.replace('\n', '')
    #         # tests.append(l)
    #         parts = l.split(' ')
    #         tests.append(parts[0])
    #         tests.append(parts[1])
    # with open('New/tooFreq_multi.txt') as f:
    #     for line in f:
    #         l = line.replace('\n', '')
    #         # tests.append(l)
    #         parts = l.split(' ')
    #         tests.append(parts[0])
    #         tests.append(parts[1])
    with open('data/alpha-test.txt') as f:
        for line in f:
            l = line.replace('\n', '')
            tests.append(l)


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
    p1 = (x1, y1)
    p2 = (x2, y2)
    res = great_circle(p1, p2).kilometers
    # print(res)
    return res


def find_trends():
    cnt = 0
    # resf = open('Results/random_query_1000_true_events.txt', 'w') 
    with open(file) as f:
        for line in f:
                parts = line.split("\t")
                text = parts[0].lower()
                lat = parts[2]
                lon = parts[1]
                location = math.floor(float(lat)).__str__() + "/" + math.floor(float(lon)).__str__()
                terms = text.split(" ")
                for item in stop:
                    if item in terms:
                        terms = list(filter((item).__ne__, terms))


                for term in terms:
                    if term == '':
                        continue
                    if term in tests:
                        # print(term)
                        if all_terms.get(term, None):
                            if all_terms[term].get(location, None):
                                all_terms[term][location] += 1
                            else:
                                all_terms[term].update({location: 1})
                        else:
                            all_terms.update({term: {location: 1}})


    for key, value in all_terms.items():
        max_count = 0
        loc = ""
        count_sum = 0
        for k, val in value.items():
            count_sum += val
            if val > max_count:
                max_count = val
                loc = k
        value.update({'center': (loc, max_count/count_sum)})
        value.update({'sum': count_sum})



    for key, value in all_terms.items():
        if key in tests:
            if value['center'][1] == 1:
                print(key)
                continue
            # if value['sum'] < 50:
            #     continue

            def f(x):

                result = 0        
                for k, val in value.items():
                    if k == 'center' or k == 'sum':
                        continue
                    dist = get_dist(value['center'][0], k)
                    if dist == 0:
                        continue


                    result = result + math.log(value['center'][1] * ( dist **(-x))) 
                    # print(value)
                
                used_locations = [val for k, val in value.items()]

                for k, val in map_cells.items():
                    if k not in used_locations:
                        dist = get_dist(value['center'][0], k)
                        if dist == 0 or dist == 1:
                            continue
                

                        result = result + math.log(1 - (value['center'][1] * (dist**(-x)))) 

                # print(result)
                
                return (-1) * result


            res = minimize_scalar(f, bounds = (0,5), method = "bounded")
            # print("Done optimization")
            
            alpha = res.x
            value.update({'alpha': alpha})

            print('{}\t{}\t{}\t{}\t{}'. format(key, value['center'][0], value['center'][1], value['alpha'], value['sum']))
            # resf.write('\n')
            cnt += 1
            print(cnt)
    # resf.close()


if __name__ == "__main__":
    find_terms()
    build_map()
    find_trends()
