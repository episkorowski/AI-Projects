import csp
import sys

def argParse(args):
	length = len(args)
	assignment = csp.Assignment()
	if args[2] == "backtrack":
		bt = csp.BacktrackingSearch()
		if args[1] == "aus":
			aus = csp.AustraliaCSP()
			if length == 4:
				if args[3] == "mrv":
					print(bt.backtrack(assignment, aus, bt.mrv))
				if args[3] == "mac":
					print(bt.backtrack(assignment, aus, None, None, bt.AC3))
			elif length > 4:
				print(bt.backtrack(assignment, aus, bt.mrv, None, bt.AC3))
			elif length < 4:
				print(bt.backtrack(assignment, aus))
			else:
				print("Invalid Argument")

		elif args[1] == "usa":
			usa = csp.AmericaCSP()
			if length == 4:
				if args[3] == "mrv":
					print(bt.backtrack(assignment, usa, bt.mrv))
				if args[3] == "mac":
					print(bt.backtrack(assignment, usa, None, None, bt.AC3))
			elif length > 4:
				print(bt.backtrack(assignment, usa, bt.mrv, None, bt.AC3))
			elif length < 4:
				print(bt.backtrack(assignment, usa))
			else:
				print("Invalid Argument")

	elif args[2] == "minconflicts":
		minc = csp.MinConflictsSearch()
		if args[1] == "aus":
			aus = csp.AustraliaCSP()
			print(minc.solve(aus))

		elif args[1] == "usa":
			usa = csp.AmericaCSP()
			print(minc.solve(usa))

	else:
		print("Invalid Argument")


def main():
	argParse(sys.argv)

main()

