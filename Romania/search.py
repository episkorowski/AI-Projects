"""Search (Chapters 3-4)

The way to use this code is to subclass Problem to create a class of problems,
then create problem instances and solve them with calls to the various search
functions."""

import sys
import csv
import ast
import structs

#______________________________________________________________________________

class Problem:
	"""The abstract class for a formal problem.  You should subclass this and
	implement the method successor, and possibly __init__, goal_test, and
	path_cost. Then you will create instances of your subclass and solve them
	with the various search functions."""
	
	
	def __init__(self, initial, goal=None):
		"""The constructor specifies the initial state, and possibly a goal
		state, if there is a unique goal.  Your subclass's constructor can add
		other arguments."""
		self.initial = initial; self.goal = goal
		
	def successor(self, state):
		"""Given a state, return a sequence of (action, state) pairs reachable
		from this state. If there are many successors, consider an iterator
		that yields the successors one at a time, rather than building them
		all at once. Iterators will work fine within the framework."""
		raise NotImplementedError("successor() must be implemented in subclass")
	
	def goal_test(self, state):
		"""Return True if the state is a goal. The default method compares the
		state to self.goal, as specified in the constructor. Implement this
		method if checking against a single self.goal is not enough."""
		return state == self.goal
	
	def path_cost(self, c, state1, action, state2):
		"""Return the cost of a solution path that arrives at state2 from
		state1 via action, assuming cost c to get up to state1. If the problem
		is such that the path doesn't matter, this function will only look at
		state2.  If the path does matter, it will consider c and maybe state1
		and action. The default method costs 1 for every step in the path."""
		return c + 1
		
	def h(self, node):
		"""Return the heuristic function value for a particular node. Implement
		this if using informed (heuristic) search."""
		return 0
#______________________________________________________________________________

class Graph:

	# It's just a dictionary
	def __init__(self):
		self.edges = {}

	# Returns the value of the given state
	def neighbors(self, state):
		return self.edges[state]

#______________________________________________________________________________


class RomaniaProblem(Problem):

	def __init__(self, initial, goal):
		super().__init__(initial, goal)
		self.map = self.createMap()
		self.path = []
		self.heuristic = {"Arad": 366, "Bucharest": 0, "Craiova": 160,
		"Drobeta": 242, "Eforie": 161, "Fagaras": 176, "Giurgiu": 77,
		"Hirsova": 151, "Iasi": 226, "Lugoj": 244, "Mehadia": 241,
		"Neamt": 234, "Oradea": 380, "Pitesti": 100, "Rimnicu Vilcea": 193,
		"Sibiu": 253, "Timisoara": 329, "Urziceni": 80, "Vaslui": 199,
		"Zerind": 374}

	# Creates the map of Romania using the csv file. Stores them in the graph class, with
	# cities as keys, and their values as lists of tuples containing possible destinations and
	# path costs. So the value of "Arad" would be: [('Sibiu', 140), ('Timisoara', 118), ('Zerind', 75)].
	def createMap(self):
		map = Graph()
		tuple_list = []
		with open('romania_adjacency_list.csv') as file:
			reader = csv.reader(file)
			for row in reader:
				rowlen = len(row)
				city = row[0]
				for i in range(1, rowlen, 2):
					tuple_list.append((row[i], int(row[i+1])))
				map.edges[city] = tuple_list
				tuple_list = []
		return map


	def successor(self, state):
		state_action_list = []
		for city in self.map.neighbors(state):
			state_action_list.append(("ACTION", city[0]))

		return state_action_list
	
	def path_cost(self, c, state1, action, state2):

		# Stores the successors and path costs of state1
		state1_successors = self.map.neighbors(state1)

		# Loops through the successors, records the path cost to state2
		for i in range(0, len(state1_successors)):
			if state1_successors[i][0] == state2:
				c += state1_successors[i][1]
		return c


	def h(self, node):
		return self.heuristic[node.state] + node.path_cost


#______________________________________________________________________________

class EightPuzzle(Problem):
	def __init__(self, initial, goal):
		super().__init__(initial, goal)

	def out_of_place(self, state):
		goal = [0,1,2,3,4,5,6,7,8]
		out_of_place = 0
		for i in range(0, len(state)):
			if state[i] != goal[i]:
				out_of_place += 1
		return out_of_place

	# Not working
	def manhattan(self, state):
		goal = [[0,1,2],[3,4,5],[6,7,8]]
		state = [state[i:i+3] for i in range(0,len(state),3)]
		mhd = 0
		for x in range(3):
			for y in range(3):
				if state[x][y] != goal[x][y]:
					value = state[x][y]
					xstart = x
					ystart = y
					xgoal = goal.index(x)
					ygoal = goal.index(y)
					dist = abs(xgoal - xstart) + abs(ygoal - ystart)
					mhd += dist
		return mhd

	def successor(self, state):
		zero_index = state.index(0)
		state_action_list = []	# More of an action-state list but I wanted to be consistent

		# UP
		if zero_index > 2:
			upstate = state[:]
			upstate[zero_index], upstate[zero_index - 3] = upstate[zero_index - 3], upstate[zero_index]
			state_action_list.append(("Up", upstate))

		# DOWN
		if zero_index < 6:
			downstate = state[:]
			downstate[zero_index], downstate[zero_index + 3] = downstate[zero_index + 3], downstate[zero_index]
			state_action_list.append(("Down", downstate))

		# LEFT
		if zero_index not in [0,3,6]:
			leftstate = state[:]
			leftstate[zero_index], leftstate[zero_index - 1] = leftstate[zero_index - 1], leftstate[zero_index]
			state_action_list.append(("Left", leftstate))

		# RIGHT
		if zero_index not in [2,5,8]:
			rightstate = state[:]
			rightstate[zero_index], rightstate[zero_index + 1] = rightstate[zero_index + 1], rightstate[zero_index]
			state_action_list.append(("Right", rightstate))

		return state_action_list

	def path_cost(self, c, state1, action, state2):
		return c + 1

	# Heuristic is number of squares out of place
	def h(self, node):
		return self.out_of_place(node.state)
		



#______________________________________________________________________________


class Node:
	"""A node in a search tree. Contains a pointer to the parent (the node
	that this is a successor of) and to the actual state for this node. Note
	that if a state is arrived at by two paths, then there are two nodes with
	the same state.  Also includes the action that got us to this state, and
	the total path_cost (also known as g) to reach the node.  Other functions
	may add an f and h value. You will not need to
	subclass this class."""

	def __init__(self, state, parent=None, action=None, path_cost=0):
		"Create a search tree Node, derived from a parent by an action."
		self.state = state
		self.parent = parent
		self.action = action
		self.path_cost = path_cost
		self.depth = 0
		
		if parent:
			self.depth = parent.depth + 1
			
	def __str__(self):
		return "<Node " + self.state + ">"
	
	def path(self):
		"Create a list of nodes from the root to this node."
		x, result = self, [self]
		while x.parent:
			result.append(x.parent)
			x = x.parent
		return result

	def expand(self, problem):
		"Return a list of nodes reachable from this node. [Fig. 3.8]"
		return [Node(next, self, act,
					 problem.path_cost(self.path_cost, self.state, act, next))
				for (act, next) in problem.successor(self.state)]

#______________________________________________________________________________
## Uninformed Search algorithms

def breadth_first_search(problem):
	frontier = structs.Queue()
	frontier.put(Node(problem.initial))
	visited = []
	nodes_visited = 0

	while not frontier.empty():
		curr_node = frontier.get()

		#print("Now visiting: " + str(curr_node))
		nodes_visited += 1

		if problem.goal_test(curr_node.state):
			return curr_node, nodes_visited, curr_node.path_cost
		if (curr_node.state not in visited):
			visited.append(curr_node.state)

			neighbors = sorted(curr_node.expand(problem), key=lambda x: x.state)

			for node in neighbors:
				if problem.goal_test(node.state):
					return node, nodes_visited, node.path_cost
				if node.state not in visited and node not in frontier.elements:
					frontier.put(node)

			
	
def depth_first_search(problem):
	frontier = structs.Stack()
	frontier.push(Node(problem.initial))
	visited = []
	nodes_visited = 0

	while not frontier.empty():
		curr_node = frontier.pop()

		#print("Now visiting: " + str(curr_node))
		nodes_visited += 1

		if problem.goal_test(curr_node.state):
			return curr_node, nodes_visited, curr_node.path_cost
		if (curr_node.state not in visited):
			visited.append(curr_node.state)
			
			neighbors = curr_node.expand(problem)[::-1]

			for node in neighbors:
				if node.state not in visited:
					frontier.push(node)


#______________________________________________________________________________
# Informed (Heuristic) Search

def astar_search(problem):
	frontier = structs.PriorityQueue()
	init_node = Node(problem.initial)
	frontier.put(init_node, problem.h(init_node))
	visited = []
	nodes_visited = 0

	while not frontier.empty():
		curr_node = frontier.get()

		#print("Now visiting: " + str(curr_node))
		nodes_visited +=1

		if problem.goal_test(curr_node.state):
			return curr_node, nodes_visited, curr_node.path_cost
		if (curr_node.state not in visited):
			visited.append(curr_node.state)
			
			neighbors = sorted(curr_node.expand(problem), key=lambda x: x.state)

			for node in neighbors:
				if node.state not in visited:
					#print(node.state, problem.h(node), node.path_cost)
					frontier.put(node, problem.h(node))

	print("Not Found")

#______________________________________________________________________________

''' Parses command line arguments. I probably could have imported a library to do this
	but then I would have had to learn how to use it.'''

def argParse(args):
	if args[2] == "dfs":
		if args[1] == "romania":

			result = depth_first_search(RomaniaProblem(args[3], "Bucharest"))
			path_list = [x.state for x in result[0].path()[::-1]]
			print("Final Path: " + " - ".join(path_list))
			print("Cost:",result[2])
			print("Nodes Visited:", result[1])

		elif args[1] == "eight":

			result = depth_first_search(EightPuzzle(ast.literal_eval(args[3]), [0,1,2,3,4,5,6,7,8]))
			path_list = [x.action for x in result[0].path()[::-1]]
			print("Final Path: " + " - ".join(path_list[1:]))
			print("Cost:",result[2])
			print("Nodes Visited:", result[1])

		else:
			print("Invalid Argument: "+args[1]+" is not a valid problem")

	elif args[2] == "bfs":
		if args[1] == "romania":

			result = breadth_first_search(RomaniaProblem(args[3], "Bucharest"))
			path_list = [x.state for x in result[0].path()[::-1]]
			print("Final Path: " + " - ".join(path_list))
			print("Cost:",result[2])
			print("Nodes Visited:", result[1])

		elif args[1] == "eight":
			
			result = breadth_first_search(EightPuzzle(ast.literal_eval(args[3]), [0,1,2,3,4,5,6,7,8]))
			path_list = [x.action for x in result[0].path()[::-1]]
			print("Final Path: " + " - ".join(path_list[1:]))
			print("Cost:",result[2])
			print("Nodes Visited:", result[1])

		else:
			print("Invalid Argument: "+args[1]+" is not a valid problem")

	elif args[2] == "astar":
		if args[1] == "romania":
			
			result = astar_search(RomaniaProblem(args[3], "Bucharest"))
			path_list = [x.state for x in result[0].path()[::-1]]
			print("Final Path: " + " - ".join(path_list))
			print("Cost:",result[2])
			print("Nodes Visited:", result[1])

		elif args[1] == "eight":
			
			result = astar_search(EightPuzzle(ast.literal_eval(args[3]), [0,1,2,3,4,5,6,7,8]))
			path_list = [x.action for x in result[0].path()[::-1]]
			print("Final Path: " + " - ".join(path_list[1:]))
			print("Cost:",result[2])
			print("Nodes Visited:", result[1])

		else:
			print("Invalid Argument: "+args[1]+" is not a valid problem")

	else:
		print("Invalid Argument: "+args[2]+" is not a valid algorithm")


#______________________________________________________________________________
## Main
			 

def main():

	
	#test_problem = RomaniaProblem("Arad", "Bucharest")

	#print("Cost: " + str(test_problem.path_cost(0, "Arad", " to ", "Zerind")))
	#print(test_problem.map.neighbors("Arad"))

	#test_problem2 = EightPuzzle([1,4,2,3,0,5,6,7,8], [0,1,2,3,4,5,6,7,8])
	#print(test_problem2.successor([3,1,2,6,4,5,7,8,0]))
	#state = [3,1,2,6,4,5,7,8,0]
	#state = [state[i:i+3] for i in range(0,len(state),3)]
	#print(state)

	#test_problem2.manhattan([3,1,2,6,4,5,7,8,0])


	argParse(sys.argv)
	
	

main()