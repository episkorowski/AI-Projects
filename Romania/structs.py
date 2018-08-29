import collections
import heapq

class Queue:
	def __init__(self):
		self.elements = collections.deque()
		self.visited = []
	
	def empty(self):
		return len(self.elements) == 0
	
	def put(self, x):
		self.elements.append(x)

	def get(self):
		return self.elements.popleft()


class Stack:
	def __init__(self):
		self.elements = collections.deque()
		self.visited = []

	def empty(self):
		return len(self.elements) == 0
	
	def push(self, x):
		self.elements.append(x)

	def pop(self):
		return self.elements.pop()


class PriorityQueue:
	def __init__(self):
		self.elements = []

	def empty(self):
		return len(self.elements) == 0

	def put(self, item, priority):
		if self.empty():
			heapq.heappush(self.elements, (priority, item))
		if priority != self.elements[0][0]:		# Lazy tie breaking
			heapq.heappush(self.elements, (priority, item))

	def get(self):
		return heapq.heappop(self.elements)[1]
		
# Testing stuff
if __name__ == '__main__':
	s = Stack()
	q = Queue()
	pq = PriorityQueue()

	s.push(3)
	s.push(7)
	print(s.pop())

	q.put(3)
	q.put(7)
	print(q.get())
	print(q.elements)

	pq.put("Arad", 320)
	pq.put("Other City", 120)
	print(pq.get())