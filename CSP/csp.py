"""The code in this module is based on the Java code for Constraint Satisfaction
Problems available from Artificial Intelligence: A Modern Approach (3rd Ed.)
created by Ruediger Lunde and Mike Stampone

Author: Brian O'Neill
"""
import collections
import random

class SolutionStrategy:
    """Abstract base class for CSP solver implementations. Solving a CSP means
    finding an assignment which is consistent and complete with respect to a
    CSP. This abstract class provides the central interface method.
    """

    def solve(self, csp):
        """Returns a solution to the specified CSP, which specifies values
        for the variables such that the constraints are satisfied.

        :param csp: A CSP to solve
        :return An Assignment object, representing a solution to the specified
        CSP, which specifies values for variables such that the constraints
        are satisfied
        """
        raise NotImplementedError('Must be implemented by subclass')


class CSP:
    """A constraint satisfaction problem (CSP) consists of three components: X,
    D, and C:

    X is a set of variables (X1, ... , Xn}
    D is a set of domains {D1, ... , Dn}, one for each variable.
    C is a set of constraints that specify allowable combinations of values.
    """

    def __init__(self, variables=None):
        if variables is None:
            variables = []
        self.__variables = variables
        self.__domains = []
        self.__constraints = []
        self.__var_index_map = {}  # Variable to index map
        self.__constraint_network = {}  # Variable to constraint map

    def _add_variable(self, var):
        if var not in self.__var_index_map:
            empty_domain = Domain()
            self.__variables.append(var)
            self.__domains.append(empty_domain)
            self.__var_index_map[var] = len(self.__variables)-1
            self.__constraint_network[var] = []
        else:
            raise ValueError('Variable with same name already exists.')

    def get_variables(self):
        return tuple(self.__variables)

    def _index(self, var):
        return self.__var_index_map[var]

    def get_domain(self, var):
        """Returns the Domain for a given variable"""
        return self.__domains[self.__var_index_map[var]]

    def set_domain(self, var, domain):
        """Sets the Domain for the given variable"""
        self.__domains[self._index(var)] = domain

    def remove_value_from_domain(self, var, value):
        """Replaces the domain of the specified variable by new domain,
        which contains all values of the old domain except the specified
        value.
        """
        current_domain = self.get_domain(var)
        values = []
        for item in current_domain:
            if item != value:
                values.append(item)
        self.set_domain(var, Domain(values))

    def add_constraint(self, constraint):
        """Add a constraint to the problem"""
        self.__constraints.append(constraint)
        for var in constraint.get_scope():
            self.__constraint_network[var].append(constraint)

    def get_constraints(self, var=None):
        """Return all constraints, or the constraints for a given variable"""
        if var is None:
            return self.__constraints
        else:
            return self.__constraint_network[var]

    def get_neighbor(self, var, constraint):
        """For binary constraints, returns the other variable from the scope.
        Returns None for non-binary constraints
        """
        scope = constraint.get_scope()
        if len(scope) == 2:
            if var == scope[0]:
                return scope[1]
            elif var == scope[1]:
                return scope[0]

        return None

    def copy_domains(self):
        """Returns a copy which contains a copy of the domains list. In all
        other aspects, this is a flat (shallow) copy of this object.
        """
        result = CSP()
        result.__variables = self.__variables
        for d in self.__domains:
            result.__domains.append(d)
        result.__constraints = self.__constraints
        result.__var_index_map = self.__var_index_map
        result.__constraint_network = self.__constraint_network
        return result

#################################################################

class AustraliaCSP(CSP):
	def __init__(self):
		super().__init__(variables=None)
		domain = Domain(["Red", "Blue", "Yellow"])
		map = self.createMap()
		for key in map.keys():
			self._add_variable(key)
			#print("Key:",key)
			self.set_domain(key, domain)
		for key in map.keys():
			for item in map[key]:
				constraint = NotEqualConstraint(key, item)
				self.add_constraint(constraint)


	def createMap(self):
		map = {}
		adj = []
		with open('australia-adj-list.txt', 'r') as f:
			for line in f:
				# Check if not comment or empty line
				if not line.startswith("#") and line.strip() != '':
					line_list = [x.strip() for x in line.split(',')]
					region = line_list[0]
					for i in range(1, len(line_list)):
						adj.append(line_list[i])
					map[region] = adj
				adj = []
		return map


#################################################################

class AmericaCSP(CSP):
	def __init__(self):
		super().__init__(variables=None)
		domain = Domain(["Red", "Blue", "Yellow", "Green"])
		map = self.createMap()
		for key in map.keys():
			self._add_variable(key)
			#print("Key:",key)
			self.set_domain(key, domain)
		for key in map.keys():
			for item in map[key]:
				constraint = NotEqualConstraint(key, item)
				self.add_constraint(constraint)

	def createMap(self):
		map = {}
		adj = []
		with open('usa-adj-list.txt', 'r') as f:
			for line in f:
				# Check if not comment or empty line
				if not line.startswith("#") and line.strip() != '':
					line_list = [x.strip() for x in line.split(',')]
					region = line_list[0]
					for i in range(1, len(line_list)):
						adj.append(line_list[i])
					map[region] = adj
				adj = []
		return map

#################################################################


class BacktrackingSearch(SolutionStrategy):
    # Initializes with no inference or ordering stuff enabled by default
    def __init__(self):
        super().__init__()
        #assignment = Assignment()
        #self.csp = csp

    # Default order of variables
    def first_unassigned(self, assignment, csp):
        var_list = [var for var in csp.get_variables() if not assignment.__contains__(var)]
        return var_list[0]

    # Default order of domains
    def unordered(self, var, assignment, csp):
        return csp.get_domain(var)

    # Default inference function
    def no_inference(self, csp, var, values):
        return True

    def mrv(self, assignment, csp):
        result = None
        count = 0
        for var in csp.get_variables():
            if not assignment.__contains__(var):
                if len(csp.get_domain(var)) == 0:
                    return var
                num_conflicts = len(csp.get_constraints(var))
                if num_conflicts >= count:
                    count = num_conflicts
                    result = var
        return result

    def AC3(self, csp, var, value):
        queue = collections.deque()
        for Xi in csp.get_variables():
            cons = csp.get_constraints(Xi)
            for con in cons:
                Xj = csp.get_neighbor(Xi, con)
                queue.append((Xi, Xj))

        while len(queue) != 0:
            (Xi, Xj) = queue.popleft()
            if self.revise(csp, Xi, Xj):
                if csp.get_domain(Xi).__len__() == 0:
                    return False
                cons = csp.get_constraints(Xi)
                for con in cons:
                    Xk = csp.get_neighbor(Xi, con)
                    if Xk != Xi:
                        queue.append((Xk, Xi))
        return True


    def revise(self, csp, Xi, Xj):
        revised = False
        Di = csp.get_domain(Xi)
        Dj = csp.get_domain(Xj)
        assignment = Assignment()
        cons = csp.get_constraints(Xi)
        for x in Di:
            for y in Dj:
                assignment.__setitem__(Xi, y)
                if not assignment.is_consistent(cons):
                    csp.remove_value_from_domain(Xi, x)
                    revised = True
        return revised



    def backtrack(self, assignment, csp,
            select_unassigned_variable=None, 
            order_domain_values=None, 
            inference=None):

        if select_unassigned_variable == None:
            select_unassigned_variable = self.first_unassigned

        if order_domain_values == None:
            order_domain_values = self.unordered

        if inference == None:
            inference = self.no_inference

        def solve(self, assignment):

            if assignment.is_complete(csp.get_variables()):
                return assignment

            var = select_unassigned_variable(assignment, csp)

            for value in order_domain_values(var, assignment, csp):

                assignment.__setitem__(var, value)
                if assignment.is_consistent(csp.get_constraints(var)):

                    inf = inference(csp, var, value)
                    #inference = True # Temporary
                    #inf = self.AC3(csp)
                    #print(inf)

                    if inf:
                        result = solve(self, assignment)
                        if result is not None:
                            return result

                assignment.__delitem__(var)
                csp.remove_value_from_domain(var, value)

            return None

        result = solve(self, assignment)
        return result


#################################################################

class MinConflictsSearch(SolutionStrategy):
    def __init__(self):
        super().__init__()

    def solve(self, csp, max_steps=10000):
        current = self.random_assignment(csp)

        for i in range (max_steps):
            if current.is_solution(csp):
                return current
            conflicted_vars = self.get_conflicted_vars(current, csp)
            var = random.choice(conflicted_vars)
            value = self.get_min_conflict_domain(var, current, csp)
            current.__setitem__(var, value)

        return None

    def num_conflicts(self, assignment, constraints):
        num_conflicts = 0
        for con in constraints:
            if not con.is_satisfied_with(assignment):
                num_conflicts += 1
        return num_conflicts

    def random_assignment(self, csp):
        assignment = Assignment()
        for var in csp.get_variables():
            val = random.choice(csp.get_domain(var))
            assignment.__setitem__(var, val)
        return assignment

    def get_conflicted_vars(self, assignment, csp):
        result = []
        for con in csp.get_constraints():
            if not con.is_satisfied_with(assignment):
                for var in con.get_scope():
                    result.append(var)
        return result

    def get_min_conflict_domain(self, var, assignment, csp):
        min_conflicts = 9999999
        cons = csp.get_constraints()
        assignment_copy = assignment.copy()
        result_list = []

        for value in csp.get_domain(var):
            assignment_copy.__setitem__(var, value)
            num_conflicts = self.num_conflicts(assignment, cons)
            if num_conflicts <= min_conflicts:
                if num_conflicts < min_conflicts:
                    result_list = []
                    min_conflicts = num_conflicts
            result_list.append(value)

        return random.choice(result_list)


#################################################################

class Domain:
    """A domain D[i] consists of a set of allowable values {v1, ..., vk} for the
    corresponding variable X[i] and defines a default order on those values. This
    implementation guarantees that domains are never changed after they have been
    created. Domain reduction is implemented by replacement instead of modification,
    so previous states can easily and safely be restored.
    """
    def __init__(self, values=None):
        if values is None:
            values = []
        self.__values = []
        for v in values:
            self.__values.append(v)

    def is_empty(self):
        return len(self.__values) == 0

    def get_values(self):
        result = []
        for v in self.__values:
            result.append(v)
        return result

    def __len__(self):
        return len(self.__values)

    def __getitem__(self, key):
        return self.__values[key]

    def __contains__(self, item):
        return item in self.__values

    def __iter__(self):
        for item in self.__values:
            yield item

    def __eq__(self, other):
        return self.__values == other.__values

    def __str__(self):
        result = ['{']
        comma = False
        for value in self.__values:
            if comma:
                result.append(',')
            result.append(str(value))
            comma = True
        result.append('}')
        return ''.join(result)


class Constraint:
    """A Constraint specifies the allowable combination of values for a set of
    variables. Each constraint consists of a pair <scope,rel>, where score is a
    tuple of variables that participate in the constraint, and rel is a relation
    that defines the values that those variables can take on.

    Each subclass of Constraint defines its own relation.
    """

    def get_scope(self):
        """Returns a tuple of variables that participate in the constraint."""
        raise NotImplementedError('Must be implemented by subclass')

    def is_satisfied_with(self, assignment):
        """Constrains the values that the variables can take on."""
        raise NotImplementedError('Must be implemented by subclass')


class NotEqualConstraint(Constraint):
    """Represents a binary constraint which forbids equal values."""
    def __init__(self, var1, var2):
        self.__var1 = var1
        self.__var2 = var2
        self.__scope = (var1, var2)

    def get_scope(self):
        return self.__scope

    def is_satisfied_with(self, assignment):
        value = assignment[self.__var1]
        return (value is None) or value != assignment[self.__var2]


class Assignment:
    """An Assignment assigns values to some or all variables of a CSP."""
    def __init__(self):
        self.__values = {}  # Map of variables to values

    def get_variables(self):
        return tuple(self.__values.keys())

    def __getitem__(self, var):
        return self.__values.get(var, None)

    def __setitem__(self, var, value):
        self.__values[var] = value

    def __delitem__(self, key):
        if key in self.__values:
            del self.__values[key]

    def __contains__(self, item):
        return item in self.__values

    def is_consistent(self, constraints):
        """Returns True if this Assignment does not violate any of the
        given constraints.
        """
        for con in constraints:
            if not con.is_satisfied_with(self):
                return False
        return True

    def is_complete(self, variables):
        """Returns True if this Assignment assigns values to every
        variable in the given sequence.
        """
        for v in variables:
            if v not in self.__values:
                return False
        return True

    def is_solution(self, csp):
        """Returns True if this Assignment is consistent and complete
        with respect to the given CSP.
        """
        return self.is_consistent(csp.get_constraints()) and \
               self.is_complete(csp.get_variables())

    def copy(self):
        result = Assignment()
        for variable,value in self.__values.items():
            result[variable] = value
        return result

    def __str__(self):
        comma = False
        result = ['{']
        for variable,value in self.__values.items():
            if comma:
                result.append(',')
            result.append(variable+'='+value)
            comma = True
        result.append('}')
        return ''.join(result)

if __name__ == "__main__":
	#aus = AustraliaCSP()
	#us = AmericaCSP()
    pass