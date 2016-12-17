#Demonstrates an imperfect loop nest
#
# for i0=0, i0<n
#     S1(i0)
#     for i1=1, i1<n
#         S2(i0,i1)
#
#While the second statement is executed at each loop iteration, the first is only executed at the 0th iteration of the inner loop

#See input_template.py for an explanation of the input format

nBlocks = 128
blockSz = 32

dims = 2
params = 0
references = 2

#user constants
n=100

domain = [{'type':'in', 'i0': 1},{'type':'in', 'i0': -1, 1: n-1},{'type':'in', 'i1': 1},{'type':'in', 'i1': -1, 1: n-1}]

guards = [[{'type':'eq', 'i1': 1}],[]] #execute first statement only when i1=0

refMem = ([
		  {'i0': 4*n, 'i1': 4}, #a[i][j]
		  {'i0': 4, 1: 4*n*n}, #b[i]
])
