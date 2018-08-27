__author__="Sara Farazi"
import pdb
import math
from cell import Point, Coordinates, Cell
from geopy.distance import great_circle
import numpy as np
from scipy.optimize import brentq


class Counter:
	def __init__(self, cell_id, freq, err):
		self.cell = cell_id
		self.count = freq
		self.error = err
		self.rings = Rings(cell_id, 10)

	def __str__(self):
		return "{}\t{}\t{}\t{}".format(self.cell, self.count, self.error, self.rings)

class Ring_Counter:
	def __init__(self, cell_id, freq, err):
		self.cell = cell_id
		self.count = freq
		self.error = err
	def __str__(self):
		return "{}\t{}\t{}".format(self.cell, self.count, self.error)





class Summary:
	def __init__(self, k):
		self.size = k
		self.counters = []
		self.cnt = 0
		self.sum_dist = 0
		self.temp1 = 0
		self.temp2 = 0
		self.temp3 = 0
		self.temp_sum = []
		self.total = 0
		# self.total = 0
		# self.seen_cells = set()


	def update_summary(self, cell_id):
		cells = []
		for item in self.counters:
			cells.append(item.cell)
		if cell_id in cells:
			for it in self.counters:
				if it.cell == cell_id:
					it.count += 1
				else:
					it.rings.add_to_rings(cell_id) #here (add)
			return

			# ind = cells.index(cell_id)
			# self.counters[ind].count += 1
			
		if len(self.counters) >= self.size:
			(ind, minimum) = self.find_min_index()
			# if self.counters[ind].cell == self.sort()[0].cell:
			# 	# self.cnt += 1
			# 	d = self.get_dist(self.counters[ind].cell, cell_id)
				# self.sum_dist += d
			self.counters[ind].cell = cell_id
			self.counters[ind].count += 1
			self.counters[ind].error = minimum
			self.counters[ind].rings.update_rings2(cell_id) #here (up)
			# self.counters[ind].rings.change_key(cell_id)
			for c in self.counters:
				if c.cell == cell_id:
					continue
				c.rings.add_to_rings(cell_id)  #here (add)
			# self.cnt += 1
			



		if len(self.counters) < self.size:
			for c in self.counters:
				c.rings.add_to_rings(cell_id) # here (add)

			temp = Counter(cell_id, 1, 0)
			self.counters.append(temp)

	
		


	def find_min_index(self):
		minimum = float('inf')
		ind = -1
		for item in self.counters:
			if item.count < minimum:
				minimum = item.count
				ind = self.counters.index(item)

		return (ind, minimum)


	def get_dist(self, loc1, loc2):
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


	def sort(self):		
		sc = sorted(self.counters, key=lambda x: x.count, reverse=True)
		return sc


	def find_remained_cells(self):
		# d = 0
		# for item in self.temp_sum:
		# 	print(item)
		# print("*****************************************************")
		# for item in self.counters:
		# 	print(item)
		cnt = 0
		cells = [c.cell for c in self.counters]
		temps = self.temp_sum
		# print(cells)
		# print(temps)
		for item in cells:
			if item in temps:
				cnt += 1

		self.temp_sum = []
		for item in self.counters:
			self.temp_sum.append(item.cell)

		# print("*****************************************************")
		# for item in self.temp_sum:
		# 	print(item)
		# self.temp_sum = self.counters
		# # if len(self.counters) > 1:
		# # 	if len(self.temp_sum) <= 1:
		# # 		# d = 0
		# # 		cnt = 1
		# # 	elif self.sort()[0] != self.temp_sum[0]:
		# # 		# d = self.get_dist(self.sort()[2].cell, self.temp_sum[2].cell)
		# # 		cnt = 1
		# # 	else:
		# # 		cnt = 0
		# # self.temp_sum = self.sort()

		return cnt


	def __str__(self):
		
		str_res = ""
		for counter in self.counters: 
			str_res += counter.__str__() + '\t'
		str_res += 'tot: {}'.format(self.total)

		return str_res
		# return self.cnt.__str__()




class Rings:
	def __init__(self, term, k):
		# self.RING_SIZE = 200 
		# self.sizes = [1.0, 10.0, 100.0, 1000.0, 10000.0]
		# self.sizes = [100, 400.0, 2000.0, 10000.0]
		# self.sizes = [100, 270.0, 900.0, 3000.0, 10000.0]
		# self.sizes = [100, 102.4, 256.0, 640.0, 1600.0, 4000.0, 10000.0]
		# self.sizes = [100, 156.25, 312.5, 625.0, 1250.0, 2500.0, 5000.0, 10000.0]
		self.sizes= [100.77695999999999, 167.96159999999998, 279.936, 466.56, 777.6, 1296.0, 2160.0, 3600.0, 6000.0, 10000.0]
		# self.sizes = [1296.0, 2160.0, 3600.0, 6000.0, 10000.0]
		# self.sizes = [403.5360699999998, 576.4800999999998, 823.5429999999998, 1176.4899999999998, 1680.6999999999998, 2401.0, 3430.0, 4900.0, 7000.0, 10000.0]
		# self.sizes= [1342.1772800000006, 1677.7216000000005, 2097.1520000000005, 2621.4400000000005, 3276.8, 4096.0, 5120.0, 6400.0, 8000.0, 10000.0]
		# self.sizes = [3874.204890000001, 4304.672100000001, 4782.969000000001, 5314.410000000001, 5904.900000000001, 6561.0,7290.0, 8100.0, 9000.0, 10000.0]
		# self.sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

		self.key = term
		# self.size = k
		# self.sizes = [5.0, 50.0, 500.0, 5000.0]
		# self.sizes = [1.6, 8.0, 40.0, 200.0, 1000.0, 5000]
		# self.sizes = [1.0935, 3.645, 12.15, 40.5, 135.0, 450.0, 1500.0, 5000]
		# self.sizes = [1.3107200000000006, 3.276800000000001, 8.192000000000002, 20.480000000000004, 51.2, 128.0, 320.0, 800.0, 2000.0, 5000]
		# self.sizes = [9.765625, 19.53125, 39.0625, 78.125, 156.25, 312.5, 625.0, 1250.0, 2500.0, 5000]
		# self.sizes = [50.388479999999994, 83.98079999999999, 139.968, 233.28, 388.8, 648.0, 1080.0, 1800.0, 3000.0, 5000]
		# self.sizes = [201.7680349999999, 288.2400499999999, 411.7714999999999, 588.2449999999999, 840.3499999999999, 1200.5, 1715.0, 2450.0, 3500.0, 5000]
		# self.sizes = [671.0886400000003, 838.8608000000003, 1048.5760000000002, 1310.7200000000003, 1638.4, 2048.0, 2560.0, 3200.0, 4000.0, 5000]
		# self.sizes = [1937.1024450000004, 2152.3360500000003, 2391.4845000000005, 2657.2050000000004, 2952.4500000000003, 3280.5, 3645.0, 4050.0, 4500.0, 5000]
		# self.sizes = [500.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 3500.0, 4000.0, 4500.0, 5000]
		self.counters = {}
		self.create_rings()
		# self.average_rad_distance = 0
	
		

	def create_rings(self):
		for i in range (0,len(self.sizes)):
			self.counters[self.sizes[i]] = 0
		# self.counters['total'] = 1


	def add_to_rings(self, cell_id):			
		# if cell_id in seen_cells[item]:
		max_dist = 20000
		radius = 0
		
		r = self.get_dist(cell_id, self.key)
		radius = self.get_radius(r)
		# if radius < max_dist:
		if self.pick_or_not(cell_id, self.key, radius):
			if radius == 0:
				return
			self.counters[radius] += 1
			# print('{} was added to ring {}'.format(cell_id, radius))
				# self.counters['total'] += 1
		# seen_cells[item].remove(cell_id)
				# self.average_rad_distance = ((self.average_rad_distance * (self.counters['total']-1)) + radius)/self.counters['total']
				# print("one was added to ring {} for {} -- {}".format(radius, self.key, self.counters[radius]))


	def update_rings1(self, new_cell):
		max_dist = 10000
		points = self.generate_points()
		for k,v in self.counters.items():
			v = 0
		for point in points:
			dist = self.get_dist(new_cell, point)
			radius = self.get_radius(dist)
			# if radius < max_dist:
			self.counters[radius] += 1
		self.key = new_cell
		# print(self.counters)



	def update_rings2(self, new_cell):
		max_dist = 10000
		temp = {}
		for item in self.counters:
			temp[item] = self.counters[item]

		for item in self.counters:
			# print("K:{}, v:{}".format(item,self.counters[item]))
			self.counters[item] = 0
		
		for i in range(0, len(self.sizes)-1):
			a = self.sizes[i]
			b = self.sizes[i+1]
			for j in range(0, len(self.sizes)-1):
				c = self.sizes[j]
				d = self.sizes[j+1]
			
				overlap = self.get_rings_intersection(a, b, c, d, new_cell)
				total_area = (math.pi * math.pow(d,2)) - (math.pi * math.pow(c,2))
				ratio = overlap/total_area
				# print("{} .. {}".format(overlap,total_area))
				self.counters[a] += math.floor((ratio * temp[c])) + 1
			
				# print("{} - {} - {} - {}". format(a, ratio, self.counters[a], temp[c]))
		
		# for k, v in self.counters.items():
		# 	sum_ring += v
		# self.counters['total'] = sum_ring
		# print("{} is updated to {}".format(self.key, new_cell))
		self.key = new_cell


		

	def get_rings_intersection(self, a, b, c, d, new_cell):
		dist = self.get_dist(self.key, new_cell)
		if dist >= (b + d):
			return 0

		# print("{} - {} - {} - {} -- {}".format(a,b,c,d, dist))
		# a = c1 + c2 - c3
		x0 = float(new_cell.split('/')[0])
		y0 = float(new_cell.split('/')[1])
		x1 = float(self.key.split('/')[0])
		y1 = float(self.key.split('/')[1])
		biggest = self.areaOfIntersection(x0, y0, b, x1, y1, d)
		c1 = biggest - self.areaOfIntersection(x0, y0, a, x1, y1, d)
		c2 = biggest - self.areaOfIntersection(x0, y0, b, x1, y1, c)
		c3 = biggest - self.areaOfIntersection(x0, y0, a, x1, y1, c)
		# print("{} / {} / {}".format(c1, c2, c3))
		return (c1 + c2 - c3)/2
		


	def delete_rings(slef, changed_cell):
		pass

	def pick_or_not(self, cell, center, radius):
		return True

	def get_dist(self, loc1, loc2):
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


	def get_rad_distance(self, latlong_a, latlong_b):
		EARTH_CIRCUMFERENCE = 6378137	 # earth circumference in meters
		lat1, lon1 = latlong_a
		lat2, lon2 = latlong_b

		dLat = math.radians(lat2 - lat1)
		dLon = math.radians(lon2 - lon1)
		a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
				math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
				math.sin(dLon / 2) * math.sin(dLon / 2))
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
		d = EARTH_CIRCUMFERENCE * c
		
		return d

	
	def generate_points(self):
		points = []
		lat1 = float(self.key.split('/')[0])
		lon1 = float(self.key.split('/')[1])
		for k, val in self.counters.items():
			if val > 0:
				tc = (2 * math.pi)/val
				d = k/6378137
				for i in range (0, val):
					lat =math.asin(math.sin(lat1)*math.cos(d)+math.cos(lat1)*math.sin(d)*math.cos(i * tc))
					dlon=math.atan2(math.sin(i * tc)*math.sin(d)*math.cos(lat1),math.cos(d)-math.sin(lat1)*math.sin(lat))
					lon= ((lon1 - dlon + math.pi) % (2 * math.pi) )- math.pi
					new_point = lat.__str__() + '/' + lon.__str__()
					points.append(new_point)
		
		return points
			



	def get_radius(self, dist):
		if dist < self.sizes[0]:
			return self.sizes[0]
		if dist >= self.sizes[len(self.sizes)-1]:
			return self.sizes[len(self.sizes)-1]

		for i in range(0, len(self.sizes) - 1):
			if dist >= self.sizes[i] and dist < self.sizes[i+1]:
				return self.sizes[i]


	def sort(self):
		pass


	def areaOfIntersection(self, x0, y0, r0, x1, y1, r1):
		if r0 == 0:
			r0 = 10
		R = r0
		r = r1
		d = math.sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0));
		try:
			if d <= abs(R-r):
				# One circle is entirely enclosed in the other.
				return np.pi * min(R, r)**2
			if d >= r + R:
				# The circles don't overlap at all.
				return 0

			r2, R2, d2 = r**2, R**2, d**2
			alpha = np.arccos((d2 + r2 - R2) / (2*d*r))
			beta = np.arccos((d2 + R2 - r2) / (2*d*R))
			return ( r2 * alpha + R2 * beta -
			     0.5 * (r2 * np.sin(2*alpha) + R2 * np.sin(2*beta))
			   )
		except:
			print("error in intersection")
			return 0



	def __str__(self):
		
		str_res = ""
		for k, v in self.counters.items(): 
			str_res += k.__str__() + " " + v.__str__() + '\t'

		return str_res



class Rings2:
	def __init__(self, term, k):
		self.size = k
		self.counters = []
		self.key = term
		max_dist = 20000


	def change_key(self, t):
		self.key = t
	
	def get_radius(self, dist):
		sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000]
		if dist < sizes[0]:
			return sizes[0]
		if dist >= sizes[len(sizes)-1]:
			return sizes[len(sizes)-1]

		for i in range(0, len(sizes) - 1):
			if dist >= sizes[i] and dist < sizes[i+1]:
				return sizes[i+1]



	def get_dist(self, loc1, loc2):
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


	def update_rings(self, dist):
		d = self.get_dist(self.key, dist)
		cell_id = self.get_radius(d)
		cells = []
		for item in self.counters:
			cells.append(item.cell)
		if cell_id in cells:
			for it in self.counters:
				if it.cell == cell_id:
					it.count += 1
					return

			# ind = cells.index(cell_id)
			# self.counters[ind].count += 1
			
		if len(self.counters) >= self.size:
			(ind, minimum) = self.find_min_index()
			self.counters[ind].cell = cell_id
			self.counters[ind].count += 1
			self.counters[ind].error = minimum


		if len(self.counters) < self.size:
			temp = Ring_Counter(cell_id, 1, 0)
			self.counters.append(temp)



	def find_min_index(self):
		minimum = float('inf')
		ind = -1
		for item in self.counters:
			if item.count < minimum:
				minimum = item.count
				ind = self.counters.index(item)

		return (ind, minimum)


	def __str__(self):
		
		str_res = ""
		for counter in self.counters: 
			str_res += counter.__str__() + '\t'

		return str_res