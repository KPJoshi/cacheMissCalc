Internal Cache Miss Calculator by Keyur Joshi

Based on the following paper:
Exact Analysis of the Cache Behavior of Nested Loops
Siddhartha Chatterjee, Erin Parker, Philip J. Hanlon, Alvin R. Lebeck
PLDI 2001
http://dl.acm.org/citation.cfm?id=378859

Requirements:
python and its dependencies
islpy and its dependencies

Instructions for using the python scripts
1) Make a copy of input_template.py and name it input.py
2) Edit input.py with your desired parameters
3) Run internal.py to get the isl representation of a set containing all iteration points where internal cache misses occur
4) Run boundary.py to get the isl representation of a set containing all iteration points where boundary cache misses occur

Instructions for using ISCC to count the number of cache misses
1) Make a copy of iscc_input_template.py
2) Insert the set representation into this copy at the location mentioned
3) Run ISCC and pipe this file into its standard input
