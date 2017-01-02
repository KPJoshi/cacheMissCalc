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
foo = 5

#constraints on the domain
#it is expected that the iteration dimensions are i0, i1, ... and the parameters are p0, p1, ...
#additionally, the 'type' should be included and should be 'in' for inequalities or 'eq' for equalities
#constraining parameters is highly recommended
domain = [{'type':'in', 'i0': 1},{'type':'in', 'i0': -1, 'p0': 1, 1: -1},{'type':'in', 'p0': 1},{'type':'in', 'p0': -1, 1: 1023}]

#additional per-statement constraints
#must be a list of lists, with one list for each statement, each list containing the respective statement's constraints
#useful for representing simple imperfectly nested loops
guards = [[],[]]

#memory location accessed by each reference
#there is one tuple for each reference:
#  the first item is a linear expression to calculate the starting memory location
#  the second item is the number of bytes of memory accessed - for now, it is required to be constant
#note - no 'type' required here - the accessed memory addresses are assumed to be [ startAddr , startAddr+size )
refMem = ([
		  ({'i0': 4}, 4), #a[i]
		  ({'i0': 4, 'p0': 4}, 4), #b[i]
])
