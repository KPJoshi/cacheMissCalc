Internal Cache Miss Calculator by Keyur Joshi

Based on the following paper:
Exact Analysis of the Cache Behavior of Nested Loops
Siddhartha Chatterjee, Erin Parker, Philip J. Hanlon, Alvin R. Lebeck
PLDI 2001
http://dl.acm.org/citation.cfm?id=378859

Requirements:
python and its dependencies
islpy and its dependencies

Commands:
./internal.py <inputfile> [outputmode]
./boundary.py <inputfile> [outputmode]

The first script is for measuring guaranteed cache misses regardless of initial cache state
The second script is for measuring the maximum number of possible cache misses dependent on the initial cache state
inputfile is the input file
outputmode is 'iscc' by default, produces output that can be directly piped into the ISCC calculator
giving 'poly' (without quotes) as outputmode will just produce the polygon representing the cache misses

Use input_template.py as an example to create the input file
