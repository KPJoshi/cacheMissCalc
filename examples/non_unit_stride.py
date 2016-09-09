#An example demonstrating how to use non unit stride iterators
#Consists of one 1D array of size p0, such that 0<=p0<=4095
#The loop simulated is:
#    for( i0 = p0/2 ; i0 < p0 ; i0 += 3 )
#        access array[i0]
#Assuming that p0 is an EVEN number


#input data

nBlocks = 128 #no. of cache blocks
blockSz = 32 #size of block in bytes

dims = 1 #dimensions in iteration domain
params = 1 #no. of parameters
references = 1 #no. of references to memory locations

#user constants - use these instead of parameters if you want to use a specific value

#inequality constraints on the domain
#it is expected that the iteration dimensions are i0, i1, ... and the parameters are p0, p1, ...
#constraining parameters is highly recommended if possible
domain = [{'i0': 1},{'i0': -6, 'p0': 1, 1: -1},{'p0': 1},{'p0': -1, 1: 4095}]

#equality constraints on the domain of individual statements
#must be a list of lists, one list for each statement, each list containing that statement's constraints
#for use with imperfect loop nests, as statement guards
guards = [[],[]]

#memory location accessed by each reference
#representing a linear expression to calculate the memory location accessed by the reference
refMem = ([
		  {'i0': 12, 'p0': 2}, #assuming that p0 is an EVEN number
])
