#Demonstrates the use of user constants
#A matrix multiplication operation is simulated
#The size of the square matrices, the no. of bytes of each data item, and the loop order can be easily changed

#See input_template.py for an explanation of the input format

nBlocks = 128
blockSz = 32

dims = 3
params = 0
references = 3

#user constants - use these instead of parameters if you want to use a specific value
n = 21 #array size
width = 8 #data size
order = {'i': 'i0', 'j': 'i1', 'k': 'i2'} #loop order

domain = [{'type':'in', 'i0': 1},{'type':'in', 'i0': -1, 1: n-1},{'type':'in', 'i1': 1},{'type':'in', 'i1': -1, 1: n-1},{'type':'in', 'i2': 1},{'type':'in', 'i2': -1, 1: n-1}]

guards = [[],[],[]]

refMem = ([
		  {order['i']: n*width, order['j']: width}, #a[i][j]
		  {order['i']: n*width, order['k']: width, 1: n*n*width}, #b[i][k]
		  {order['k']: n*width, order['j']: width, 1: 2*n*n*width}, #c[k][j]
])
