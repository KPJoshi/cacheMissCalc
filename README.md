# Formula-Based Cache Miss Calculator

By Keyur Joshi
Indian Institute of Technology, Hyderabad

Based on the following paper:
*Exact Analysis of the Cache Behavior of Nested Loops*
Siddhartha Chatterjee, Erin Parker, Philip J. Hanlon, Alvin R. Lebeck
Published in PLDI 2001
([link](http://dl.acm.org/citation.cfm?id=378859))

## Requirements
* python 2.7
* islpy and its dependencies ([link](https://documen.tician.de/islpy/))

## Running the Scripts
* `./internal.py <inputfile> [outputmode]`
* `./boundary.py <inputfile> [outputmode]`

### Breakdown
* The first script is for measuring the number of guaranteed cache misses that occur regardless of the initial cache state.
* The second script is for measuring the maximum number of possible cache misses whose actual occurence depends on the initial cache state.
* `inputfile` is the input file
* `outputmode` is `iscc` by default, and produces output that can be directly piped into the ISCC calculator
* Setting `poly` as the output mode instead will just produce the polygon representing the cache misses

**NOTE**: Use `input_template.py` as an example to create the input file.

### Examples

* `./internal.py input.py`
* `./boundary.py jacobi.py poly`

## Limitations

1. Does not support associativity at the moment.
2. Does not directly support non-unit stride loops. However such a loop can be easily simulated using some linear math on a unit stride iterator.
3. Assumes that only one cache block is referenced at a time. If a single data item spans 2 different cache blocks, only the first one will be considered as accessed.
