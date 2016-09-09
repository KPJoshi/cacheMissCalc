#Demonstrates the use of user constants
#A matrix multiplication operation is simulated
#The size of the square matrices, the no. of bytes of each data item, and the loop order can be easily changed

#input data

nBlocks = 128 #no. of cache blocks
blockSz = 32 #size of block in bytes

dims = 3 #dimensions in iteration domain
params = 0 #no. of parameters
references = 3 #no. of references to memory locations

#user constants - use these instead of parameters if you want to use a specific value
n = 21 #array size
width = 8 #data size
order = {'i': 'i0', 'j': 'i1', 'k': 'i2'} #loop order

#inequality constraints on the domain
#it is expected that the iteration dimensions are i0, i1, ... and the parameters are p0, p1, ...
#constraining parameters is highly recommended if possible
domain = [{'i0': 1},{'i0': -1, 1: n-1},{'i1': 1},{'i1': -1, 1: n-1},{'i2': 1},{'i2': -1, 1: n-1}]

#equality constraints on the domain of individual statements
#must be a list of lists, one list for each statement, each list containing that statement's constraints
#for use with imperfect loop nests, as statement guards
guards = [[],[],[]]

#memory location accessed by each reference
#representing a linear expression to calculate the memory location accessed by the reference
refMem = ([
		  {order['i']: n*width, order['j']: width}, #a[i][j]
		  {order['i']: n*width, order['k']: width, 1: n*n*width}, #b[i][k]
		  {order['k']: n*width, order['j']: width, 1: 2*n*n*width}, #c[k][j]
])
