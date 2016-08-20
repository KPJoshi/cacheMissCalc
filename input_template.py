#THIS IS A TEMPLATE
#Please create a copy of this file and rename it 'input.py' and then modify that copy
#an example is provided below

#input data

nBlocks = 128 #no. of cache blocks
blockSz = 32 #size of block in bytes

dims = 1 #dimensions in iteration domain
params = 1 #no. of parameters
references = 2 #no. of references to memory locations

#user constants - use these instead of parameters if you want to use a specific value

#inequality constraints on the domain
#it is expected that the iteration dimensions are i0, i1, ... and the parameters are p0, p1, ...
#constraining parameters is highly recommended if possible
domain = [{'i0': 1},{'i0': -1, 'p0': 1, 1: -1},{'p0': 1},{'p0': -1, 1: 1023}]

#equality constraints on the domain of individual statements
#must be a list of lists, one list for each statement, each list containing that statement's constraints
#for use with imperfect loop nests, as statement guards
guards = [[],[]]

#memory location accessed by each reference
#representing a linear expression to calculate the memory location accessed by the reference
refMem = ([
		  {'i0': 4}, #a[i]
		  {'i0': 4, 'p0': 4}, #b[i]
])
