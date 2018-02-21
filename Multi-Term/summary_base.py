__author__="Sara Farazi"


class Counter:
	def __init__(self, cell_id, freq, err):
		self.cell = cell_id
		self.count = freq
		self.error = err
		self.rings = Summary(10)

	def __str__(self):
		if len(self.rings.counters) == 0:
			return "{}\t{}\t{}".format(self.cell, self.count, self.error)
		else:
			return "{}\t{}\t{}\t{}".format(self.cell, self.count, self.error, self.rings)



class Summary:
	def __init__(self, k):
		self.size = k
		self.counters = []
		self.cnt = 0

	def update_summary(self, cell_id):
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


	def sort(self):
		pass

	def __str__(self):
		
		str_res = ""
		for counter in self.counters: 
			str_res += counter.__str__() + '\t'

		return str_res


