import islpy as isl

# BEGIN data to be entered by user

nBlocks = 64 #no. of cache blocks
blockSz = 64 #size of block in bytes

dims = 1
params = 0
references = 2

#constraints on the domain
#it is expected that the iteration dimensions are i0, i1, ... and the parameters are p0, p1, ...
domain = [{'i0': 1},{'i0': -1, 1: 1023}]

#schedule is expected to be lexicographic in i0,i1,... and order of specification of the statements

#memory location accessed by each reference
#representing a linear expression to calculate the memory location accessed by the reference
refMem = ([
		  {'i0': 4},
		  {'i0': 4, 1: 4096},
])

# END data to be entered by user

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
def addLexConstraint(set,greater,lesser,stmt1Idx,stmt2Idx):
	finalSet = isl.Set.empty(set.get_space())
	for i in range(dims):
		setc = set.copy()
		setc = setc.add_constraint(isl.Constraint.ineq_from_names(space,{greater+str(i): 1, lesser+str(i): -1, 1: -1}))
		finalSet = finalSet.union(setc)
		set = set.add_constraint(isl.Constraint.eq_from_names(space,{greater+str(i): 1, lesser+str(i): -1}))
	#allow exactly same lexicographically depending on static statement occurence
	if stmt1Idx>stmt2Idx:
		finalSet = finalSet.union(set)
	return finalSet

#create dimension names
dNameSet=[]
for i in range(dims):
	string = str(i)
	dNameSet.append('i'+string)
for i in range(dims):
	string = str(i)
	dNameSet.append('j'+string)
dNameSet += ['s','d','e']
for i in range(dims):
	string = str(i)
	dNameSet.append('k'+string)
pNameSet=[]
for i in range(params):
	pNameSet.append('p'+str(i))

#create context and space
ctx = isl.Context()
space = isl.Space.create_from_names(ctx,set=dNameSet,params=pNameSet)

#the final main set to be created by combining several other sets
finalSet = isl.Set.empty(space)
finalSet = finalSet.project_out(isl.dim_type.set,dims*2+3,dims)

#the initial working set with all the constraints that are common
setLv0 = (isl.Set.universe(space)
		  .add_constraint(isl.Constraint.ineq_from_names(space,{'s': 1}))
		  .add_constraint(isl.Constraint.ineq_from_names(space,{'s': -1, 1: nBlocks-1})))

#constraints on the dimensions
for const in domain:
	setLv0 = (setLv0.add_constraint(isl.Constraint.ineq_from_names(space, const))
					.add_constraint(isl.Constraint.ineq_from_names(space,cvtConstrIters(const,'i','j')))
					.add_constraint(isl.Constraint.ineq_from_names(space,cvtConstrIters(const,'i','k'))))

#remove possibility of d=e
setLv0Cpy = (setLv0
    		 .copy()
			 .add_constraint(isl.Constraint.eq_from_names(space,{'d': 1, 'e': -1})))
setLv0 = setLv0.subtract(setLv0Cpy)

#print 'setLv0:\n', setLv0

for i in range(references):
	#create and add constraint that reference at i maps to cache block s, with free parameter d
	lowerConstr = createGTConstraint(refMem[i],{'d': nBlocks*blockSz, 's': blockSz},False)
	upperConstr = createGTConstraint({'d': nBlocks*blockSz, 's': blockSz, 1:blockSz},refMem[i],True)
	setLv1 = (setLv0
			  .add_constraint(isl.Constraint.ineq_from_names(space, lowerConstr))
			  .add_constraint(isl.Constraint.ineq_from_names(space, upperConstr)))
	#print 'setLv1 ', i, ':\n', setLv1
	for j in range(references):
		#create and add constraint that reference at j maps to cache block s, with free parameter e
		lowerConstr = createGTConstraint(cvtConstrIters(refMem[j],'i','j'),{'e': nBlocks*blockSz, 's': blockSz},False)
		upperConstr = createGTConstraint({'e': nBlocks*blockSz, 's': blockSz, 1:blockSz},cvtConstrIters(refMem[j],'i','j'),True)
		setLv2 = (setLv1
				  .add_constraint(isl.Constraint.ineq_from_names(space, lowerConstr))
				  .add_constraint(isl.Constraint.ineq_from_names(space, upperConstr)))
		#add lex constraint: j<i
		setLv2 = addLexConstraint(setLv2,'i','j',i,j)
		#print 'setLv2 ', i, j, ':\n', setLv2
		setLv2Temp = isl.Set.empty(space)
		for k in range(references):
			setLv3 = setLv2.copy()
			#create and add constraint that reference at k maps to cache block s, with free parameter d
			lowerConstr = createGTConstraint(cvtConstrIters(refMem[k],'i','k'),{'d': nBlocks*blockSz, 's': blockSz},False)
			upperConstr = createGTConstraint({'d': nBlocks*blockSz, 's': blockSz, 1:blockSz},cvtConstrIters(refMem[k],'i','k'),True)
			setLv3 = (setLv3
					  .add_constraint(isl.Constraint.ineq_from_names(space, lowerConstr))
					  .add_constraint(isl.Constraint.ineq_from_names(space, upperConstr)))
			setLv3 = addLexConstraint(setLv3,'i','k',i,k)
			setLv3 = addLexConstraint(setLv3,'k','j',k,j)
			setLv2Temp = setLv2Temp.union(setLv3)
		setLv2 = setLv2.project_out(isl.dim_type.set,dims*2+3,dims)
		setLv2Temp = setLv2Temp.project_out(isl.dim_type.set,dims*2+3,dims)
		setLv2 = setLv2.subtract(setLv2Temp)
		finalSet = finalSet.union(setLv2)

finalSet = finalSet.project_out(isl.dim_type.set,dims,dims+3)

print finalSet
