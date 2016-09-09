#Demonstrates an imperfect loop nest
#While the second statement is executed at each loop iteration, the first is only executed at the 0th iteration of the inner loop

#input data

nBlocks = 128 #no. of cache blocks
blockSz = 32 #size of block in bytes

dims = 2 #dimensions in iteration domain
params = 0 #no. of parameters
references = 2 #no. of references to memory locations

#user constants - use these instead of parameters if you want to use a specific value
n=100

#inequality constraints on the domain
#it is expected that the iteration dimensions are i0, i1, ... and the parameters are p0, p1, ...
#constraining parameters is highly recommended if possible
domain = [{'i0': 1},{'i0': -1, 1: n-1},{'i1': 1},{'i1': -1, 1: n-1}]

#equality constraints on the domain of individual statements
#must be a list of lists, one list for each statement, each list containing that statement's constraints
#for use with imperfect loop nests, as statement guards
guards = [[{'i1': 1}],[]] #execute first statement only when i1=0

#memory location accessed by each reference
#representing a linear expression to calculate the memory location accessed by the reference
refMem = ([
		  {'i0': 4*n, 'i1': 4}, #a[i][j]
		  {'i0': 4, 1: 4*n*n}, #b[i]
])
