import pdb
import json
import re
import sys
import math
from summary_base import Summary
from pymongo import MongoClient
from cell import Point, Coordinates, Cell
from scipy.optimize import minimize_scalar
from geopy.distance import great_circle

file = "../data/flickr1m.txt"

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
tests = []
map_terms = {}


def find_terms():
    with open('rare_multi.txt') as f:
        for line in f:
            l = line.replace('\n', '')
            tests.append(l)
    with open('med_multi.txt') as f:
        for line in f:
            l = line.replace('\n', '')
            tests.append(l)
    with open('frequent_multi.txt') as f:
        for line in f:
            l = line.replace('\n', '')
            tests.append(l)
    with open('tooFreq_multi.txt') as f:
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


def find_trends(k):
    with open(file) as f:
        for line in f:
                parts = line.split("\t")
                text = parts[0].lower()
                lat = parts[1]
                lon = parts[2]
                cell_id = math.floor(float(lat)).__str__() + "/" + math.floor(float(lon)).__str__()
                # terms = text.split(" ")
                # for item in stop:
                #     if item in terms:
                #         terms = list(filter((item).__ne__, terms))


                for item in tests:               
                    if item in text:
                        if item in map_terms.keys():
                            map_terms[item].update_summary(cell_id)
                        else:
                            temp_summary = Summary(k)
                            temp_summary.update_summary(cell_id)
                            map_terms.update({item : temp_summary})


    for key, value in map_terms.items():
        value.counters = sorted(value.counters, key=lambda x: x.count, reverse=True)
        print("{}\t{}".format(key, value))

if __name__ == "__main__":
    find_terms()
    build_map()
    find_trends(1000)
