#!/usr/bin/env python

try:
	execfile('common.py')
except (IOError, SyntaxError):
	print 'Error: missing common.py'
	sys.exit(1)

#create dimension names
dNameSet=[]
for i in range(dims):
	string = str(i)
	dNameSet.append('i'+string)
dNameSet += ['s','d','e']
for i in range(dims):
	string = str(i)
	dNameSet.append('j'+string)
pNameSet=[]
for i in range(params):
	pNameSet.append('p'+str(i))

#create context and space
ctx = isl.Context()
space = isl.Space.create_from_names(ctx,set=dNameSet,params=pNameSet)

#the final main set to be created by combining several other sets
finalSet = isl.Set.empty(space)
finalSet = finalSet.project_out(isl.dim_type.set,dims+2,dims+1)

#the initial working set with all the constraints that are common
setLv0 = (isl.Set.universe(space)
		  .add_constraint(isl.Constraint.ineq_from_names(space,{'s': 1}))
		  .add_constraint(isl.Constraint.ineq_from_names(space,{'s': -1, 1: nBlocks-1})))

#constraints on the dimensions
for const in domain:
	setLv0 = (setLv0
			  .add_constraint(isl.Constraint.ineq_from_names(space, const))
			  .add_constraint(isl.Constraint.ineq_from_names(space,cvtConstrIters(const,'i','j'))))

#print 'setLv0:\n', setLv0

for i in range(references):
	#create and add constraint that reference at i maps to cache block s, with free parameter d
	lowerConstr = createGTConstraint(refMem[i],{'d': nBlocks*blockSz, 's': blockSz},False)
	upperConstr = createGTConstraint({'d': nBlocks*blockSz, 's': blockSz, 1:blockSz},refMem[i],True)
	#print 'lc', lowerConstr, 'uc', upperConstr
	setLv1 = (setLv0
			  .add_constraint(isl.Constraint.ineq_from_names(space, lowerConstr))
			  .add_constraint(isl.Constraint.ineq_from_names(space, upperConstr))
			  .add_constraint(isl.Constraint.eq_from_names(space, {'i'+str(dims-1): 1, 1: -i})))
	for c in guards[i]:
		setLv1 = setLv1.add_constraint(isl.Constraint.eq_from_names(space,c))
	#print 'setLv1', i, ':\n', setLv1
	setLv2Agg = isl.Set.empty(space)
	setLv2Template = setLv1.copy()
	#add lex constraint: j<i
	setLv2Template = addLexConstraint(setLv2Template,'i','j')
	for j in range(references):
		setLv2 = setLv2Template.copy()
		#print 'setLv2 (0)', i, j, ':\n', setLv2
		#create and add constraint that reference at j maps to cache block s, with free parameter e
		lowerConstr = createGTConstraint(cvtConstrIters(refMem[j],'i','j'),{'e': nBlocks*blockSz, 's': blockSz},False)
		upperConstr = createGTConstraint({'e': nBlocks*blockSz, 's': blockSz, 1:blockSz},cvtConstrIters(refMem[j],'i','j'),True)
		#print 'lc', lowerConstr, 'uc', upperConstr
		setLv2 = (setLv2
				  .add_constraint(isl.Constraint.ineq_from_names(space, lowerConstr))
				  .add_constraint(isl.Constraint.ineq_from_names(space, upperConstr))
				  .add_constraint(isl.Constraint.eq_from_names(space, {'j'+str(dims-1): 1, 1: -j})))
		for c in guards[j]:
			setLv2 = setLv2.add_constraint(isl.Constraint.eq_from_names(space,cvtConstrIters(c,'i','j')))
		#print 'setLv2 (1)', i, j, ':\n', setLv2
		setLv2Agg = setLv2Agg.union(setLv2)
	setLv1 = setLv1.project_out(isl.dim_type.set,dims+2,dims+1)
	setLv2Agg = setLv2Agg.project_out(isl.dim_type.set,dims+2,dims+1)
	setLv1 = setLv1.subtract(setLv2Agg)
	finalSet = finalSet.union(setLv1)

finalSet = finalSet.project_out(isl.dim_type.set,dims,2)

#optional step: simplify the set representation - increases processing time
finalSet = finalSet.coalesce()

if outputMode=='iscc':
	print 'card', finalSet, ';'
else:
	print finalSet
