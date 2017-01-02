#An example demonstrating how to use non unit stride iterators
#Consists of one 1D array of size p0, such that 0<=p0<=4095
#The loop simulated is:
#    for( i0 = 0 ; i0 < p0 ; i0 += 3 )
#        access array[i0]

#See input_template.py for an explanation of the input format

nBlocks = 128 
blockSz = 32

dims = 2 #we will need an extra dimension
params = 1
references = 1

#the first constraint is 3i1=i0, effectively setting the stride of i0 to 3
domain = [{'type':'eq', 'i0': 1, 'i1': -3},{'type':'in', 'i0': 1},{'type':'in', 'i0': -1, 'p0': 1, 1: -1},{'type':'in', 'p0': 1},{'type':'in', 'p0': -1, 1: 4095}]

guards = [[],[]]

refMem = ([
		  ({'i0': 4}, 4)
])
