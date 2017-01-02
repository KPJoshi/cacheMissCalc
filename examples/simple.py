#A simple example (and the input template)
#Consists of two 1D arrays of size p0, such that 0<=p0<=1023, which are arranged one after the other
#Simulates a simple array copy loop

#See input_template.py for an explanation of the input format

nBlocks = 128
blockSz = 32

dims = 1
params = 1
references = 2

domain = [{'type':'in', 'i0': 1},{'type':'in', 'i0': -1, 'p0': 1, 1: -1},{'type':'in', 'p0': 1, 1: -1},{'type':'in', 'p0': -1, 1: 1023}]

guards = [[],[]]

refMem = ([
		  ({'i0': 4}, 4), #a[i]
		  ({'i0': 4, 'p0': 4}, 4), #b[i]
])
