__author__="Sara Farazi"
import pdb
import math
import time
from cell import Point, Coordinates, Cell
from summary_base import Summary, Counter
from nltk.corpus import stopwords
from geopy.distance import great_circle

# Change this file path for running on different datasets:
file = "data/1mtweets.txt"

map_cells = {}
map_terms = {}
term_locations = {}
tests = []
all_terms = []

k = 5

# cameras = ['illinois', 'athens', 'basketball', 'hamilton', 'image', 'birthday', 'hawaii', 'paris', 'ohio']
cameras = ['minolta', 'sony', 'canon', 'olympus', 'nikon', 'pentax', 'samsung', 'leica', 'kodak', 'fujifilm']

# stop = set(stopwords.words('english'))

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


def is_word(word):
    chars = {'%', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    for char in chars:
        if char in word:
            return False
    return True
    
# Create a test set of incoming words:
def find_terms():
    with open('data/alpha-test.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            # l = line.replace('\n', '')
            parts = line.split('\t')
            tests.append(parts[0])

    # with open('Multi-Term/rare_multi.txt') as f:
    #     for line in f:
    #         l = line.replace('\n', '')
    #         # multi_qr.append(l)
    #         parts = l.split(' ')
    #         all_terms.append(parts[0])
    #         all_terms.append(parts[1])
    # with open('Multi-Term/med_multi.txt') as f:
    #     for line in f:
    #         l = line.replace('\n', '')
    #         # multi_qm.append(l)
    #         parts = l.split(' ')
    #         all_terms.append(parts[0])
    #         all_terms.append(parts[1])
    # with open('Multi-Term/frequent_multi.txt') as f:
    #     for line in f:
    #         l = line.replace('\n', '')
    #         # multi_qf.append(l)
    #         parts = l.split(' ')
    #         all_terms.append(parts[0])
    #         all_terms.append(parts[1])
    # with open('Multi-Term/tooFreq_multi.txt') as f:
    #     for line in f:
    #         l = line.replace('\n', '')
    #         # multi_qt.append(l)
    #         parts = l.split(' ')
    #         all_terms.append(parts[0])
    #         all_terms.append(parts[1])


# Create a map of the world: Each cell size is 1 x 1 degree latitude and logitude

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


# Read incoming terms with their locations and process earch term's summary:

def stream_terms():
    tot_time = 0
    with open(file) as f:
        lines = f.read().splitlines()
        for line in lines:
            start = time.time()
            parts = line.split("\t")
            text = parts[0].lower()
            lat = parts[1]
            lon = parts[2]
            
            cell_id = math.floor(float(lat)).__str__() + "/" + math.floor(float(lon)).__str__()
            # cell = map_cells[cell_id]
            terms = text.split(" ")
            # pdb.set_trace()

            for item in stop:
                if item in terms:
                    terms = list(filter((item).__ne__, terms))

            # print(terms)
            for item in terms:
                if item == '':
                    continue
                if item in tests:
                    if item in map_terms.keys():
                        map_terms[item].update_summary(cell_id)
                        map_terms[item].total += 1
                    else:
                        temp_summary = Summary(k)
                        temp_summary.update_summary(cell_id)
                        map_terms.update({item : temp_summary})
                        map_terms[item].total += 1
        #     print((time.time() - start))
            tot_time += (time.time() - start)
        # print(tot_time/len(lines))
                    # if item in term_locations.items():
                    #     term_locations[item].add(cell_id)
                    # else:
                    #     term_locations[item] = set([cell_id])
    
    
    for key, value in map_terms.items():
        value.counters = sorted(value.counters, key=lambda x: x.count, reverse=True)
        print("{}\t{}".format(key, value))


if __name__ == "__main__":
    find_terms()
    build_map()
    stream_terms()


