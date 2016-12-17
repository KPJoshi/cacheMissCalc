import sys, islpy as isl

#get input
if len(sys.argv)<2:
	print 'Error: input file not supplied'
	sys.exit(1)

try:
	execfile(sys.argv[1])
except (IOError, SyntaxError):
	print 'Error: missing or invalid input file'
	sys.exit(1)

#get (optional) output mode
outputMode = 'iscc'
if len(sys.argv)>2 and sys.argv[2]=='poly':
	outputMode = 'poly'

#convert constraint's iterators to a different one
#returns a modified COPY of the original
def cvtConstrIters(constr,itOrig,itNew):
	constr = constr.copy()
	for i in range(dims):
		if itOrig+str(i) in constr:
			constr[itNew+str(i)]=constr.pop(itOrig+str(i))
	return constr

#create a greater than constraint expr1>(=)expr2, possibly strict
#returns a completely new constraint
def createGTConstraint(expr1,expr2,gtIsStrict):
	expr1=expr1.copy()
	for var in expr2:
		if var in expr1:
			expr1[var]-=expr2[var]
		else:
			expr1[var]=-expr2[var]
	if gtIsStrict:
		if 1 in expr1:
			expr1[1]-=1
		else:
			expr1[1]=-1
	return expr1

#add lexicographic constraints to input set
#note that set is passed by reference and is modified
def addLexConstraint(set,greater,lesser):
	finalSet = isl.Set.empty(set.get_space())
	for i in range(dims):
		setc = set.copy()
		setc = setc.add_constraint(isl.Constraint.ineq_from_names(space,{greater+str(i): 1, lesser+str(i): -1, 1: -1}))
		finalSet = finalSet.union(setc)
		set = set.add_constraint(isl.Constraint.eq_from_names(space,{greater+str(i): 1, lesser+str(i): -1}))
	return finalSet

#add 1 dimension that represents order of statements
domain.append({'i'+str(dims): 1})
domain.append({'i'+str(dims): -1, 1: references-1})
dims += 1
