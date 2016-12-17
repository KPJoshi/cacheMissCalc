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
	#print 'lc', lowerConstr, 'uc', upperConstr
	setLv1 = (setLv0
			  .add_constraint(isl.Constraint.ineq_from_names(space, lowerConstr))
			  .add_constraint(isl.Constraint.ineq_from_names(space, upperConstr))
			  .add_constraint(isl.Constraint.eq_from_names(space, {'i'+str(dims-1): 1, 1: -i})))
	for c in guards[i]:
		setLv1 = setLv1.add_constraint(isl.Constraint.eq_from_names(space, c))
	#add lex constraint: j<i
	setLv1 = addLexConstraint(setLv1,'i','j')
	#print 'setLv1', i, ':\n', setLv1
	for j in range(references):
		setLv2 = setLv1.copy()
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
		setLv3Agg = isl.Set.empty(space)
		setLv3Template = setLv2.copy()
		#add lex constraint: j<k<i
		setLv3Template = addLexConstraint(setLv3Template,'i','k')
		setLv3Template = addLexConstraint(setLv3Template,'k','j')
		for k in range(references):
			setLv3 = setLv3Template.copy()
			#create and add constraint that reference at k maps to cache block s, with free parameter d
			lowerConstr = createGTConstraint(cvtConstrIters(refMem[k],'i','k'),{'d': nBlocks*blockSz, 's': blockSz},False)
			upperConstr = createGTConstraint({'d': nBlocks*blockSz, 's': blockSz, 1:blockSz},cvtConstrIters(refMem[k],'i','k'),True)
			#print 'lc', lowerConstr, 'uc', upperConstr
			setLv3 = (setLv3
					  .add_constraint(isl.Constraint.ineq_from_names(space, lowerConstr))
					  .add_constraint(isl.Constraint.ineq_from_names(space, upperConstr))
					  .add_constraint(isl.Constraint.eq_from_names(space, {'k'+str(dims-1): 1, 1: -k})))
			for c in guards[k]:
				setLv3 = setLv3.add_constraint(isl.Constraint.eq_from_names(space,cvtConstrIters(c,'i','k')))
			#print 'setLv3', i, j, k, ':\n', setLv3
			setLv3Agg = setLv3Agg.union(setLv3)
		setLv2 = setLv2.project_out(isl.dim_type.set,dims*2+3,dims)
		setLv3Agg = setLv3Agg.project_out(isl.dim_type.set,dims*2+3,dims)
		setLv2 = setLv2.subtract(setLv3Agg)
		finalSet = finalSet.union(setLv2)

finalSet = finalSet.project_out(isl.dim_type.set,dims,dims+3)

#optional step: simplify the set representation - increases processing time
finalSet = finalSet.coalesce()

if outputMode=='iscc':
	print 'card', finalSet, ';'
else:
	print finalSet
